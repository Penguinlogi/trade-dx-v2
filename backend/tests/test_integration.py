"""
統合テスト
"""
import pytest
from fastapi import status
from app.models.customer import Customer
from app.models.product import Product
from app.models.case import Case


@pytest.mark.integration
class TestIntegration:
    """統合テスト"""

    def test_case_workflow(self, client, auth_headers, db_session):
        """案件の完全なワークフロー"""
        # 1. 顧客を作成
        customer_data = {
            "customer_code": "C_INTEG",  # 最大10文字
            "customer_name": "統合テスト顧客"
        }
        response = client.post(
            "/api/customers",
            json=customer_data,
            headers=auth_headers
        )
        if response.status_code != status.HTTP_201_CREATED:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            print(f"\n[ERROR] Customer creation failed: {response.status_code}")
            print(f"[ERROR] Request: {customer_data}")
            print(f"[ERROR] Response: {error_detail}\n")
        assert response.status_code == status.HTTP_201_CREATED, f"Customer creation failed: {response.status_code}"
        customer_id = response.json()["id"]

        # 2. 商品を作成
        product_data = {
            "product_code": "P_INTEG",  # 最大10文字
            "product_name": "統合テスト商品"
        }
        response = client.post(
            "/api/products",
            json=product_data,
            headers=auth_headers
        )
        if response.status_code != status.HTTP_201_CREATED:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            print(f"\n[ERROR] Product creation failed: {response.status_code}")
            print(f"[ERROR] Request: {product_data}")
            print(f"[ERROR] Response: {error_detail}\n")
        assert response.status_code == status.HTTP_201_CREATED, f"Product creation failed: {response.status_code}"
        product_id = response.json()["id"]

        # 3. 案件を作成
        case_data = {
            "case_number": "2025-IM-INTEGRATION",
            "customer_id": customer_id,
            "product_id": product_id,
            "trade_type": "輸入",
            "quantity": 1000,
            "unit": "pcs",
            "sales_unit_price": 5000,
            "purchase_unit_price": 4000,
            "status": "見積中",
            "pic": "統合テスト担当"
        }
        response = client.post(
            "/api/cases",
            json=case_data,
            headers=auth_headers
        )
        # エラーの場合は詳細を表示
        error_detail = None
        if response.status_code != status.HTTP_201_CREATED:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            print(f"\n[ERROR] Case creation failed: {response.status_code}")
            print(f"[ERROR] Request data: {case_data}")
            print(f"[ERROR] Response: {error_detail}\n")
        assert response.status_code == status.HTTP_201_CREATED, f"Case creation failed: {response.status_code} - {error_detail if error_detail else response.text}"
        case_id = response.json()["id"]

        # 4. 案件を取得
        response = client.get(
            f"/api/cases/{case_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        case = response.json()
        assert case["case_number"] == case_data["case_number"]
        assert case["customer"]["id"] == customer_id
        assert case["product"]["id"] == product_id

        # 5. 案件を更新
        update_data = {
            "quantity": 1500,
            "status": "受注済"
        }
        response = client.put(
            f"/api/cases/{case_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        updated_case = response.json()
        # quantityはDecimal型なので文字列として返される可能性がある
        assert float(updated_case["quantity"]) == float(update_data["quantity"])
        assert updated_case["status"] == update_data["status"]

        # 6. 案件を削除
        response = client.delete(
            f"/api/cases/{case_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 7. 削除確認
        response = client.get(
            f"/api/cases/{case_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthorized_access(self, client):
        """認証なしでのアクセステスト"""
        # 認証なしで案件一覧を取得しようとする
        response = client.get("/api/cases")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # 認証なしで顧客一覧を取得しようとする
        response = client.get("/api/customers")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # 認証なしで商品一覧を取得しようとする
        response = client.get("/api/products")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
