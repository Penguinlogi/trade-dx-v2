"""
FastAPI メインアプリケーション
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .core.database import engine, Base
from .api.endpoints import auth, cases, case_numbers, customers, products, analytics, documents, change_history, backups, websocket
from scripts.seed_data import main as init_db

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# データベーステーブルの作成
try:
    Base.metadata.create_all(bind=engine)
    logger.info("データベーステーブルの作成が完了しました")
except Exception as e:
    logger.error(f"データベーステーブルの作成に失敗しました: {str(e)}")

# FastAPIアプリケーションの作成
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="貿易業務を効率化するDX管理システム",
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターの登録
app.include_router(auth.router, prefix="/api/auth", tags=["認証"])
app.include_router(cases.router, prefix="/api/cases", tags=["案件管理"])
app.include_router(case_numbers.router, prefix="/api/case-numbers", tags=["案件番号"])
app.include_router(customers.router, prefix="/api/customers", tags=["顧客マスタ"])
app.include_router(products.router, prefix="/api/products", tags=["商品マスタ"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["分析・集計"])
app.include_router(documents.router, prefix="/api/documents", tags=["ドキュメント生成"])
app.include_router(change_history.router, prefix="/api/change-history", tags=["変更履歴"])
app.include_router(backups.router, prefix="/api/backups", tags=["バックアップ"])
app.include_router(websocket.router, prefix="/api", tags=["WebSocket"])

@app.on_event("startup")
async def startup_event():
    """アプリ起動時の処理"""
    # データベース初期化
    init_db()

@app.get("/")
async def root():
    """
    ルートエンドポイント（ヘルスチェック）
    """
    return {
        "message": f"{settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    グローバル例外ハンドラー
    """
    logger.error(f"未処理のエラーが発生しました: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "内部サーバーエラーが発生しました"}
    )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

