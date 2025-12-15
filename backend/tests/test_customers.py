"""
顧客APIのテスト
"""
import pytest
from fastapi import status
from app.models.customer import Customer


@pytest.mark.unit
class TestCustomers:
    """顧客エンドポイントのテスト"""

    def test_create_customer(self, client, auth_headers):
        """顧客の作成"""
        customer_data = {
            "customer_code": "C999",
            "customer_name": "新規テスト顧客"
        }
        response = client.post(
            "/api/customers",
            json=customer_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["customer_code"] == customer_data["customer_code"]
        assert data["customer_name"] == customer_data["customer_name"]

    def test_get_customers(self, client, auth_headers, db_session):
        """顧客一覧の取得"""
        # テストデータを作成
        customer = Customer(
            customer_code="C998",
            customer_name="テスト顧客2"
        )
        db_session.add(customer)
        db_session.commit()

        response = client.get(
            "/api/customers",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) > 0

    def test_get_customer_by_id(self, client, auth_headers, db_session):
        """顧客IDで取得"""
        customer = Customer(
            customer_code="C997",
            customer_name="テスト顧客3"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        response = client.get(
            f"/api/customers/{customer.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == customer.id
        assert data["customer_code"] == customer.customer_code

    def test_update_customer(self, client, auth_headers, db_session):
        """顧客の更新"""
        customer = Customer(
            customer_code="C996",
            customer_name="テスト顧客4"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        update_data = {
            "customer_name": "更新された顧客名"
        }
        response = client.put(
            f"/api/customers/{customer.id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["customer_name"] == update_data["customer_name"]

    def test_delete_customer(self, client, auth_headers, db_session):
        """顧客の削除"""
        customer = Customer(
            customer_code="C995",
            customer_name="テスト顧客5"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        customer_id = customer.id

        response = client.delete(
            f"/api/customers/{customer_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 削除確認（論理削除なので、取得できるがis_active=0になっている）
        response = client.get(
            f"/api/customers/{customer_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] == 0
