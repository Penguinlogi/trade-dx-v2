"""
商品APIのテスト
"""
import pytest
from fastapi import status
from app.models.product import Product


@pytest.mark.unit
class TestProducts:
    """商品エンドポイントのテスト"""

    def test_create_product(self, client, auth_headers):
        """商品の作成"""
        product_data = {
            "product_code": "P999",
            "product_name": "新規テスト商品"
        }
        response = client.post(
            "/api/products",
            json=product_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["product_code"] == product_data["product_code"]
        assert data["product_name"] == product_data["product_name"]

    def test_get_products(self, client, auth_headers, db_session):
        """商品一覧の取得"""
        # テストデータを作成
        product = Product(
            product_code="P998",
            product_name="テスト商品2"
        )
        db_session.add(product)
        db_session.commit()

        response = client.get(
            "/api/products",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) > 0

    def test_get_product_by_id(self, client, auth_headers, db_session):
        """商品IDで取得"""
        product = Product(
            product_code="P997",
            product_name="テスト商品3"
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        response = client.get(
            f"/api/products/{product.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == product.id
        assert data["product_code"] == product.product_code

    def test_update_product(self, client, auth_headers, db_session):
        """商品の更新"""
        product = Product(
            product_code="P996",
            product_name="テスト商品4"
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        update_data = {
            "product_name": "更新された商品名"
        }
        response = client.put(
            f"/api/products/{product.id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_name"] == update_data["product_name"]

    def test_delete_product(self, client, auth_headers, db_session):
        """商品の削除"""
        product = Product(
            product_code="P995",
            product_name="テスト商品5"
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        product_id = product.id

        response = client.delete(
            f"/api/products/{product_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 削除確認（論理削除なので、取得できるがis_active=0になっている）
        response = client.get(
            f"/api/products/{product_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] == 0
