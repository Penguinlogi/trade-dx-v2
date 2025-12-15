"""
ユーザー情報確認スクリプト
"""
import sys
sys.path.append('..')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User

# データベース接続
DATABASE_URL = "sqlite:///./trade_dx.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def check_users():
    """ユーザー一覧を表示"""
    db = SessionLocal()
    try:
        users = db.query(User).all()

        if not users:
            print("❌ ユーザーが1人も登録されていません")
            print("\nシードデータを投入してください:")
            print("  python scripts/seed_data.py")
            return False

        print(f"✅ {len(users)}人のユーザーが登録されています\n")
        print("-" * 80)
        for user in users:
            print(f"ID: {user.id}")
            print(f"ユーザー名: {user.username}")
            print(f"メール: {user.email}")
            print(f"フルネーム: {user.full_name}")
            print(f"アクティブ: {user.is_active}")
            print(f"スタッフ: {user.is_staff}")
            print(f"管理者: {user.is_superuser}")
            print("-" * 80)

        # testuserが存在するか確認
        testuser = db.query(User).filter(User.username == "testuser").first()
        if testuser:
            print("\n✅ testuser が存在します")
            print("ログイン情報:")
            print("  ユーザー名: testuser")
            print("  パスワード: testpass123")
        else:
            print("\n❌ testuser が存在しません")
            print("シードデータを投入してください:")
            print("  python scripts/seed_data.py")

        return True

    except Exception as e:
        print(f"❌ エラー: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    check_users()







