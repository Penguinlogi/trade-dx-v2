"""
変更履歴APIのテスト
"""
import pytest
from fastapi import status
from app.models.customer import Customer
from app.models.product import Product
from app.models.case import Case
from app.models.change_history import ChangeHistory


@pytest.mark.unit
class TestChangeHistory:
    """変更履歴エンドポイントのテスト"""

    @pytest.fixture
    def test_case(self, db_session, test_user):
        """テスト用案件を作成"""
        customer = Customer(
            customer_code="C_HIST",
            customer_name="履歴テスト顧客"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        product = Product(
            product_code="P_HIST",
            product_name="履歴テスト商品"
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        case = Case(
            case_number="2025-IM-HIST",
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

    def test_get_change_history(self, client, auth_headers, test_case):
        """変更履歴一覧取得のテスト"""
        # 案件を更新して履歴を作成
        client.put(
            f"/api/cases/{test_case.id}",
            json={"quantity": 200},
            headers=auth_headers
        )

        # 変更履歴を取得
        response = client.get(
            "/api/change-history",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert len(data["items"]) > 0

    def test_get_change_history_filter_by_case_id(self, client, auth_headers, test_case):
        """案件IDでフィルタリングした変更履歴取得のテスト"""
        # 案件を更新
        client.put(
            f"/api/cases/{test_case.id}",
            json={"quantity": 200},
            headers=auth_headers
        )

        # 案件IDでフィルタリング
        response = client.get(
            f"/api/change-history?case_id={test_case.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(item["case_id"] == test_case.id for item in data["items"])

    def test_get_change_history_filter_by_type(self, client, auth_headers, test_case):
        """変更タイプでフィルタリングした変更履歴取得のテスト"""
        # 案件を更新（UPDATE履歴を作成）
        client.put(
            f"/api/cases/{test_case.id}",
            json={"quantity": 200},
            headers=auth_headers
        )

        # UPDATEタイプでフィルタリング
        response = client.get(
            "/api/change-history?change_type=UPDATE",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(item["change_type"] == "UPDATE" for item in data["items"])

    def test_get_change_history_detail(self, client, auth_headers, test_case):
        """変更履歴詳細取得のテスト"""
        # 案件を更新
        client.put(
            f"/api/cases/{test_case.id}",
            json={"quantity": 200},
            headers=auth_headers
        )

        # 変更履歴一覧を取得してIDを取得
        list_response = client.get(
            "/api/change-history",
            headers=auth_headers
        )
        assert list_response.status_code == status.HTTP_200_OK
        history_id = list_response.json()["items"][0]["id"]

        # 詳細を取得
        response = client.get(
            f"/api/change-history/{history_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == history_id
        assert "case_id" in data
        assert "change_type" in data

    def test_get_case_change_history(self, client, auth_headers, test_case):
        """特定案件の変更履歴取得のテスト"""
        # 案件を更新
        client.put(
            f"/api/cases/{test_case.id}",
            json={"quantity": 200},
            headers=auth_headers
        )

        # 案件の変更履歴を取得
        response = client.get(
            f"/api/change-history/case/{test_case.id}/history",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert all(item["case_id"] == test_case.id for item in data["items"])

    def test_get_change_history_pagination(self, client, auth_headers, test_case):
        """変更履歴のページネーションテスト"""
        # 複数回更新して履歴を作成
        for i in range(3):
            client.put(
                f"/api/cases/{test_case.id}",
                json={"quantity": 100 + i * 10},
                headers=auth_headers
            )

        # 1ページ目を取得
        response = client.get(
            "/api/change-history?page=1&page_size=2",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) <= 2
        assert data["page"] == 1

    def test_get_change_history_unauthorized(self, client):
        """認証なしでの変更履歴取得のテスト"""
        response = client.get("/api/change-history")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
