"""
分析・集計スキーマ
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SummaryData(BaseModel):
    """サマリーデータ"""
    total_cases: int = Field(..., description="総案件数")
    active_cases: int = Field(..., description="進行中案件数")
    completed_cases: int = Field(..., description="完了案件数")
    total_customers: int = Field(..., description="総顧客数")
    total_products: int = Field(..., description="総商品数")
    this_month_cases: int = Field(..., description="今月の案件数")
    this_month_revenue: float = Field(..., description="今月の売上額")
    last_month_revenue: float = Field(..., description="先月の売上額")


class CaseStatusDistribution(BaseModel):
    """案件ステータス分布"""
    status: str = Field(..., description="ステータス")
    count: int = Field(..., description="件数")
    percentage: float = Field(..., description="割合(%)")


class MonthlyTrend(BaseModel):
    """月次トレンドデータ"""
    year_month: str = Field(..., description="年月 (YYYY-MM)")
    case_count: int = Field(..., description="案件数")
    revenue: float = Field(..., description="売上額")


class CustomerRevenue(BaseModel):
    """顧客別売上"""
    customer_id: int = Field(..., description="顧客ID")
    customer_code: str = Field(..., description="顧客コード")
    customer_name: str = Field(..., description="顧客名")
    case_count: int = Field(..., description="案件数")
    total_revenue: float = Field(..., description="総売上額")


class AnalyticsSummaryResponse(BaseModel):
    """集計サマリーレスポンス"""
    summary: SummaryData
    status_distribution: List[CaseStatusDistribution]


class TrendsResponse(BaseModel):
    """トレンドレスポンス"""
    trends: List[MonthlyTrend]
    period_months: int = Field(..., description="期間（月数）")


class CustomerRevenueResponse(BaseModel):
    """顧客別売上レスポンス"""
    top_customers: List[CustomerRevenue]
    limit: int = Field(..., description="上位件数")


class AnalyticsFilters(BaseModel):
    """分析フィルター"""
    start_date: Optional[datetime] = Field(None, description="開始日")
    end_date: Optional[datetime] = Field(None, description="終了日")
    customer_id: Optional[int] = Field(None, description="顧客ID")
    status: Optional[str] = Field(None, description="ステータス")





