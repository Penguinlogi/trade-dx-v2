"""
案件番号管理モデル
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class CaseNumber(Base):
    """案件番号管理テーブル
    
    案件番号の自動採番を管理する。
    形式: YYYY-XX-NNN
    - YYYY: 年
    - XX: 区分コード (EX=輸出, IM=輸入)
    - NNN: 連番 (001-999)
    """
    __tablename__ = "case_numbers"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True, comment="年（YYYY）")
    trade_type = Column(String(10), nullable=False, index=True, comment="区分（輸出/輸入）")
    trade_type_code = Column(String(2), nullable=False, comment="区分コード（EX/IM）")
    last_sequence = Column(Integer, default=0, nullable=False, comment="最後に使用した連番")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<CaseNumber(year={self.year}, type={self.trade_type}, last_seq={self.last_sequence})>"

    @classmethod
    def generate_case_number(cls, year: int, trade_type: str, sequence: int) -> str:
        """案件番号を生成する
        
        Args:
            year: 年（YYYY）
            trade_type: 区分（輸出/輸入）
            sequence: 連番
            
        Returns:
            案件番号（例: 2025-EX-001）
        """
        type_code = "EX" if trade_type == "輸出" else "IM"
        return f"{year}-{type_code}-{sequence:03d}"












