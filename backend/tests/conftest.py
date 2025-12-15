"""
pytest設定とフィクスチャ
"""
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash

# get_dbを明示的にインポート（オーバーライド用）
# 注意: auth.pyなどではcore.deps.get_dbを使用しているため、こちらをオーバーライドする必要がある
from app.core.deps import get_db as original_get_db


# テスト用データベースURL
TEST_DATABASE_URL = "sqlite:///:memory:"

# テスト用エンジン
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# テスト用セッションファクトリ
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    テスト用データベースセッション
    各テスト関数ごとに新しいセッションを作成
    """
    # テーブルを作成
    Base.metadata.create_all(bind=test_engine)

    # セッションを作成
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # テーブルを削除
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    テスト用FastAPIクライアント
    """
    # get_dbをオーバーライドする関数
    def override_get_db():
        # テスト用セッションを返す
        yield db_session
        # セッションは閉じない（テスト終了時に閉じる）

    # 依存性をオーバーライド
    # get_db関数オブジェクト自体をキーとして使用
    app.dependency_overrides[original_get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # クリーンアップ: オーバーライドを削除
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    """
    テスト用ユーザーを作成
    """
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="テストユーザー",
        is_active=True,
        is_superuser=False
    )
    db_session.add(user)
    db_session.flush()  # フラッシュしてIDを取得
    db_session.commit()  # コミット
    db_session.refresh(user)  # リフレッシュして最新の状態を取得

    # ユーザーが正しく保存されたことを確認
    from app.models.user import User as UserModel
    db_user = db_session.query(UserModel).filter(UserModel.username == user.username).first()
    assert db_user is not None, "User should be saved to database"

    return user


@pytest.fixture(scope="function")
def test_superuser(db_session):
    """
    テスト用スーパーユーザーを作成
    """
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        full_name="管理者",
        is_active=True,
        is_superuser=True
    )
    db_session.add(user)
    db_session.flush()  # フラッシュしてIDを取得
    db_session.commit()  # コミット
    db_session.refresh(user)  # リフレッシュして最新の状態を取得

    # ユーザーが正しく保存されたことを確認
    from app.models.user import User as UserModel
    db_user = db_session.query(UserModel).filter(UserModel.username == user.username).first()
    assert db_user is not None, "Superuser should be saved to database"

    return user


@pytest.fixture(scope="function")
def auth_headers(client, test_user, db_session):
    """
    認証済みリクエスト用のヘッダーを取得
    """
    # セッションをフラッシュして、変更を確実にコミット
    db_session.flush()
    db_session.commit()

    # ユーザーがデータベースに存在することを確認
    from app.models.user import User
    db_user = db_session.query(User).filter(User.username == test_user.username).first()
    assert db_user is not None, "Test user should exist in database"

    # パスワード検証
    from app.core.security import verify_password
    password_valid = verify_password("testpassword", db_user.hashed_password)
    assert password_valid, f"Password verification should succeed. Hashed: {db_user.hashed_password[:50]}..."

    # セッションを明示的にリフレッシュして、変更を確実に反映
    db_session.expire_all()
    db_session.refresh(db_user)

    # ログインリクエスト
    # OAuth2PasswordRequestFormはapplication/x-www-form-urlencoded形式を期待
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user.username,
            "password": "testpassword"
        }
    )

    if response.status_code != 200:
        # デバッグ情報を出力
        print(f"\n[DEBUG] Login failed with status {response.status_code}")
        print(f"[DEBUG] Response: {response.text}")
        print(f"[DEBUG] Request URL: /api/auth/login")
        print(f"[DEBUG] Request data: username={test_user.username}, password=testpassword")
        print(f"[DEBUG] User in DB session: username={db_user.username}, is_active={db_user.is_active}, id={db_user.id}")
        print(f"[DEBUG] DB session id: {id(db_session)}")
        print(f"[DEBUG] Password valid in test: {password_valid}")

        # セッション内の全ユーザーを確認
        all_users = db_session.query(User).all()
        print(f"[DEBUG] All users in DB session: {[(u.username, u.id, u.is_active) for u in all_users]}")

        # ログインエンドポイントが使用するセッションを確認するため、
        # 直接get_dbを呼び出して確認（これは実際にはオーバーライドされたもの）
        from app.core.database import get_db
        # 注意: これは実際にはオーバーライドされたget_dbを呼び出す
        # しかし、直接呼び出すとオーバーライドが機能しない可能性がある
        # 代わりに、ログインエンドポイントが使用するセッションでユーザーを確認
        # これは難しいので、別のアプローチを試す

    assert response.status_code == 200, f"Login failed: {response.status_code} - {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_headers(client, test_superuser, db_session):
    """
    管理者認証済みリクエスト用のヘッダーを取得
    """
    # セッションをフラッシュして、変更を確実にコミット
    db_session.flush()
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        data={
            "username": test_superuser.username,
            "password": "adminpassword"
        }
    )
    assert response.status_code == 200, f"Admin login failed: {response.status_code} - {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
