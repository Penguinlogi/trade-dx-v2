"""
案件APIのテスト
"""
import pytest
from fastapi import status
from app.models.customer import Customer
from app.models.product import Product
from app.models.case import Case


@pytest.mark.unit
class TestCases:
    """案件エンドポイントのテスト"""

    @pytest.fixture
    def test_customer(self, db_session):
        """テスト用顧客を作成"""
        customer = Customer(
            customer_code="C001",
            customer_name="テスト顧客"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        return customer

    @pytest.fixture
    def test_product(self, db_session):
        """テスト用商品を作成"""
        product = Product(
            product_code="P001",
            product_name="テスト商品"
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        return product

    def test_create_case(self, client, auth_headers, test_customer, test_product):
        """案件の作成"""
        case_data = {
            "case_number": "2025-IM-001",
            "customer_id": test_customer.id,
            "product_id": test_product.id,
            "trade_type": "輸入",
            "quantity": 100,
            "unit": "pcs",
            "sales_unit_price": 1000,
            "purchase_unit_price": 800,
            "status": "見積中",
            "pic": "テスト担当"
        }
        response = client.post(
            "/api/cases",
            json=case_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["case_number"] == case_data["case_number"]
        # quantityはDecimal型なので文字列として返される可能性がある
        assert float(data["quantity"]) == float(case_data["quantity"])
        assert float(data["sales_unit_price"]) == float(case_data["sales_unit_price"])

    def test_get_cases(self, client, auth_headers, db_session, test_customer, test_product):
        """案件一覧の取得"""
        # テストデータを作成
        case = Case(
            case_number="2025-IM-001",
            customer_id=test_customer.id,
            product_id=test_product.id,
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

        response = client.get(
            "/api/cases",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert len(data["items"]) > 0

    def test_get_case_by_id(self, client, auth_headers, db_session, test_customer, test_product):
        """案件IDで取得"""
        case = Case(
            case_number="2025-IM-002",
            customer_id=test_customer.id,
            product_id=test_product.id,
            trade_type="輸入",
            quantity=200,
            unit="pcs",
            sales_unit_price=2000,
            purchase_unit_price=1600,
            status="見積中",
            pic="テスト担当"
        )
        db_session.add(case)
        db_session.commit()
        db_session.refresh(case)

        response = client.get(
            f"/api/cases/{case.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == case.id
        assert data["case_number"] == case.case_number

    def test_update_case(self, client, auth_headers, db_session, test_customer, test_product):
        """案件の更新"""
        case = Case(
            case_number="2025-IM-003",
            customer_id=test_customer.id,
            product_id=test_product.id,
            trade_type="輸入",
            quantity=300,
            unit="pcs",
            sales_unit_price=3000,
            purchase_unit_price=2400,
            status="見積中",
            pic="テスト担当"
        )
        db_session.add(case)
        db_session.commit()
        db_session.refresh(case)

        update_data = {
            "quantity": 350,
            "sales_unit_price": 3500,
            "purchase_unit_price": 2800,
            "status": "受注済"
        }
        response = client.put(
            f"/api/cases/{case.id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # quantityはDecimal型なので文字列として返される可能性がある
        assert float(data["quantity"]) == float(update_data["quantity"])
        assert float(data["sales_unit_price"]) == float(update_data["sales_unit_price"])
        assert data["status"] == update_data["status"]

    def test_delete_case(self, client, auth_headers, db_session, test_customer, test_product):
        """案件の削除"""
        case = Case(
            case_number="2025-IM-004",
            customer_id=test_customer.id,
            product_id=test_product.id,
            trade_type="輸入",
            quantity=400,
            unit="pcs",
            sales_unit_price=4000,
            purchase_unit_price=3200,
            status="見積中",
            pic="テスト担当"
        )
        db_session.add(case)
        db_session.commit()
        db_session.refresh(case)
        case_id = case.id

        response = client.delete(
            f"/api/cases/{case_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 削除確認
        response = client.get(
            f"/api/cases/{case_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_cases_with_search(self, client, auth_headers, db_session, test_customer, test_product):
        """検索機能のテスト"""
        case = Case(
            case_number="2025-IM-SEARCH",
            customer_id=test_customer.id,
            product_id=test_product.id,
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

        response = client.get(
            "/api/cases?search=SEARCH",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) > 0
        assert any("SEARCH" in item["case_number"] for item in data["items"])
