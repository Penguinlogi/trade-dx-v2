"""
アプリケーション設定
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """アプリケーション設定"""

    # アプリケーション情報
    APP_NAME: str = "貿易DX管理システム"
    APP_VERSION: str = "2.1.0"
    DEBUG: bool = True

    # サーバー設定
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # データベース設定
    DATABASE_URL: str = "sqlite:///./trade_dx.db"

    # JWT設定
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS設定
    CORS_ORIGINS: List str = [
        "http://localhost:3000",
        "http://localhost:3000",
    ]

    # ログ設定
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

@property
def cors_origins_list(self) -> List[str]:
    """CORS_ORIGINSをリストに変換"""
    if self.CORS_ORIGINS == "*":
        return ["*"]
    return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

# グローバル設定インスタンス
settings = Settings()
