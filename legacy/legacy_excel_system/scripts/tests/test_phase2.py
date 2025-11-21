#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2: 案件番号サーバーのテストコード

テスト項目:
1. サーバーの起動とヘルスチェック
2. 案件番号の生成
3. ステータスの取得
4. 同時リクエストでの重複防止
5. エラーハンドリング
"""

import pytest
import requests
import threading
import time
import sys
from pathlib import Path

# Phase2モジュールのインポート
# プロジェクトルートからの相対パスを設定
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / 'scripts' / 'phase2'))
from case_number_server import CaseNumberManager, CaseNumberServer


class TestCaseNumberManager:
    """
    CaseNumberManagerクラスのテスト
    """
    
    def test_initialization(self, tmp_path):
        """初期化テスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        assert manager.data is not None
        assert 'EX' in manager.data
        assert 'IM' in manager.data
        assert 'TR' in manager.data
        assert 'DO' in manager.data
        assert 'history' in manager.data
        assert manager.data['EX']['counter'] == 0
    
    def test_generate_case_number_ex(self, tmp_path):
        """輸出案件番号の生成テスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        result = manager.generate_case_number(case_type='EX', user='test_user')
        
        assert result['success'] is True
        assert result['case_number'] is not None
        assert result['case_number'].startswith('EX-')
        assert 'timestamp' in result
        
        # カウンターが増えていることを確認
        assert manager.data['EX']['counter'] == 1
    
    def test_generate_case_number_im(self, tmp_path):
        """輸入案件番号の生成テスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        result = manager.generate_case_number(case_type='IM', user='test_user')
        
        assert result['success'] is True
        assert result['case_number'].startswith('IM-')
        assert manager.data['IM']['counter'] == 1
    
    def test_generate_multiple_case_numbers(self, tmp_path):
        """複数の案件番号生成テスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        case_numbers = []
        for i in range(5):
            result = manager.generate_case_number(case_type='EX', user=f'user_{i}')
            assert result['success'] is True
            case_numbers.append(result['case_number'])
        
        # 重複がないことを確認
        assert len(case_numbers) == len(set(case_numbers))
        
        # カウンターが正しく増えていることを確認
        assert manager.data['EX']['counter'] == 5
    
    def test_invalid_case_type(self, tmp_path):
        """無効な案件種別のテスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        result = manager.generate_case_number(case_type='INVALID', user='test_user')
        
        assert result['success'] is False
        assert result['case_number'] is None
        assert 'message' in result
    
    def test_get_status(self, tmp_path):
        """ステータス取得テスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        # 何件か生成
        manager.generate_case_number(case_type='EX', user='user1')
        manager.generate_case_number(case_type='IM', user='user2')
        
        status = manager.get_status()
        
        assert status['success'] is True
        assert 'counters' in status
        assert status['counters']['EX']['counter'] == 1
        assert status['counters']['IM']['counter'] == 1
        assert 'history_count' in status
    
    def test_concurrent_generation(self, tmp_path):
        """同時生成テスト（スレッドセーフ確認）"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        case_numbers = []
        errors = []
        
        def generate_number(thread_id):
            try:
                result = manager.generate_case_number(case_type='EX', user=f'thread_{thread_id}')
                if result['success']:
                    case_numbers.append(result['case_number'])
                else:
                    errors.append(result['message'])
            except Exception as e:
                errors.append(str(e))
        
        # 10スレッドで同時に案件番号を生成
        threads = []
        for i in range(10):
            thread = threading.Thread(target=generate_number, args=(i,))
            threads.append(thread)
            thread.start()
        
        # 全スレッドの完了を待機
        for thread in threads:
            thread.join()
        
        # エラーがないことを確認
        assert len(errors) == 0, f"エラーが発生しました: {errors}"
        
        # 10個の案件番号が生成されたことを確認
        assert len(case_numbers) == 10
        
        # 重複がないことを確認
        assert len(case_numbers) == len(set(case_numbers)), \
            f"重複が検出されました: {case_numbers}"
        
        # カウンターが正しく増えていることを確認
        assert manager.data['EX']['counter'] == 10
    
    def test_history_limit(self, tmp_path):
        """履歴の上限テスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        # 150件生成（上限は100件）
        for i in range(150):
            manager.generate_case_number(case_type='EX', user=f'user_{i}')
        
        # 履歴が100件以下であることを確認
        assert len(manager.data['history']) <= 100
    
    def test_reset_counter(self, tmp_path):
        """カウンターリセットテスト"""
        data_file = tmp_path / "test_case_numbers.json"
        manager = CaseNumberManager(data_file=str(data_file))
        
        # 何件か生成
        manager.generate_case_number(case_type='EX', user='user1')
        manager.generate_case_number(case_type='EX', user='user2')
        
        assert manager.data['EX']['counter'] == 2
        
        # リセット
        result = manager.reset_counter(case_type='EX')
        
        assert result['success'] is True
        assert manager.data['EX']['counter'] == 0
        assert manager.data['EX']['last_generated'] is None
    
    def test_persistence(self, tmp_path):
        """データ永続化テスト"""
        data_file = tmp_path / "test_case_numbers.json"
        
        # 最初のマネージャーで案件番号を生成
        manager1 = CaseNumberManager(data_file=str(data_file))
        result1 = manager1.generate_case_number(case_type='EX', user='user1')
        case_number1 = result1['case_number']
        counter1 = manager1.data['EX']['counter']
        
        # 新しいマネージャーインスタンスを作成（ファイルから読み込み）
        manager2 = CaseNumberManager(data_file=str(data_file))
        
        # カウンターが引き継がれていることを確認
        assert manager2.data['EX']['counter'] == counter1
        
        # 次の案件番号を生成
        result2 = manager2.generate_case_number(case_type='EX', user='user2')
        case_number2 = result2['case_number']
        
        # 案件番号が連続していることを確認
        assert case_number1 != case_number2
        assert manager2.data['EX']['counter'] == counter1 + 1


@pytest.mark.integration
class TestCaseNumberServerIntegration:
    """
    サーバー統合テスト
    
    注意: これらのテストを実行する前に、サーバーが起動している必要があります。
          手動テスト用のテストケースです。
    """
    
    BASE_URL = "http://localhost:8080"
    
    @pytest.fixture(scope="class")
    def server_url(self):
        """サーバーURLのフィクスチャ"""
        return self.BASE_URL
    
    def test_health_check(self, server_url):
        """ヘルスチェックテスト"""
        try:
            response = requests.get(f"{server_url}/health", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert data['success'] is True
            assert data['status'] == 'healthy'
        except requests.exceptions.ConnectionError:
            pytest.skip("サーバーが起動していません")
    
    def test_generate_via_http(self, server_url):
        """HTTP経由の案件番号生成テスト"""
        try:
            response = requests.get(
                f"{server_url}/generate",
                params={'type': 'EX', 'user': 'test'},
                timeout=5
            )
            assert response.status_code == 200
            
            data = response.json()
            assert data['success'] is True
            assert 'case_number' in data
            assert data['case_number'].startswith('EX-')
        except requests.exceptions.ConnectionError:
            pytest.skip("サーバーが起動していません")
    
    def test_status_via_http(self, server_url):
        """HTTP経由のステータス取得テスト"""
        try:
            response = requests.get(f"{server_url}/status", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert data['success'] is True
            assert 'counters' in data
        except requests.exceptions.ConnectionError:
            pytest.skip("サーバーが起動していません")
    
    def test_concurrent_http_requests(self, server_url):
        """同時HTTPリクエストテスト"""
        try:
            case_numbers = []
            errors = []
            
            def make_request(thread_id):
                try:
                    response = requests.get(
                        f"{server_url}/generate",
                        params={'type': 'EX', 'user': f'thread_{thread_id}'},
                        timeout=5
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data['success']:
                            case_numbers.append(data['case_number'])
                except Exception as e:
                    errors.append(str(e))
            
            # 10スレッドで同時にリクエスト
            threads = []
            for i in range(10):
                thread = threading.Thread(target=make_request, args=(i,))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
            
            assert len(errors) == 0, f"エラーが発生しました: {errors}"
            assert len(case_numbers) == 10
            assert len(case_numbers) == len(set(case_numbers)), \
                f"重複が検出されました: {case_numbers}"
        
        except requests.exceptions.ConnectionError:
            pytest.skip("サーバーが起動していません")


def run_tests():
    """
    テストを実行
    """
    print("=" * 60)
    print("Phase 2: 案件番号サーバー テスト")
    print("=" * 60)
    print()
    
    # 単体テストを実行
    print("[1] 単体テスト（サーバー不要）")
    pytest.main([__file__, '-v', '-m', 'not integration'])
    
    print()
    print("=" * 60)
    print("[2] 統合テスト（サーバー起動が必要）")
    print("サーバーを起動してから、以下のコマンドを実行してください:")
    print(f"  pytest {__file__} -v -m integration")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()

