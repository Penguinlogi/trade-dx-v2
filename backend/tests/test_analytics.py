"""
集計・ダッシュボードAPIのテスト
"""
import pytest
from fastapi import status
from datetime import datetime, timedelta
from app.models.customer import Customer
from app.models.product import Product
from app.models.case import Case


@pytest.mark.unit
class TestAnalytics:
    """集計・ダッシュボードエンドポイントのテスト"""

    @pytest.fixture
    def test_data(self, db_session):
        """テスト用データを作成"""
        customer = Customer(
            customer_code="C_ANALYTICS",
            customer_name="集計テスト顧客"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        product = Product(
            product_code="P_ANALYTICS",
            product_name="集計テスト商品"
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        # 複数の案件を作成
        cases = []
        for i in range(3):
            case = Case(
                case_number=f"2025-IM-ANALYTICS-{i+1}",
                customer_id=customer.id,
                product_id=product.id,
                trade_type="輸入",
                quantity=100 * (i + 1),
                unit="pcs",
                sales_unit_price=1000,
                purchase_unit_price=800,
                status="見積中" if i < 2 else "完了",
                pic="テスト担当"
            )
            db_session.add(case)
            cases.append(case)
        db_session.commit()
        for case in cases:
            db_session.refresh(case)

        return {
            "customer": customer,
            "product": product,
            "cases": cases
        }

    def test_get_analytics_summary(self, client, auth_headers, test_data):
        """集計サマリー取得のテスト"""
        response = client.get(
            "/api/analytics/summary",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "summary" in data
        assert "status_distribution" in data
        summary = data["summary"]
        assert "total_cases" in summary
        assert "active_cases" in summary
        assert "completed_cases" in summary
        assert "total_customers" in summary
        assert "total_products" in summary
        assert "this_month_cases" in summary
        assert "this_month_revenue" in summary
        assert "last_month_revenue" in summary

    def test_get_analytics_summary_with_date_range(self, client, auth_headers, test_data):
        """日付範囲指定での集計サマリー取得のテスト"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        response = client.get(
            f"/api/analytics/summary?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "summary" in data
        assert "total_cases" in data["summary"]

    def test_get_analytics_trends(self, client, auth_headers, test_data):
        """月次トレンド取得のテスト"""
        response = client.get(
            "/api/analytics/trends?period_months=12",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "trends" in data
        assert isinstance(data["trends"], list)

    def test_get_analytics_trends_custom_period(self, client, auth_headers, test_data):
        """カスタム期間での月次トレンド取得のテスト"""
        response = client.get(
            "/api/analytics/trends?period_months=6",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "trends" in data

    def test_get_analytics_by_customer(self, client, auth_headers, test_data):
        """顧客別売上TOP取得のテスト"""
        response = client.get(
            "/api/analytics/by-customer?limit=10",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "top_customers" in data
        assert isinstance(data["top_customers"], list)

    def test_get_analytics_by_customer_custom_limit(self, client, auth_headers, test_data):
        """カスタム件数での顧客別売上TOP取得のテスト"""
        response = client.get(
            "/api/analytics/by-customer?limit=5",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "top_customers" in data
        assert len(data["top_customers"]) <= 5

    def test_get_analytics_unauthorized(self, client):
        """認証なしでの集計データ取得のテスト"""
        response = client.get("/api/analytics/summary")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
