"""
案件スキーマ
"""
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


# ベーススキーマ
class CaseBase(BaseModel):
    """案件ベーススキーマ"""
    case_number: Optional[str] = Field(None, max_length=20, description="案件番号")
    trade_type: str = Field(..., max_length=10, description="区分（輸出/輸入）")
    customer_id: int = Field(..., description="顧客ID")
    supplier_name: Optional[str] = Field(None, max_length=100, description="仕入先名")
    product_id: int = Field(..., description="商品ID")
    quantity: Decimal = Field(..., gt=0, description="数量")
    unit: str = Field(..., max_length=10, description="単位")
    sales_unit_price: Decimal = Field(..., ge=0, description="販売単価")
    purchase_unit_price: Decimal = Field(..., ge=0, description="仕入単価")
    shipment_date: Optional[date] = Field(None, description="船積予定日")
    status: str = Field(..., max_length=20, description="ステータス")
    pic: str = Field(..., max_length=50, description="担当者名")
    notes: Optional[str] = Field(None, description="備考")

    @field_validator('trade_type')
    @classmethod
    def validate_trade_type(cls, v: str) -> str:
        """区分のバリデーション"""
        allowed = ['輸出', '輸入']
        if v not in allowed:
            raise ValueError(f'区分は {", ".join(allowed)} のいずれかである必要があります')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """ステータスのバリデーション"""
        allowed = ['見積中', '受注済', '船積済', '完了', 'キャンセル']
        if v not in allowed:
            raise ValueError(f'ステータスは {", ".join(allowed)} のいずれかである必要があります')
        return v


# 案件作成用
class CaseCreate(CaseBase):
    """案件作成スキーマ"""
    pass


# 案件更新用
class CaseUpdate(BaseModel):
    """案件更新スキーマ"""
    trade_type: Optional[str] = Field(None, max_length=10, description="区分（輸出/輸入）")
    customer_id: Optional[int] = Field(None, description="顧客ID")
    supplier_name: Optional[str] = Field(None, max_length=100, description="仕入先名")
    product_id: Optional[int] = Field(None, description="商品ID")
    quantity: Optional[Decimal] = Field(None, gt=0, description="数量")
    unit: Optional[str] = Field(None, max_length=10, description="単位")
    sales_unit_price: Optional[Decimal] = Field(None, ge=0, description="販売単価")
    purchase_unit_price: Optional[Decimal] = Field(None, ge=0, description="仕入単価")
    shipment_date: Optional[date] = Field(None, description="船積予定日")
    status: Optional[str] = Field(None, max_length=20, description="ステータス")
    pic: Optional[str] = Field(None, max_length=50, description="担当者名")
    notes: Optional[str] = Field(None, description="備考")

    @field_validator('trade_type')
    @classmethod
    def validate_trade_type(cls, v: Optional[str]) -> Optional[str]:
        """区分のバリデーション"""
        if v is None:
            return v
        allowed = ['輸出', '輸入']
        if v not in allowed:
            raise ValueError(f'区分は {", ".join(allowed)} のいずれかである必要があります')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """ステータスのバリデーション"""
        if v is None:
            return v
        allowed = ['見積中', '受注済', '船積済', '完了', 'キャンセル']
        if v not in allowed:
            raise ValueError(f'ステータスは {", ".join(allowed)} のいずれかである必要があります')
        return v


# 顧客情報（埋め込み用）
class CustomerInCase(BaseModel):
    """案件内の顧客情報"""
    id: int
    customer_code: str
    customer_name: str

    class Config:
        from_attributes = True


# 商品情報（埋め込み用）
class ProductInCase(BaseModel):
    """案件内の商品情報"""
    id: int
    product_code: str
    product_name: str
    hs_code: Optional[str] = None

    class Config:
        from_attributes = True


# 案件レスポンス用
class Case(CaseBase):
    """案件レスポンススキーマ"""
    id: int
    sales_amount: Optional[Decimal] = None
    gross_profit: Optional[Decimal] = None
    gross_profit_rate: Optional[Decimal] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    # リレーション
    customer: Optional[CustomerInCase] = None
    product: Optional[ProductInCase] = None

    class Config:
        from_attributes = True


# 案件一覧用（簡易版）
class CaseListItem(BaseModel):
    """案件一覧用スキーマ"""
    id: int
    case_number: str
    trade_type: str
    customer_id: int
    customer_name: Optional[str] = None
    product_id: int
    product_name: Optional[str] = None
    quantity: Decimal
    unit: str
    sales_amount: Optional[Decimal] = None
    gross_profit: Optional[Decimal] = None
    gross_profit_rate: Optional[Decimal] = None
    status: str
    pic: str
    shipment_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ページネーションレスポンス
class CaseListResponse(BaseModel):
    """案件一覧レスポンス（ページネーション付き）"""
    items: list[CaseListItem]
    total: int
    page: int
    page_size: int
    total_pages: int

