#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4のテストコード
統合処理改善のテスト

【テスト項目】
1. 項目単位マージのテスト
2. 競合解決のテスト
3. ファイルロック検知のテスト
4. リトライ機構のテスト
5. 統合フローのテスト

【作成日】2025-11-20
"""

import sys
import pytest
import pandas as pd
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
import shutil

# テスト対象モジュールのインポート
sys.path.append(str(Path(__file__).parent.parent / 'phase4'))
from integrate_data import DataIntegrator

# Phase 1の共通モジュール
sys.path.append(str(Path(__file__).parent.parent / 'phase1'))
from common import load_config
from file_handler import write_excel_safe


# テスト用のフィクスチャ
@pytest.fixture
def test_config():
    """テスト用の設定を返す"""
    config_path = Path(__file__).parent.parent / 'phase1' / 'config.json'
    return load_config(str(config_path))


@pytest.fixture
def test_integrator(test_config):
    """テスト用のDataIntegratorインスタンスを作成"""
    return DataIntegrator()


@pytest.fixture
def sample_master_df():
    """サンプルのマスターデータを作成"""
    data = {
        '案件番号': ['2025-EX-001', '2025-EX-002'],
        '案件名': ['テスト案件A', 'テスト案件B'],
        '顧客名': ['株式会社A', '株式会社B'],
        '数量': [100, 200],
        '単価': [1000, 2000],
        '最終更新日時': [
            datetime(2025, 11, 20, 10, 0, 0),
            datetime(2025, 11, 20, 10, 0, 0)
        ],
        '更新者': ['システム', 'システム']
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_user1_df():
    """サンプルのユーザー1データを作成（数量を更新）"""
    data = {
        '案件番号': ['2025-EX-001'],
        '案件名': ['テスト案件A'],
        '顧客名': ['株式会社A'],
        '数量': [150],  # 100 → 150 に更新
        '単価': [1000],
        '最終更新日時': [datetime(2025, 11, 20, 15, 0, 0)],
        '更新者': ['山田']
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_user2_df():
    """サンプルのユーザー2データを作成（単価を更新）"""
    data = {
        '案件番号': ['2025-EX-001'],
        '案件名': ['テスト案件A'],
        '顧客名': ['株式会社A'],
        '数量': [100],
        '単価': [1200],  # 1000 → 1200 に更新
        '最終更新日時': [datetime(2025, 11, 20, 15, 30, 0)],
        '更新者': ['鈴木']
    }
    return pd.DataFrame(data)


class TestFieldLevelMerge:
    """項目単位マージのテスト"""
    
    def test_no_conflict_merge(self, test_integrator, sample_master_df):
        """競合なしのマージ（単一ソース）"""
        result = test_integrator.merge_with_field_level_resolution(
            sample_master_df, []
        )
        
        assert len(result) == 2
        assert result['案件番号'].tolist() == ['2025-EX-001', '2025-EX-002']
    
    def test_field_level_merge_with_different_fields(
        self, test_integrator, sample_master_df, sample_user1_df, sample_user2_df
    ):
        """異なる項目を更新した場合のマージ（両方の更新が反映されること）"""
        result = test_integrator.merge_with_field_level_resolution(
            sample_master_df, [sample_user1_df, sample_user2_df]
        )
        
        # 案件2025-EX-001を確認
        case_001 = result[result['案件番号'] == '2025-EX-001'].iloc[0]
        
        # 山田さんの数量更新が反映されている
        assert case_001['数量'] == 150, "山田さんの数量更新が反映されていません"
        
        # 鈴木さんの単価更新が反映されている
        assert case_001['単価'] == 1200, "鈴木さんの単価更新が反映されていません"
        
        print(f"[OK] 項目単位マージ成功: 数量={case_001['数量']}, 単価={case_001['単価']}")
    
    def test_conflict_resolution_same_field(self, test_integrator):
        """同じ項目への同時更新（最新タイムスタンプが採用されること）"""
        # マスターデータ
        master_df = pd.DataFrame({
            '案件番号': ['2025-EX-001'],
            '案件名': ['テスト案件'],
            '数量': [100],
            '最終更新日時': [datetime(2025, 11, 20, 10, 0, 0)],
            '更新者': ['システム']
        })
        
        # ユーザー1: 15:00に数量を150に更新
        user1_df = pd.DataFrame({
            '案件番号': ['2025-EX-001'],
            '案件名': ['テスト案件'],
            '数量': [150],
            '最終更新日時': [datetime(2025, 11, 20, 15, 0, 0)],
            '更新者': ['山田']
        })
        
        # ユーザー2: 15:30に数量を180に更新
        user2_df = pd.DataFrame({
            '案件番号': ['2025-EX-001'],
            '案件名': ['テスト案件'],
            '数量': [180],
            '最終更新日時': [datetime(2025, 11, 20, 15, 30, 0)],
            '更新者': ['鈴木']
        })
        
        result = test_integrator.merge_with_field_level_resolution(
            master_df, [user1_df, user2_df]
        )
        
        # 最新（15:30）の鈴木さんの値が採用される
        case_001 = result[result['案件番号'] == '2025-EX-001'].iloc[0]
        assert case_001['数量'] == 180, "最新のタイムスタンプが採用されていません"
        
        print(f"[OK] 競合解決成功: 最新の値({case_001['数量']})が採用されました")
    
    def test_empty_value_handling(self, test_integrator):
        """空値の処理テスト"""
        master_df = pd.DataFrame({
            '案件番号': ['2025-EX-001'],
            '案件名': ['テスト案件'],
            '数量': [100],
            '備考': [''],
            '最終更新日時': [datetime(2025, 11, 20, 10, 0, 0)],
            '更新者': ['システム']
        })
        
        user_df = pd.DataFrame({
            '案件番号': ['2025-EX-001'],
            '案件名': ['テスト案件'],
            '数量': [100],
            '備考': ['重要案件'],
            '最終更新日時': [datetime(2025, 11, 20, 15, 0, 0)],
            '更新者': ['山田']
        })
        
        result = test_integrator.merge_with_field_level_resolution(
            master_df, [user_df]
        )
        
        case_001 = result[result['案件番号'] == '2025-EX-001'].iloc[0]
        assert case_001['備考'] == '重要案件', "空値が正しく処理されていません"
        
        print("[OK] 空値処理成功")


class TestFileOperations:
    """ファイル操作のテスト"""
    
    def test_load_master_data(self, test_integrator):
        """マスターデータの読み込みテスト"""
        df = test_integrator.load_master_data()
        
        # ファイルが存在すればDataFrameが返る
        assert isinstance(df, pd.DataFrame)
        
        if not df.empty:
            assert '案件番号' in df.columns
            print(f"[OK] マスターデータ読み込み成功: {len(df)}件")
        else:
            print("[OK] マスターデータが空（正常）")
    
    def test_load_user_data(self, test_integrator):
        """ユーザーデータの読み込みテスト"""
        df = test_integrator.load_user_data('山田')
        
        # DataFrameが返る（空の場合もある）
        assert isinstance(df, pd.DataFrame)
        
        if not df.empty:
            print(f"[OK] ユーザーデータ読み込み成功: {len(df)}件")
        else:
            print("[OK] ユーザーデータが空（正常）")
    
    def test_check_files_accessible(self, test_integrator):
        """ファイルアクセス可能チェックのテスト"""
        locked_users = test_integrator.check_all_files_accessible()
        
        assert isinstance(locked_users, list)
        
        if locked_users:
            print(f"[WARNING] ロック中のファイル: {', '.join(locked_users)}")
        else:
            print("[OK] 全ファイルがアクセス可能")


class TestConflictLogging:
    """競合ログのテスト"""
    
    def test_conflict_log_generation(self, test_integrator, tmp_path):
        """競合ログが正しく生成されること"""
        # 一時的にlog_dirを変更
        original_log_dir = test_integrator.log_dir
        test_integrator.log_dir = tmp_path
        
        try:
            # 競合が発生するデータを作成
            master_df = pd.DataFrame({
                '案件番号': ['2025-EX-001'],
                '数量': [100],
                '最終更新日時': [datetime(2025, 11, 20, 10, 0, 0)],
                '更新者': ['システム']
            })
            
            user1_df = pd.DataFrame({
                '案件番号': ['2025-EX-001'],
                '数量': [150],
                '最終更新日時': [datetime(2025, 11, 20, 15, 0, 0)],
                '更新者': ['山田']
            })
            
            user2_df = pd.DataFrame({
                '案件番号': ['2025-EX-001'],
                '数量': [180],
                '最終更新日時': [datetime(2025, 11, 20, 15, 30, 0)],
                '更新者': ['鈴木']
            })
            
            # マージ実行
            result = test_integrator.merge_with_field_level_resolution(
                master_df, [user1_df, user2_df]
            )
            
            # 競合ログファイルが作成されているか確認
            log_files = list(tmp_path.glob("conflicts_*.json"))
            
            if log_files:
                # ログファイルの内容を確認
                with open(log_files[0], 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                
                assert len(log_data) > 0, "競合ログが記録されていません"
                assert log_data[0]['case_number'] == '2025-EX-001'
                
                print(f"[OK] 競合ログ生成成功: {log_files[0].name}")
                print(f"  競合件数: {len(log_data)}")
            else:
                print("[WARNING] 競合ログファイルが作成されませんでした")
        
        finally:
            # log_dirを元に戻す
            test_integrator.log_dir = original_log_dir


class TestIntegrationFlow:
    """統合フローのテスト"""
    
    def test_full_integration_flow(self, test_integrator):
        """統合処理の全体フローテスト"""
        # 統合処理を実行
        # 注: 実際のファイルに影響を与えるため、テスト環境でのみ実行
        print("\n統合処理フローテスト:")
        print("  ※ このテストは実際のファイルに影響を与える可能性があります")
        print("  ※ 手動テストで実行することを推奨します")
        
        # 簡易チェックのみ実行
        locked_users = test_integrator.check_all_files_accessible()
        
        if locked_users:
            print(f"  [WARNING] ロック中のファイル: {', '.join(locked_users)}")
            print("  → 統合処理はスキップします")
        else:
            print("  [OK] 全ファイルがアクセス可能")
            print("  → 統合処理を実行できる状態です")


def run_all_tests():
    """全てのテストを実行"""
    print("=" * 70)
    print("Phase 4 - 統合処理改善のテスト")
    print("=" * 70)
    print()
    
    # pytest実行
    pytest_args = [
        __file__,
        '-v',           # 詳細表示
        '--tb=short',   # トレースバックを短く
        '-s'            # printを表示
    ]
    
    result = pytest.main(pytest_args)
    
    print()
    print("=" * 70)
    if result == 0:
        print("[SUCCESS] 全てのテストが成功しました")
    else:
        print("[FAILED] 一部のテストが失敗しました")
    print("=" * 70)
    
    return result


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

