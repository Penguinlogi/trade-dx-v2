"""
認証APIのテスト
"""
import pytest
from fastapi import status


@pytest.mark.unit
class TestAuth:
    """認証エンドポイントのテスト"""

    def test_login_success(self, client, test_user):
        """正常なログイン"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": test_user.username,
                "password": "testpassword"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    def test_login_invalid_username(self, client):
        """存在しないユーザー名でのログイン"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent",
                "password": "password"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_invalid_password(self, client, test_user):
        """間違ったパスワードでのログイン"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": test_user.username,
                "password": "wrongpassword"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, client, auth_headers, test_user):
        """現在のユーザー情報取得"""
        response = client.get(
            "/api/auth/me",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email

    def test_get_current_user_unauthorized(self, client):
        """認証なしでのユーザー情報取得"""
        response = client.get("/api/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout(self, client, auth_headers):
        """ログアウト"""
        response = client.post(
            "/api/auth/logout",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
