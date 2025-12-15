"""
ユーザースキーマ
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """ユーザー基本スキーマ"""
    username: str = Field(..., min_length=3, max_length=50, description="ユーザー名")
    email: EmailStr = Field(..., description="メールアドレス")
    full_name: Optional[str] = Field(None, max_length=100, description="フルネーム")


class UserCreate(UserBase):
    """ユーザー作成スキーマ"""
    password: str = Field(..., min_length=8, description="パスワード")


class UserUpdate(BaseModel):
    """ユーザー更新スキーマ"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="ユーザー名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    full_name: Optional[str] = Field(None, max_length=100, description="フルネーム")
    password: Optional[str] = Field(None, min_length=8, description="パスワード")
    is_active: Optional[bool] = Field(None, description="アクティブ状態")
    is_superuser: Optional[bool] = Field(None, description="スーパーユーザー")


class UserInDB(UserBase):
    """データベース内のユーザースキーマ"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    """レスポンス用ユーザースキーマ"""
    pass






