"""
顧客マスタスキーマ
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class CustomerBase(BaseModel):
    """顧客マスタ基底スキーマ"""
    customer_code: str = Field(..., min_length=1, max_length=10, description="顧客コード")
    customer_name: str = Field(..., min_length=1, max_length=100, description="顧客名（日本語）")
    customer_name_en: Optional[str] = Field(None, max_length=200, description="顧客名（英語）")
    address: Optional[str] = Field(None, description="住所（日本語）")
    address_en: Optional[str] = Field(None, description="住所（英語）")
    phone: Optional[str] = Field(None, max_length=20, description="電話番号")
    contact_person: Optional[str] = Field(None, max_length=50, description="担当者名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    payment_terms: Optional[str] = Field(None, max_length=50, description="支払条件")
    notes: Optional[str] = Field(None, description="備考")
    is_active: int = Field(1, description="有効フラグ（1=有効, 0=無効）")


class CustomerCreate(CustomerBase):
    """顧客マスタ作成スキーマ"""
    pass


class CustomerUpdate(BaseModel):
    """顧客マスタ更新スキーマ"""
    customer_code: Optional[str] = Field(None, min_length=1, max_length=10)
    customer_name: Optional[str] = Field(None, min_length=1, max_length=100)
    customer_name_en: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = None
    address_en: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    contact_person: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    payment_terms: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    is_active: Optional[int] = None


class CustomerInDB(CustomerBase):
    """顧客マスタDB保存スキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerResponse(CustomerInDB):
    """顧客マスタレスポンススキーマ"""
    pass


class CustomerListResponse(BaseModel):
    """顧客マスタ一覧レスポンススキーマ"""
    total: int
    items: list[CustomerResponse]
    page: int
    page_size: int
    total_pages: int








