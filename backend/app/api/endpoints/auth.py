"""
認証APIエンドポイント
"""
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.config import settings
from ...core.deps import get_db, get_current_active_user
from ...core.security import verify_password, create_access_token
from ...models.user import User as UserModel
from ...schemas.auth import LoginResponse, Token
from ...schemas.user import User

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    ユーザーログイン

    Args:
        db: データベースセッション
        form_data: ログインフォームデータ

    Returns:
        LoginResponse: アクセストークンとユーザー情報

    Raises:
        HTTPException: 認証に失敗した場合
    """
    # ユーザーを取得
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()

    # ユーザーが存在しない、またはパスワードが一致しない場合
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ユーザーが非アクティブの場合
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="非アクティブなユーザーです"
        )

    # アクセストークンを作成
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
async def logout(
    current_user: UserModel = Depends(get_current_active_user)
) -> Any:
    """
    ユーザーログアウト

    Note:
        JWTはステートレスなので、サーバー側で特別な処理は不要
        クライアント側でトークンを削除する

    Args:
        current_user: 現在のユーザー

    Returns:
        dict: 成功メッセージ
    """
    return {"message": "ログアウトしました"}


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_active_user)
) -> Any:
    """
    現在のユーザー情報を取得

    Args:
        current_user: 現在のユーザー

    Returns:
        User: ユーザー情報
    """
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: UserModel = Depends(get_current_active_user)
) -> Any:
    """
    トークンをリフレッシュ

    Args:
        current_user: 現在のユーザー

    Returns:
        Token: 新しいアクセストークン
    """
    # 新しいアクセストークンを作成
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }








