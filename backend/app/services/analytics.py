"""
分析・集計サービス
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, desc
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict
from decimal import Decimal

from ..models.case import Case
from ..models.customer import Customer
from ..models.product import Product
from ..schemas.analytics import (
    SummaryData,
    CaseStatusDistribution,
    MonthlyTrend,
    CustomerRevenue,
)


class AnalyticsService:
    """分析サービス"""

    def __init__(self, db: Session):
        self.db = db

    def get_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict:
        """サマリーデータを取得"""
        # 日付フィルター条件
        query_filter = []
        if start_date:
            query_filter.append(Case.created_at >= start_date)
        if end_date:
            query_filter.append(Case.created_at <= end_date)

        # 総案件数
        total_cases = self.db.query(func.count(Case.id)).filter(*query_filter).scalar() or 0

        # 進行中案件数（見積中、受注済、船積済）
        active_statuses = ["見積中", "受注済", "船積済"]
        active_cases = (
            self.db.query(func.count(Case.id))
            .filter(Case.status.in_(active_statuses))
            .filter(*query_filter)
            .scalar() or 0
        )

        # 完了案件数
        completed_cases = (
            self.db.query(func.count(Case.id))
            .filter(Case.status == "完了")
            .filter(*query_filter)
            .scalar() or 0
        )

        # 総顧客数
        total_customers = self.db.query(func.count(Customer.id)).scalar() or 0

        # 総商品数
        total_products = self.db.query(func.count(Product.id)).scalar() or 0

        # 今月の案件数と売上額
        today = date.today()
        first_day_of_month = date(today.year, today.month, 1)

        this_month_cases = (
            self.db.query(func.count(Case.id))
            .filter(Case.created_at >= first_day_of_month)
            .scalar() or 0
        )

        this_month_revenue = (
            self.db.query(func.coalesce(func.sum(Case.sales_amount), 0))
            .filter(Case.created_at >= first_day_of_month)
            .scalar() or 0
        )

        # 先月の売上額
        if today.month == 1:
            last_month = date(today.year - 1, 12, 1)
            first_day_of_this_month = date(today.year, 1, 1)
        else:
            last_month = date(today.year, today.month - 1, 1)
            first_day_of_this_month = first_day_of_month

        last_month_revenue = (
            self.db.query(func.coalesce(func.sum(Case.sales_amount), 0))
            .filter(Case.created_at >= last_month)
            .filter(Case.created_at < first_day_of_this_month)
            .scalar() or 0
        )

        summary = SummaryData(
            total_cases=total_cases,
            active_cases=active_cases,
            completed_cases=completed_cases,
            total_customers=total_customers,
            total_products=total_products,
            this_month_cases=this_month_cases,
            this_month_revenue=float(this_month_revenue),
            last_month_revenue=float(last_month_revenue),
        )

        # ステータス分布
        status_distribution = self._get_status_distribution(query_filter)

        return {
            "summary": summary,
            "status_distribution": status_distribution,
        }

    def _get_status_distribution(self, query_filter: List) -> List[CaseStatusDistribution]:
        """ステータス分布を取得"""
        # ステータス別の件数を取得
        status_counts = (
            self.db.query(
                Case.status,
                func.count(Case.id).label("count")
            )
            .filter(*query_filter)
            .group_by(Case.status)
            .all()
        )

        # 総件数
        total = sum(row.count for row in status_counts)

        # パーセンテージを計算
        distribution = []
        for row in status_counts:
            percentage = (row.count / total * 100) if total > 0 else 0
            distribution.append(
                CaseStatusDistribution(
                    status=row.status,
                    count=row.count,
                    percentage=round(percentage, 2),
                )
            )

        # ステータス順にソート（定義順）
        status_order = ["見積中", "受注済", "船積済", "完了", "キャンセル"]
        distribution.sort(key=lambda x: status_order.index(x.status) if x.status in status_order else 999)

        return distribution

    def get_trends(self, period_months: int = 12) -> Dict:
        """月次トレンドを取得"""
        # 期間の開始日を計算（N ヶ月前の1日）
        today = date.today()
        start_date = date(today.year, today.month, 1) - timedelta(days=(period_months - 1) * 31)
        start_date = date(start_date.year, start_date.month, 1)

        # 月次集計
        monthly_data = (
            self.db.query(
                func.strftime('%Y-%m', Case.created_at).label('year_month'),
                func.count(Case.id).label('case_count'),
                func.coalesce(func.sum(Case.sales_amount), 0).label('revenue')
            )
            .filter(Case.created_at >= start_date)
            .group_by(func.strftime('%Y-%m', Case.created_at))
            .order_by(func.strftime('%Y-%m', Case.created_at))
            .all()
        )

        trends = [
            MonthlyTrend(
                year_month=row.year_month,
                case_count=row.case_count,
                revenue=float(row.revenue),
            )
            for row in monthly_data
        ]

        return {
            "trends": trends,
            "period_months": period_months,
        }

    def get_top_customers(self, limit: int = 10) -> Dict:
        """顧客別売上TOP取得"""
        # 顧客別の案件数と売上額を集計
        customer_data = (
            self.db.query(
                Customer.id,
                Customer.customer_code,
                Customer.customer_name,
                func.count(Case.id).label('case_count'),
                func.coalesce(func.sum(Case.sales_amount), 0).label('total_revenue')
            )
            .join(Case, Customer.id == Case.customer_id)
            .group_by(Customer.id, Customer.customer_code, Customer.customer_name)
            .order_by(desc('total_revenue'))
            .limit(limit)
            .all()
        )

        top_customers = [
            CustomerRevenue(
                customer_id=row.id,
                customer_code=row.customer_code,
                customer_name=row.customer_name,
                case_count=row.case_count,
                total_revenue=float(row.total_revenue),
            )
            for row in customer_data
        ]

        return {
            "top_customers": top_customers,
            "limit": limit,
        }





