"""
案件番号スキーマ
"""
from typing import Literal
from pydantic import BaseModel, Field


class CaseNumberGenerateRequest(BaseModel):
    """案件番号生成リクエスト"""
    trade_type: Literal["輸出", "輸入"] = Field(..., description="区分（輸出/輸入）")


class CaseNumberGenerateResponse(BaseModel):
    """案件番号生成レスポンス"""
    case_number: str = Field(..., description="生成された案件番号")
    year: int = Field(..., description="年")
    trade_type: str = Field(..., description="区分")
    trade_type_code: str = Field(..., description="区分コード")
    sequence: int = Field(..., description="連番")
