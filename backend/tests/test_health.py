"""
ヘルスチェックAPIのテスト
"""
import pytest
from fastapi import status


@pytest.mark.unit
class TestHealth:
    """ヘルスチェックエンドポイントのテスト"""

    def test_root_endpoint(self, client):
        """ルートエンドポイントのテスト"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"

    def test_health_check(self, client):
        """ヘルスチェックエンドポイントのテスト"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "app_name" in data
        assert "version" in data
