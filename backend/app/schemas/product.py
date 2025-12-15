"""
商品マスタスキーマ
"""
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """商品マスタ基底スキーマ"""
    product_code: str = Field(..., min_length=1, max_length=10, description="商品コード")
    product_name: str = Field(..., min_length=1, max_length=100, description="商品名（日本語）")
    product_name_en: Optional[str] = Field(None, max_length=200, description="商品名（英語）")
    hs_code: Optional[str] = Field(None, max_length=20, description="HSコード")
    unit: Optional[str] = Field(None, max_length=10, description="単位（kg, pcs, m3, etc.）")
    standard_price: Optional[Decimal] = Field(None, ge=0, description="標準単価")
    category: Optional[str] = Field(None, max_length=50, description="カテゴリ")
    specification: Optional[str] = Field(None, description="仕様・スペック")
    notes: Optional[str] = Field(None, description="備考")
    is_active: int = Field(1, description="有効フラグ（1=有効, 0=無効）")


class ProductCreate(ProductBase):
    """商品マスタ作成スキーマ"""
    pass


class ProductUpdate(BaseModel):
    """商品マスタ更新スキーマ"""
    product_code: Optional[str] = Field(None, min_length=1, max_length=10)
    product_name: Optional[str] = Field(None, min_length=1, max_length=100)
    product_name_en: Optional[str] = Field(None, max_length=200)
    hs_code: Optional[str] = Field(None, max_length=20)
    unit: Optional[str] = Field(None, max_length=10)
    standard_price: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)
    specification: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[int] = None


class ProductInDB(ProductBase):
    """商品マスタDB保存スキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductResponse(ProductInDB):
    """商品マスタレスポンススキーマ"""
    pass


class ProductListResponse(BaseModel):
    """商品マスタ一覧レスポンススキーマ"""
    total: int
    items: list[ProductResponse]
    page: int
    page_size: int
    total_pages: int






