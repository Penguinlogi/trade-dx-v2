"""
案件番号生成APIのテスト
"""
import pytest
from fastapi import status
from app.models.case_number import CaseNumber
from datetime import datetime


@pytest.mark.unit
class TestCaseNumbers:
    """案件番号生成エンドポイントのテスト"""

    def test_generate_case_number_import(self, client, auth_headers):
        """輸入案件番号生成のテスト"""
        response = client.post(
            "/api/case-numbers/generate",
            json={
                "trade_type": "輸入"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "case_number" in data
        assert data["trade_type"] == "輸入"
        assert data["trade_type_code"] == "IM"
        assert data["year"] == datetime.now().year
        assert data["sequence"] == 1
        assert "IM" in data["case_number"]

    def test_generate_case_number_export(self, client, auth_headers):
        """輸出案件番号生成のテスト"""
        response = client.post(
            "/api/case-numbers/generate",
            json={
                "trade_type": "輸出"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "case_number" in data
        assert data["trade_type"] == "輸出"
        assert data["trade_type_code"] == "EX"
        assert "EX" in data["case_number"]

    def test_generate_case_number_sequential(self, client, auth_headers):
        """連続した案件番号生成のテスト"""
        # 1回目
        response1 = client.post(
            "/api/case-numbers/generate",
            json={
                "trade_type": "輸入"
            },
            headers=auth_headers
        )
        assert response1.status_code == status.HTTP_200_OK
        data1 = response1.json()
        sequence1 = data1["sequence"]

        # 2回目
        response2 = client.post(
            "/api/case-numbers/generate",
            json={
                "trade_type": "輸入"
            },
            headers=auth_headers
        )
        assert response2.status_code == status.HTTP_200_OK
        data2 = response2.json()
        sequence2 = data2["sequence"]

        # 連番がインクリメントされていることを確認
        assert sequence2 == sequence1 + 1
        assert data1["case_number"] != data2["case_number"]

    def test_get_current_sequence(self, client, auth_headers):
        """現在の連番取得のテスト"""
        # 案件番号を生成
        client.post(
            "/api/case-numbers/generate",
            json={
                "trade_type": "輸入"
            },
            headers=auth_headers
        )

        # 現在の連番を取得
        response = client.get(
            "/api/case-numbers/current/輸入",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "year" in data
        assert "trade_type" in data
        assert "last_sequence" in data
        assert data["last_sequence"] >= 1

    def test_get_current_sequence_no_record(self, client, auth_headers):
        """レコードが存在しない場合の現在の連番取得のテスト"""
        # 新しい年でテストするため、存在しない区分を指定
        response = client.get(
            "/api/case-numbers/current/輸出",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["last_sequence"] == 0

    def test_generate_case_number_invalid_trade_type(self, client, auth_headers):
        """無効な取引タイプでの案件番号生成のテスト"""
        response = client.post(
            "/api/case-numbers/generate",
            json={
                "trade_type": "無効なタイプ"
            },
            headers=auth_headers
        )
        # バリデーションエラーが返ることを期待（422 Unprocessable Entity）
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_generate_case_number_unauthorized(self, client):
        """認証なしでの案件番号生成のテスト"""
        response = client.post(
            "/api/case-numbers/generate",
            json={
                "trade_type": "輸入"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
