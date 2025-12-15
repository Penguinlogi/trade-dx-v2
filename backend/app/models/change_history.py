"""
変更履歴モデル
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class ChangeHistory(Base):
    """変更履歴テーブル"""
    __tablename__ = "change_history"

    id = Column(Integer, primary_key=True, index=True)
    # 案件削除後も履歴を残すため、外部キー制約は通常通り設定
    # SQLiteでは外部キー制約がデフォルトで無効のため、案件削除時もcase_idは保持される
    # 既存のDBでcase_idがnullable=Falseの場合でも動作する
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True, comment="案件ID")

    # 変更情報
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="変更者ID")
    change_type = Column(String(20), nullable=False, comment="変更タイプ（CREATE/UPDATE/DELETE）")

    # 変更内容
    field_name = Column(String(50), nullable=True, comment="変更フィールド名")
    old_value = Column(Text, nullable=True, comment="変更前の値")
    new_value = Column(Text, nullable=True, comment="変更後の値")

    # 変更の詳細（JSON形式で複数フィールドの変更を保存）
    changes_json = Column(JSON, nullable=True, comment="変更詳細（JSON）")

    # 備考
    notes = Column(Text, nullable=True, comment="備考")

    # タイムスタンプ
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # リレーション（案件が削除されても履歴は残るため、削除された案件も参照可能にする）
    # lazy='select'（デフォルト）を使用し、案件が削除されている場合はNoneになる
    case = relationship("Case", back_populates="change_histories")

    def __repr__(self):
        return f"<ChangeHistory(id={self.id}, case_id={self.case_id}, type={self.change_type}, changed_at={self.changed_at})>"
