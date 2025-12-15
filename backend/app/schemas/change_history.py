"""
変更履歴スキーマ
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any
from decimal import Decimal


class ChangeHistoryBase(BaseModel):
    """変更履歴ベーススキーマ"""
    case_id: Optional[int] = Field(None, description="案件ID（削除時はNULL）")
    changed_by: Optional[int] = Field(None, description="変更者ID")
    change_type: str = Field(..., description="変更タイプ（CREATE/UPDATE/DELETE）")
    field_name: Optional[str] = Field(None, description="変更フィールド名")
    old_value: Optional[str] = Field(None, description="変更前の値")
    new_value: Optional[str] = Field(None, description="変更後の値")
    changes_json: Optional[dict[str, Any]] = Field(None, description="変更詳細（JSON）")
    notes: Optional[str] = Field(None, description="備考")


class ChangeHistory(ChangeHistoryBase):
    """変更履歴レスポンススキーマ"""
    id: int
    changed_at: datetime

    class Config:
        from_attributes = True


class ChangeHistoryListItem(BaseModel):
    """変更履歴一覧用スキーマ"""
    id: int
    case_id: Optional[int] = None
    case_number: Optional[str] = None
    changed_by: Optional[int] = None
    changed_by_name: Optional[str] = None
    change_type: str
    field_name: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    changes_json: Optional[dict[str, Any]] = None
    notes: Optional[str] = None
    changed_at: datetime

    class Config:
        from_attributes = True


class ChangeHistoryListResponse(BaseModel):
    """変更履歴一覧レスポンス（ページネーション付き）"""
    items: list[ChangeHistoryListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
