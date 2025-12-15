"""
testuserを追加するスクリプト
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from passlib.context import CryptContext
from app.core.database import SessionLocal
from app.models import User

# パスワードハッシュ化
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_testuser():
    """testuserを追加"""
    db = SessionLocal()

    try:
        # 既存チェック
        existing = db.query(User).filter(User.username == "testuser").first()
        if existing:
            print("[OK] testuser は既に存在します")
            print(f"  ユーザー名: {existing.username}")
            print(f"  メール: {existing.email}")
            print(f"  フルネーム: {existing.full_name}")
            return

        # testuserを作成
        testuser = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password=pwd_context.hash("testpass123"),
            full_name="テストユーザー",
            is_active=True,
            is_superuser=False,
        )

        db.add(testuser)
        db.commit()

        print("[OK] testuser を作成しました")
        print("\nログイン情報:")
        print("  ユーザー名: testuser")
        print("  パスワード: testpass123")
        print("  メール: testuser@example.com")

    except Exception as e:
        print(f"[ERROR] エラー: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_testuser()
