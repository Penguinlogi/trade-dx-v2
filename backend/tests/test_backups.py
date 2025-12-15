"""
バックアップAPIのテスト
"""
import pytest
from fastapi import status
from pathlib import Path
from app.models.backup import Backup


@pytest.mark.unit
class TestBackups:
    """バックアップエンドポイントのテスト"""

    def test_create_backup(self, client, auth_headers):
        """バックアップ作成のテスト"""
        response = client.post(
            "/api/backups/create",
            json={
                "backup_name": "テストバックアップ",
                "backup_type": "manual"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["backup_name"] == "テストバックアップ"
        assert data["backup_type"] == "manual"
        assert data["status"] == "success"
        assert "backup_path" in data

    def test_get_backups(self, client, auth_headers):
        """バックアップ一覧取得のテスト"""
        # バックアップを作成
        client.post(
            "/api/backups/create",
            json={
                "backup_name": "テストバックアップ",
                "backup_type": "manual"
            },
            headers=auth_headers
        )

        # 一覧を取得
        response = client.get(
            "/api/backups",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) > 0

    def test_get_backup_detail(self, client, auth_headers):
        """バックアップ詳細取得のテスト"""
        # バックアップを作成
        create_response = client.post(
            "/api/backups/create",
            json={
                "backup_name": "テストバックアップ",
                "backup_type": "manual"
            },
            headers=auth_headers
        )
        backup_id = create_response.json()["id"]

        # 詳細を取得
        response = client.get(
            f"/api/backups/{backup_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == backup_id
        assert data["backup_name"] == "テストバックアップ"

    def test_get_backups_filter_by_type(self, client, auth_headers):
        """バックアップタイプでフィルタリングした一覧取得のテスト"""
        # 手動バックアップを作成
        client.post(
            "/api/backups/create",
            json={
                "backup_name": "手動バックアップ",
                "backup_type": "manual"
            },
            headers=auth_headers
        )

        # manualタイプでフィルタリング
        response = client.get(
            "/api/backups?backup_type=manual",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(item["backup_type"] == "manual" for item in data["items"])

    def test_restore_backup_requires_superuser(self, client, auth_headers):
        """バックアップ復元はスーパーユーザーのみのテスト"""
        # バックアップを作成
        create_response = client.post(
            "/api/backups/create",
            json={
                "backup_name": "テストバックアップ",
                "backup_type": "manual"
            },
            headers=auth_headers
        )
        backup_id = create_response.json()["id"]

        # 通常ユーザーで復元を試みる（403が返ることを期待）
        response = client.post(
            f"/api/backups/{backup_id}/restore",
            headers=auth_headers
        )
        # スーパーユーザーでない場合は403または401が返る
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_delete_backup_requires_superuser(self, client, auth_headers):
        """バックアップ削除はスーパーユーザーのみのテスト"""
        # バックアップを作成
        create_response = client.post(
            "/api/backups/create",
            json={
                "backup_name": "テストバックアップ",
                "backup_type": "manual"
            },
            headers=auth_headers
        )
        backup_id = create_response.json()["id"]

        # 通常ユーザーで削除を試みる（403が返ることを期待）
        response = client.delete(
            f"/api/backups/{backup_id}",
            headers=auth_headers
        )
        # スーパーユーザーでない場合は403または401が返る
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_get_backup_not_found(self, client, auth_headers):
        """存在しないバックアップの取得のテスト"""
        response = client.get(
            "/api/backups/99999",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_backups_unauthorized(self, client):
        """認証なしでのバックアップ一覧取得のテスト"""
        response = client.get("/api/backups")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
