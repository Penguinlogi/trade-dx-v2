"""
依存性注入（Dependencies）
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from .security import decode_access_token
from ..models.user import User

# OAuth2スキーム
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Generator:
    """
    データベースセッションを取得する

    Yields:
        Session: SQLAlchemyセッション
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    現在のユーザーを取得する

    Args:
        token: JWTトークン
        db: データベースセッション

    Returns:
        User: 現在のユーザー

    Raises:
        HTTPException: 認証に失敗した場合
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報を検証できませんでした",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # トークンをデコード
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # ユーザーIDを取得（JWTのsubは文字列として保存されている可能性があるため、intに変換）
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception

    # ユーザーを取得
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    現在のアクティブなユーザーを取得する

    Args:
        current_user: 現在のユーザー

    Returns:
        User: アクティブなユーザー

    Raises:
        HTTPException: ユーザーが非アクティブの場合
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="非アクティブなユーザーです"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    現在のスーパーユーザーを取得する

    Args:
        current_user: 現在のユーザー

    Returns:
        User: スーパーユーザー

    Raises:
        HTTPException: ユーザーがスーパーユーザーでない場合
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を実行する権限がありません"
        )
    return current_user
