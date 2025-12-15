"""
分析・集計APIエンドポイント
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ...core.database import get_db
from ...core.deps import get_current_active_user
from ...models.user import User
from ...services.analytics import AnalyticsService
from ...schemas.analytics import (
    AnalyticsSummaryResponse,
    TrendsResponse,
    CustomerRevenueResponse,
)

router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    start_date: Optional[datetime] = Query(None, description="開始日時"),
    end_date: Optional[datetime] = Query(None, description="終了日時"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    集計サマリーを取得

    - 総案件数、進行中案件数、完了案件数
    - 顧客数、商品数
    - 今月・先月の案件数と売上額
    - 案件ステータス分布
    """
    analytics_service = AnalyticsService(db)
    result = analytics_service.get_summary(start_date, end_date)
    return result


@router.get("/trends", response_model=TrendsResponse)
async def get_analytics_trends(
    period_months: int = Query(12, ge=1, le=36, description="期間（月数）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    月次トレンドを取得

    - 指定期間の月次案件数と売上額のトレンド
    """
    analytics_service = AnalyticsService(db)
    result = analytics_service.get_trends(period_months)
    return result


@router.get("/by-customer", response_model=CustomerRevenueResponse)
async def get_analytics_by_customer(
    limit: int = Query(10, ge=1, le=50, description="上位件数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    顧客別売上TOP取得

    - 顧客別の案件数と総売上額
    - 売上額の降順でソート
    """
    analytics_service = AnalyticsService(db)
    result = analytics_service.get_top_customers(limit)
    return result
