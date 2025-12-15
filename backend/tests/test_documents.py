"""
ドキュメント生成APIのテスト
"""
import pytest
from fastapi import status
from pathlib import Path
from app.models.customer import Customer
from app.models.product import Product
from app.models.case import Case
from app.models.document import Document


@pytest.mark.unit
class TestDocuments:
    """ドキュメント生成エンドポイントのテスト"""

    @pytest.fixture
    def test_case(self, db_session, test_user):
        """テスト用案件を作成"""
        customer = Customer(
            customer_code="C_DOC",
            customer_name="ドキュメントテスト顧客"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        product = Product(
            product_code="P_DOC",
            product_name="ドキュメントテスト商品"
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        case = Case(
            case_number="2025-IM-DOC",
            customer_id=customer.id,
            product_id=product.id,
            trade_type="輸入",
            quantity=100,
            unit="pcs",
            sales_unit_price=1000,
            purchase_unit_price=800,
            status="見積中",
            pic="テスト担当"
        )
        db_session.add(case)
        db_session.commit()
        db_session.refresh(case)
        return case

    def test_generate_invoice(self, client, auth_headers, test_case):
        """Invoice生成のテスト"""
        response = client.post(
            "/api/documents/invoice",
            json={
                "case_id": test_case.id,
                "document_type": "invoice"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["case_id"] == test_case.id
        assert data["document_type"] == "invoice"
        assert "file_name" in data
        assert data["generated_by"] is not None

    def test_generate_packing_list(self, client, auth_headers, test_case):
        """Packing List生成のテスト"""
        response = client.post(
            "/api/documents/packing-list",
            json={
                "case_id": test_case.id,
                "document_type": "packing_list"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["case_id"] == test_case.id
        assert data["document_type"] == "packing_list"
        assert "file_name" in data

    def test_generate_invoice_invalid_case(self, client, auth_headers):
        """存在しない案件でのInvoice生成のテスト"""
        response = client.post(
            "/api/documents/invoice",
            json={
                "case_id": 99999,
                "document_type": "invoice"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_generate_invoice_invalid_type(self, client, auth_headers, test_case):
        """無効なdocument_typeでのInvoice生成のテスト"""
        response = client.post(
            "/api/documents/invoice",
            json={
                "case_id": test_case.id,
                "document_type": "invalid_type"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_documents(self, client, auth_headers, test_case):
        """ドキュメント一覧取得のテスト"""
        # まずドキュメントを生成
        client.post(
            "/api/documents/invoice",
            json={
                "case_id": test_case.id,
                "document_type": "invoice"
            },
            headers=auth_headers
        )

        # 一覧を取得
        response = client.get(
            "/api/documents",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "documents" in data
        assert "total" in data
        assert len(data["documents"]) > 0

    def test_get_documents_filter_by_case_id(self, client, auth_headers, test_case):
        """案件IDでフィルタリングしたドキュメント一覧取得のテスト"""
        # ドキュメントを生成
        client.post(
            "/api/documents/invoice",
            json={
                "case_id": test_case.id,
                "document_type": "invoice"
            },
            headers=auth_headers
        )

        # 案件IDでフィルタリング
        response = client.get(
            f"/api/documents?case_id={test_case.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(doc["case_id"] == test_case.id for doc in data["documents"])

    def test_get_documents_filter_by_type(self, client, auth_headers, test_case):
        """ドキュメントタイプでフィルタリングした一覧取得のテスト"""
        # Invoiceを生成
        client.post(
            "/api/documents/invoice",
            json={
                "case_id": test_case.id,
                "document_type": "invoice"
            },
            headers=auth_headers
        )

        # invoiceタイプでフィルタリング
        response = client.get(
            "/api/documents?document_type=invoice",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(doc["document_type"] == "invoice" for doc in data["documents"])

    def test_download_document(self, client, auth_headers, test_case):
        """ドキュメントダウンロードのテスト"""
        # ドキュメントを生成
        create_response = client.post(
            "/api/documents/invoice",
            json={
                "case_id": test_case.id,
                "document_type": "invoice"
            },
            headers=auth_headers
        )
        assert create_response.status_code == status.HTTP_200_OK
        document_id = create_response.json()["id"]

        # ダウンロード
        response = client.get(
            f"/api/documents/{document_id}/download",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def test_download_document_not_found(self, client, auth_headers):
        """存在しないドキュメントのダウンロードのテスト"""
        response = client.get(
            "/api/documents/99999/download",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_documents_unauthorized(self, client):
        """認証なしでのドキュメント一覧取得のテスト"""
        response = client.get("/api/documents")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
