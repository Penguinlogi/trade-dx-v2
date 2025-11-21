#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 単体テスト (test_phase1.py)

Phase 1で実装した基盤機能のテストを実施します。
- common.py の各関数
- file_handler.py の各関数
"""

import pytest
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# Phase 1モジュールをインポート
sys.path.append(str(Path(__file__).parent.parent / "phase1"))
from common import (
    load_config,
    setup_logger,
    get_file_path,
    error_handler,
    get_timestamp,
    validate_config
)
from file_handler import (
    check_file_locked,
    read_excel_safe,
    write_excel_safe,
    create_backup_file,
    cleanup_old_backups,
    get_file_info
)


class TestCommonModule:
    """common.py のテスト"""
    
    def test_load_config(self):
        """設定ファイル読み込みテスト"""
        print("\n=== test_load_config ===")
        
        # 設定ファイルを読み込み
        config_path = Path(__file__).parent.parent / "phase1" / "config.json"
        config = load_config(str(config_path))
        
        # 基本的な検証
        assert config is not None, "設定が読み込めませんでした"
        assert 'version' in config, "versionが見つかりません"
        assert config['version'] == '2.1', "バージョンが一致しません"
        assert 'paths' in config, "pathsが見つかりません"
        assert 'users' in config, "usersが見つかりません"
        
        print(f"[OK] 設定ファイル読み込み成功")
        print(f"   バージョン: {config['version']}")
        print(f"   ユーザー数: {len(config['users'])}")
    
    def test_setup_logger(self):
        """ロガーセットアップテスト"""
        print("\n=== test_setup_logger ===")
        
        # ロガーを作成
        logger = setup_logger("test_logger", log_dir="../../logs")
        
        # 基本的な検証
        assert logger is not None, "ロガーが作成できませんでした"
        assert logger.name == "test_logger", "ロガー名が一致しません"
        assert len(logger.handlers) >= 2, "ハンドラーが不足しています"
        
        # テストログ出力
        logger.info("テストログメッセージ")
        logger.debug("デバッグメッセージ")
        logger.warning("警告メッセージ")
        
        print(f"[OK] ロガーセットアップ成功")
        print(f"   ロガー名: {logger.name}")
        print(f"   ハンドラー数: {len(logger.handlers)}")
    
    def test_get_file_path(self):
        """ファイルパス生成テスト"""
        print("\n=== test_get_file_path ===")
        
        config_path = Path(__file__).parent.parent / "phase1" / "config.json"
        config = load_config(str(config_path))
        
        # マスターファイルパス
        master_path = get_file_path('master', config)
        assert master_path is not None, "マスターパスが生成できませんでした"
        assert 'master' in str(master_path), "masterが含まれていません"
        print(f"   マスターパス: {master_path}")
        
        # 作業ファイルパス（山田さん）
        work_path = get_file_path('work', config, user_name='山田')
        assert work_path is not None, "作業パスが生成できませんでした"
        assert 'work' in str(work_path), "workが含まれていません"
        assert 'yamada' in str(work_path), "yamadaが含まれていません"
        print(f"   作業ファイルパス: {work_path}")
        
        # バックアップファイルパス
        backup_path = get_file_path('backup', config)
        assert backup_path is not None, "バックアップパスが生成できませんでした"
        assert 'backup' in str(backup_path), "backupが含まれていません"
        print(f"   バックアップパス: {backup_path}")
        
        print(f"[OK] ファイルパス生成成功")
    
    def test_error_handler_decorator(self):
        """エラーハンドリングデコレータテスト"""
        print("\n=== test_error_handler_decorator ===")
        
        @error_handler()
        def test_function_success():
            return "成功"
        
        @error_handler()
        def test_function_error():
            raise ValueError("テストエラー")
        
        # 正常系
        result = test_function_success()
        assert result == "成功", "正常系の結果が一致しません"
        print(f"   正常系: {result}")
        
        # 異常系
        try:
            test_function_error()
            assert False, "例外が発生しませんでした"
        except ValueError as e:
            assert "テストエラー" in str(e), "エラーメッセージが一致しません"
            print(f"   異常系: エラーを正しくキャッチ")
        
        print(f"[OK] エラーハンドリングデコレータ成功")
    
    def test_get_timestamp(self):
        """タイムスタンプ取得テスト"""
        print("\n=== test_get_timestamp ===")
        
        timestamp = get_timestamp()
        assert timestamp is not None, "タイムスタンプが取得できませんでした"
        assert len(timestamp) > 0, "タイムスタンプが空です"
        
        # フォーマットのテスト
        custom_format = get_timestamp("%Y%m%d")
        assert len(custom_format) == 8, "カスタムフォーマットが機能していません"
        
        print(f"   デフォルト: {timestamp}")
        print(f"   カスタム: {custom_format}")
        print(f"[OK] タイムスタンプ取得成功")
    
    def test_validate_config(self):
        """設定検証テスト"""
        print("\n=== test_validate_config ===")
        
        config_path = Path(__file__).parent.parent / "phase1" / "config.json"
        config = load_config(str(config_path))
        
        # 正常な設定の検証
        try:
            result = validate_config(config)
            assert result == True, "設定検証が失敗しました"
            print(f"   正常な設定: 検証成功")
        except ValueError as e:
            assert False, f"正常な設定で例外が発生: {e}"
        
        # 異常な設定の検証
        invalid_config = {'version': '2.1'}  # pathsとusersが不足
        try:
            validate_config(invalid_config)
            assert False, "不正な設定で例外が発生しませんでした"
        except ValueError as e:
            print(f"   不正な設定: エラー検出 ({e})")
        
        print(f"[OK] 設定検証成功")


class TestFileHandlerModule:
    """file_handler.py のテスト"""
    
    @pytest.fixture
    def test_dir(self):
        """テスト用ディレクトリの準備"""
        test_path = Path("../../test_output")
        test_path.mkdir(parents=True, exist_ok=True)
        return test_path
    
    @pytest.fixture
    def sample_data(self):
        """サンプルデータの準備"""
        return pd.DataFrame({
            '案件番号': ['TEST-001', 'TEST-002', 'TEST-003'],
            '顧客名': ['テストA社', 'テストB社', 'テストC社'],
            '数量': [100, 200, 150],
            '単価': [1000, 1500, 1200],
            '金額': [100000, 300000, 180000]
        })
    
    def test_write_and_read_excel(self, test_dir, sample_data):
        """Excelファイル読み書きテスト"""
        print("\n=== test_write_and_read_excel ===")
        
        test_file = test_dir / "test_readwrite.xlsx"
        
        # 書き込みテスト
        success = write_excel_safe(
            sample_data,
            test_file,
            sheet_name="テストシート",
            create_backup=False
        )
        assert success == True, "書き込みが失敗しました"
        assert test_file.exists(), "ファイルが作成されていません"
        print(f"   [OK] 書き込み成功: {test_file.name}")
        
        # 読み込みテスト
        df = read_excel_safe(test_file, sheet_name="テストシート")
        assert df is not None, "読み込みが失敗しました"
        assert len(df) == len(sample_data), "行数が一致しません"
        assert len(df.columns) == len(sample_data.columns), "列数が一致しません"
        print(f"   [OK] 読み込み成功: {len(df)}行 × {len(df.columns)}列")
        
        # データの一致確認
        assert df['案件番号'].tolist() == sample_data['案件番号'].tolist(), "データが一致しません"
        print(f"   [OK] データ一致確認: OK")
    
    def test_file_lock_detection(self, test_dir, sample_data):
        """ファイルロック検知テスト"""
        print("\n=== test_file_lock_detection ===")
        
        test_file = test_dir / "test_lock.xlsx"
        
        # ファイルを作成
        write_excel_safe(sample_data, test_file, create_backup=False)
        
        # ロックされていない状態をテスト
        is_locked = check_file_locked(test_file, timeout=1)
        assert is_locked == False, "ファイルがロックされていると誤検出されました"
        print(f"   [OK] ロックなし: 正しく検出")
        
        # 存在しないファイルのテスト
        non_existent = test_dir / "non_existent.xlsx"
        is_locked = check_file_locked(non_existent, timeout=1)
        assert is_locked == False, "存在しないファイルでエラー"
        print(f"   [OK] 存在しないファイル: 正しく処理")
    
    def test_create_backup(self, test_dir, sample_data):
        """バックアップ作成テスト"""
        print("\n=== test_create_backup ===")
        
        test_file = test_dir / "test_backup_source.xlsx"
        
        # 元ファイルを作成
        write_excel_safe(sample_data, test_file, create_backup=False)
        
        # バックアップを作成
        backup_path = create_backup_file(test_file, test_dir)
        assert backup_path is not None, "バックアップ作成が失敗しました"
        assert backup_path.exists(), "バックアップファイルが存在しません"
        assert 'backup' in backup_path.name, "バックアップ名が不正です"
        print(f"   [OK] バックアップ作成成功: {backup_path.name}")
        
        # バックアップの内容確認
        df_backup = read_excel_safe(backup_path)
        assert df_backup is not None, "バックアップが読み込めません"
        assert len(df_backup) == len(sample_data), "バックアップの行数が一致しません"
        print(f"   [OK] バックアップ内容確認: OK")
    
    def test_cleanup_old_backups(self, test_dir, sample_data):
        """古いバックアップ削除テスト"""
        print("\n=== test_cleanup_old_backups ===")
        
        # テスト用の古いバックアップファイルを作成
        old_backup1 = test_dir / "test_backup_20231101_120000.xlsx"
        old_backup2 = test_dir / "test_backup_20231102_120000.xlsx"
        recent_backup = test_dir / f"test_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # ファイルを作成
        for backup_file in [old_backup1, old_backup2, recent_backup]:
            write_excel_safe(sample_data, backup_file, create_backup=False)
        
        # 古いファイルのタイムスタンプを変更（31日前）
        old_time = time.time() - (31 * 24 * 60 * 60)
        for old_file in [old_backup1, old_backup2]:
            if old_file.exists():
                import os
                os.utime(old_file, (old_time, old_time))
        
        # クリーンアップ実行
        deleted_count = cleanup_old_backups(test_dir, retention_days=30, file_pattern="test_backup_*")
        
        # 検証
        assert deleted_count >= 0, "削除処理でエラーが発生しました"
        assert not old_backup1.exists() or not old_backup2.exists(), "古いバックアップが削除されていません"
        assert recent_backup.exists(), "最新のバックアップが誤って削除されました"
        print(f"   [OK] クリーンアップ成功: {deleted_count}件削除")
    
    def test_get_file_info(self, test_dir, sample_data):
        """ファイル情報取得テスト"""
        print("\n=== test_get_file_info ===")
        
        test_file = test_dir / "test_info.xlsx"
        
        # ファイルを作成
        write_excel_safe(sample_data, test_file, create_backup=False)
        
        # ファイル情報を取得
        info = get_file_info(test_file)
        assert info is not None, "ファイル情報が取得できませんでした"
        assert info['exists'] == True, "ファイルが存在しません"
        assert 'size_bytes' in info, "サイズ情報がありません"
        assert 'modified_time' in info, "更新日時情報がありません"
        
        print(f"   ファイル名: {info['name']}")
        print(f"   サイズ: {info['size_mb']:.4f} MB")
        print(f"   更新日時: {info['modified_time']}")
        print(f"   [OK] ファイル情報取得成功")


def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 60)
    print("Phase 1 単体テスト開始")
    print("=" * 60)
    
    # pytestを実行
    exit_code = pytest.main([
        __file__,
        "-v",  # 詳細表示
        "-s",  # print文を表示
        "--tb=short",  # トレースバック短縮
    ])
    
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("[SUCCESS] すべてのテストが成功しました")
    else:
        print(f"[FAILED] テストが失敗しました（終了コード: {exit_code}）")
    print("=" * 60)
    
    return exit_code


if __name__ == "__main__":
    # テストを実行
    exit_code = run_all_tests()
    sys.exit(exit_code)

