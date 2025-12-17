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
    # マイグレーションを自動実行（PostgreSQL用）
    try:
        from alembic.config import Config
        from alembic import command
        import os

        # データベースURLがPostgreSQLの場合のみマイグレーションを実行
        if "postgresql" in settings.DATABASE_URL.lower():
            # 作業ディレクトリをbackendに設定
            backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend")
            alembic_ini_path = os.path.join(backend_dir, "alembic.ini")

            if os.path.exists(alembic_ini_path):
                alembic_cfg = Config(alembic_ini_path)
                alembic_cfg.set_main_option("script_location", os.path.join(backend_dir, "alembic"))
                try:
                    command.upgrade(alembic_cfg, "head")
                    logger.info("データベースマイグレーションが完了しました")
                except Exception as e:
                    logger.warning(f"マイグレーション実行中にエラーが発生しました（続行）: {str(e)}")
            else:
                # alembic.iniが見つからない場合、直接SQLでスキーマを更新
                try:
                    from sqlalchemy import text
                    from .core.database import SessionLocal
                    db = SessionLocal()
                    try:
                        # change_history.case_idがnullableかどうかを確認
                        result = db.execute(text("""
                            SELECT is_nullable
                            FROM information_schema.columns
                            WHERE table_name = 'change_history'
                            AND column_name = 'case_id'
                        """))
                        row = result.fetchone()
                        if row and row[0] == 'NO':
                            # nullable=Falseの場合、スキーマを更新
                            logger.info("change_history.case_idをnullable=Trueに変更します")
                            # 外部キー制約を削除
                            db.execute(text("""
                                ALTER TABLE change_history
                                DROP CONSTRAINT IF EXISTS change_history_case_id_fkey
                            """))
                            # case_idをnullable=Trueに変更
                            db.execute(text("""
                                ALTER TABLE change_history
                                ALTER COLUMN case_id DROP NOT NULL
                            """))
                            # 外部キー制約を再作成（ON DELETE SET NULL）
                            db.execute(text("""
                                ALTER TABLE change_history
                                ADD CONSTRAINT change_history_case_id_fkey
                                FOREIGN KEY (case_id) REFERENCES cases(id)
                                ON DELETE SET NULL
                            """))
                            db.commit()
                            logger.info("change_history.case_idのスキーマ更新が完了しました")
                        else:
                            logger.info("change_history.case_idは既にnullable=Trueです")
                    except Exception as schema_error:
                        db.rollback()
                        logger.warning(f"スキーマ更新中にエラーが発生しました（続行）: {str(schema_error)}")
                    finally:
                        db.close()
                except Exception as e:
                    logger.warning(f"スキーマ更新の試行に失敗しました（続行）: {str(e)}")
    except Exception as e:
        logger.warning(f"マイグレーションの自動実行に失敗しました（続行）: {str(e)}")

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
