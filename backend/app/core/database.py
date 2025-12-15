"""
データベース接続管理
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLiteの場合の接続引数
if "sqlite" in settings.DATABASE_URL:
    connect_args = {
        "check_same_thread": False,
    }
else:
    connect_args = {}

# データベースエンジンの作成
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args
)

# SQLiteの場合、外部キー制約は有効化しない
# （既存のDBとの互換性のため、また変更履歴を残すため）
# 外部キー制約を有効化すると、案件削除時に変更履歴も削除される可能性がある
# if "sqlite" in settings.DATABASE_URL:
#     @event.listens_for(engine, "connect")
#     def set_sqlite_pragma(dbapi_conn, connection_record):
#         cursor = dbapi_conn.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON")
#         cursor.close()

# セッションファクトリの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()


def get_db():
    """
    データベースセッションを取得する依存性注入関数
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
