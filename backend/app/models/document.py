"""
ドキュメントモデル
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Document(Base):
    """
    生成されたドキュメントの履歴を管理するテーブル
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    document_type = Column(String(50), nullable=False)  # "invoice" or "packing_list"
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)  # 保存されたファイルのパス（オプション）
    template_name = Column(String(255), nullable=True)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    generated_at = Column(DateTime, default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)

    # リレーション
    case = relationship("Case", back_populates="documents")
    user = relationship("User")

    def __repr__(self):
        return f"<Document(id={self.id}, case_id={self.case_id}, type={self.document_type}, file={self.file_name})>"

