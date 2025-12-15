"""
認証スキーマ
"""
from pydantic import BaseModel, Field
from .user import User


class Token(BaseModel):
    """トークンレスポンススキーマ"""
    access_token: str = Field(..., description="アクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")


class TokenData(BaseModel):
    """トークンデータスキーマ"""
    user_id: int


class LoginRequest(BaseModel):
    """ログインリクエストスキーマ"""
    username: str = Field(..., description="ユーザー名")
    password: str = Field(..., description="パスワード")


class LoginResponse(BaseModel):
    """ログインレスポンススキーマ"""
    access_token: str = Field(..., description="アクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
    user: User = Field(..., description="ユーザー情報")






