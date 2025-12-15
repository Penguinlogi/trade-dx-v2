"""
バックアップ履歴モデル
"""
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Text
from sqlalchemy.sql import func
from ..core.database import Base


class Backup(Base):
    """バックアップ履歴テーブル"""
    __tablename__ = "backups"

    id = Column(Integer, primary_key=True, index=True)
    backup_name = Column(String(100), nullable=False, comment="バックアップ名")
    backup_path = Column(String(500), nullable=False, comment="バックアップファイルパス")
    backup_type = Column(String(20), nullable=False, comment="バックアップタイプ（manual/auto/scheduled）")
    file_size = Column(BigInteger, nullable=True, comment="ファイルサイズ（バイト）")
    record_count = Column(Integer, nullable=True, comment="レコード数")
    status = Column(String(20), nullable=False, comment="ステータス（success/failed/in_progress）")
    error_message = Column(Text, nullable=True, comment="エラーメッセージ")
    created_by = Column(Integer, nullable=True, comment="作成者ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    def __repr__(self):
        return f"<Backup(id={self.id}, name={self.backup_name}, type={self.backup_type}, status={self.status})>"












