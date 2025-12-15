"""
ドキュメントスキーマ
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    """ドキュメント基本スキーマ"""
    case_id: int = Field(..., description="案件ID")
    document_type: str = Field(..., description="ドキュメントタイプ（invoice/packing_list）")
    template_name: Optional[str] = Field(None, description="テンプレート名")
    notes: Optional[str] = Field(None, description="備考")


class DocumentCreate(DocumentBase):
    """ドキュメント作成スキーマ"""
    pass


class DocumentGenerateRequest(BaseModel):
    """ドキュメント生成リクエスト"""
    case_id: int = Field(..., description="案件ID")
    document_type: str = Field(..., description="ドキュメントタイプ（invoice/packing_list）")
    template_name: Optional[str] = Field(None, description="テンプレート名（省略時はデフォルト）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "case_id": 1,
                "document_type": "invoice",
                "template_name": "default_invoice_template.xlsx"
            }
        }


class DocumentResponse(DocumentBase):
    """ドキュメントレスポンス"""
    id: int
    file_name: str = Field(..., description="生成されたファイル名")
    file_path: Optional[str] = Field(None, description="ファイルパス")
    generated_by: int = Field(..., description="生成者ID")
    generated_at: datetime = Field(..., description="生成日時")
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """ドキュメント一覧レスポンス"""
    documents: list[DocumentResponse]
    total: int


class InvoiceData(BaseModel):
    """Invoice データ構造"""
    # 基本情報
    invoice_number: str
    invoice_date: str
    
    # 顧客情報
    customer_name: str
    customer_address: Optional[str] = None
    customer_contact: Optional[str] = None
    
    # 商品情報
    product_name: str
    product_code: Optional[str] = None
    quantity: float
    unit: str
    unit_price: float
    total_amount: float
    
    # 案件情報
    case_number: str
    shipment_date: Optional[str] = None
    notes: Optional[str] = None


class PackingListData(BaseModel):
    """Packing List データ構造"""
    # 基本情報
    packing_list_number: str
    packing_date: str
    
    # 顧客情報
    customer_name: str
    customer_address: Optional[str] = None
    
    # 商品情報
    product_name: str
    product_code: Optional[str] = None
    quantity: float
    unit: str
    gross_weight: Optional[float] = None
    net_weight: Optional[float] = None
    package_count: Optional[int] = None
    
    # 案件情報
    case_number: str
    shipment_date: Optional[str] = None
    notes: Optional[str] = None

