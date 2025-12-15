"""
商品マスタモデル
"""
from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Product(Base):
    """商品マスタテーブル"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(10), unique=True, nullable=False, index=True, comment="商品コード")
    product_name = Column(String(100), nullable=False, comment="商品名（日本語）")
    product_name_en = Column(String(200), nullable=True, comment="商品名（英語）")
    hs_code = Column(String(20), nullable=True, comment="HSコード")
    unit = Column(String(10), nullable=True, comment="単位（kg, pcs, m3, etc.）")
    standard_price = Column(Numeric(15, 2), nullable=True, comment="標準単価")
    category = Column(String(50), nullable=True, comment="カテゴリ")
    specification = Column(Text, nullable=True, comment="仕様・スペック")
    notes = Column(Text, nullable=True, comment="備考")
    is_active = Column(Integer, default=1, nullable=False, comment="有効フラグ（1=有効, 0=無効）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # リレーション
    cases = relationship("Case", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, code={self.product_code}, name={self.product_name})>"












