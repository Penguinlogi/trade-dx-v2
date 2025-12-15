"""
バックアップスキーマ
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BackupBase(BaseModel):
    """バックアップベーススキーマ"""
    backup_name: str = Field(..., description="バックアップ名")
    backup_path: str = Field(..., description="バックアップファイルパス")
    backup_type: str = Field(..., description="バックアップタイプ（manual/auto/scheduled）")
    file_size: Optional[int] = Field(None, description="ファイルサイズ（バイト）")
    record_count: Optional[int] = Field(None, description="レコード数")
    status: str = Field(..., description="ステータス（success/failed/in_progress）")
    error_message: Optional[str] = Field(None, description="エラーメッセージ")


class Backup(BackupBase):
    """バックアップレスポンススキーマ"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BackupCreate(BaseModel):
    """バックアップ作成リクエストスキーマ"""
    backup_name: Optional[str] = Field(None, description="バックアップ名（未指定時は自動生成）")
    backup_type: str = Field("manual", description="バックアップタイプ（manual/auto/scheduled）")


class BackupRestore(BaseModel):
    """バックアップ復元リクエストスキーマ"""
    backup_id: int = Field(..., description="復元するバックアップID")


class BackupListResponse(BaseModel):
    """バックアップ一覧レスポンス（ページネーション付き）"""
    items: list[Backup]
    total: int
    page: int
    page_size: int
    total_pages: int






