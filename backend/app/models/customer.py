"""
顧客マスタモデル
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Customer(Base):
    """顧客マスタテーブル"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_code = Column(String(10), unique=True, nullable=False, index=True, comment="顧客コード")
    customer_name = Column(String(100), nullable=False, comment="顧客名（日本語）")
    customer_name_en = Column(String(200), nullable=True, comment="顧客名（英語）")
    address = Column(Text, nullable=True, comment="住所（日本語）")
    address_en = Column(Text, nullable=True, comment="住所（英語）")
    phone = Column(String(20), nullable=True, comment="電話番号")
    contact_person = Column(String(50), nullable=True, comment="担当者名")
    email = Column(String(100), nullable=True, comment="メールアドレス")
    payment_terms = Column(String(50), nullable=True, comment="支払条件")
    notes = Column(Text, nullable=True, comment="備考")
    is_active = Column(Integer, default=1, nullable=False, comment="有効フラグ（1=有効, 0=無効）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # リレーション
    cases = relationship("Case", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.id}, code={self.customer_code}, name={self.customer_name})>"












