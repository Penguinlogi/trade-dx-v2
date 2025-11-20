#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3のテストコード
差分同期機能のテスト
"""

import sys
from pathlib import Path
import pytest
import pandas as pd
from datetime import datetime
import shutil

# Phase3のモジュールをインポート
sys.path.append(str(Path(__file__).parent.parent / 'phase3'))
sys.path.append(str(Path(__file__).parent.parent / 'phase1'))

from incremental_sync import IncrementalSync


class TestIncrementalSync:
    """差分同期機能のテストクラス"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmp_path):
        """テスト前後の処理"""
        # テスト用ディレクトリの作成
        self.test_dir = tmp_path / "test_sync"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        self.master_dir = self.test_dir / "master"
        self.work_dir = self.test_dir / "work"
        self.backup_dir = self.test_dir / "backup"
        self.log_dir = self.test_dir / "logs"
        
        for d in [self.master_dir, self.work_dir, self.backup_dir, self.log_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # テスト用設定ファイルの作成
        self.config_file = self.test_dir / "test_config.json"
        self._create_test_config()
        
        # テスト用データの作成
        self._create_test_data()
        
        yield
        
        # テスト後のクリーンアップは不要（tmp_pathが自動削除される）
    
    def _create_test_config(self):
        """テスト用設定ファイルを作成"""
        import json
        
        config = {
            "version": "2.1",
            "paths": {
                "master_dir": str(self.master_dir),
                "work_dir": str(self.work_dir),
                "backup_dir": str(self.backup_dir),
                "log_dir": str(self.log_dir)
            },
            "file_settings": {
                "master_file_name": "案件管理台帳_マスター.xlsm"
            },
            "users": [
                {
                    "name": "山田",
                    "file_prefix": "yamada"
                },
                {
                    "name": "鈴木",
                    "file_prefix": "suzuki"
                }
            ],
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(levelname)s - %(message)s"
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def _create_test_data(self):
        """テスト用データを作成"""
        # マスターファイル（既存データ）
        master_data = pd.DataFrame({
            '案件番号': ['2025-EX-001', '2025-EX-002'],
            '顧客名': ['A社', 'B社'],
            '数量': [100, 200],
            '単価': [1000, 1500],
            '最終更新日時': [
                datetime(2025, 11, 1, 10, 0, 0),
                datetime(2025, 11, 2, 10, 0, 0)
            ]
        })
        
        master_file = self.master_dir / "案件管理台帳_マスター.xlsm"
        master_data.to_excel(master_file, sheet_name='案件一覧', index=False, engine='openpyxl')
        
        # 山田さんの個人ファイル（未同期データあり）
        yamada_data = pd.DataFrame({
            '案件番号': ['2025-EX-001', '2025-EX-003'],
            '顧客名': ['A社', 'C社'],
            '数量': [150, 300],  # 2025-EX-001は更新
            '単価': [1000, 2000],
            '最終更新日時': [
                datetime(2025, 11, 3, 10, 0, 0),
                datetime(2025, 11, 3, 11, 0, 0)
            ],
            '_同期済み': [False, False]  # 両方未同期
        })
        
        # ファイル名を設定に合わせる（master_file_nameがベースになる）
        yamada_file = self.work_dir / "案件管理台帳_マスター_yamada.xlsm"
        yamada_data.to_excel(yamada_file, sheet_name='案件一覧', index=False, engine='openpyxl')
        
        # 鈴木さんの個人ファイル（同期済みのみ）
        suzuki_data = pd.DataFrame({
            '案件番号': ['2025-EX-002'],
            '顧客名': ['B社'],
            '数量': [200],
            '単価': [1500],
            '最終更新日時': [
                datetime(2025, 11, 2, 10, 0, 0)
            ],
            '_同期済み': [True]  # すでに同期済み
        })
        
        # ファイル名を設定に合わせる
        suzuki_file = self.work_dir / "案件管理台帳_マスター_suzuki.xlsm"
        suzuki_data.to_excel(suzuki_file, sheet_name='案件一覧', index=False, engine='openpyxl')
    
    def test_initialization(self):
        """初期化テスト"""
        syncer = IncrementalSync(str(self.config_file))
        
        assert syncer is not None
        assert syncer.master_file.name == "案件管理台帳_マスター.xlsm"
        assert syncer.SYNC_FLAG_COL == '_同期済み'
        assert syncer.SYNC_TIME_COL == '_同期日時'
        print("✅ 初期化テスト成功")
    
    def test_get_unsynced_data(self):
        """未同期データ取得テスト"""
        syncer = IncrementalSync(str(self.config_file))
        
        # 山田さんのデータ（未同期あり）
        yamada_unsynced = syncer.get_unsynced_data('山田')
        assert not yamada_unsynced.empty
        assert len(yamada_unsynced) == 2  # 2件の未同期データ
        assert '2025-EX-001' in yamada_unsynced['案件番号'].values
        assert '2025-EX-003' in yamada_unsynced['案件番号'].values
        print(f"✅ 山田さんの未同期データ: {len(yamada_unsynced)}件")
        
        # 鈴木さんのデータ（未同期なし）
        suzuki_unsynced = syncer.get_unsynced_data('鈴木')
        assert suzuki_unsynced.empty  # 同期済みなのでデータなし
        print(f"✅ 鈴木さんの未同期データ: {len(suzuki_unsynced)}件（同期済み）")
    
    def test_update_master(self):
        """マスター更新テスト"""
        syncer = IncrementalSync(str(self.config_file))
        
        # 未同期データを取得
        yamada_unsynced = syncer.get_unsynced_data('山田')
        
        # マスター更新
        update_count = syncer.update_master([yamada_unsynced])
        
        assert update_count == 2  # 更新1件、新規1件
        print(f"✅ マスター更新: {update_count}件")
        
        # マスターファイルを読み込んで確認
        master_df = pd.read_excel(
            syncer.master_file,
            sheet_name='案件一覧',
            engine='openpyxl'
        )
        
        assert len(master_df) == 3  # 元の2件 + 新規1件
        assert '2025-EX-003' in master_df['案件番号'].values
        
        # 更新された案件の数量を確認
        ex001_row = master_df[master_df['案件番号'] == '2025-EX-001']
        assert ex001_row['数量'].values[0] == 150  # 100 → 150に更新
        print("✅ マスターファイルの内容確認OK")
    
    def test_mark_as_synced(self):
        """同期フラグ更新テスト"""
        syncer = IncrementalSync(str(self.config_file))
        
        # 同期フラグを更新
        case_numbers = ['2025-EX-001', '2025-EX-003']
        result = syncer.mark_as_synced('山田', case_numbers)
        
        assert result is True
        print("✅ 同期フラグ更新成功")
        
        # 個人ファイルを読み込んで確認
        yamada_file = self.work_dir / "案件管理台帳_マスター_yamada.xlsm"
        yamada_df = pd.read_excel(
            yamada_file,
            sheet_name='案件一覧',
            engine='openpyxl'
        )
        
        # すべて同期済みになっているはず
        assert yamada_df['_同期済み'].all()
        assert yamada_df['_同期日時'].notna().all()
        print("✅ 個人ファイルの同期フラグ確認OK")
    
    def test_full_sync_flow(self):
        """全体フローテスト"""
        syncer = IncrementalSync(str(self.config_file))
        
        # 差分同期を実行
        result = syncer.sync_all()
        
        assert result['status'] in ['success', 'no_update']
        assert result['synced'] == 2  # 2件同期
        assert result['users'] == 1  # 1ユーザー（山田さんのみ）
        print(f"✅ 全体フロー成功: {result}")
        
        # マスターファイルを確認
        master_df = pd.read_excel(
            syncer.master_file,
            sheet_name='案件一覧',
            engine='openpyxl'
        )
        assert len(master_df) == 3  # 元の2件 + 新規1件
        print(f"✅ マスター件数: {len(master_df)}件")
        
        # 個人ファイルの同期フラグを確認
        yamada_file = self.work_dir / "案件管理台帳_マスター_yamada.xlsm"
        yamada_df = pd.read_excel(
            yamada_file,
            sheet_name='案件一覧',
            engine='openpyxl'
        )
        assert yamada_df['_同期済み'].all()
        print("✅ 個人ファイルの同期フラグ確認OK")
        
        # 2回目の実行（重複しないことを確認）
        result2 = syncer.sync_all()
        assert result2['synced'] == 0  # 同期対象なし
        assert result2['status'] == 'no_data'
        print("✅ 2回目の実行で重複なし")
    
    def test_empty_master(self):
        """マスターが空の場合のテスト"""
        # マスターファイルを削除
        master_file = self.master_dir / "案件管理台帳_マスター.xlsm"
        if master_file.exists():
            master_file.unlink()
        
        syncer = IncrementalSync(str(self.config_file))
        
        # 差分同期を実行
        result = syncer.sync_all()
        
        assert result['status'] == 'success'
        assert result['synced'] > 0
        print(f"✅ 空マスターからの同期成功: {result['synced']}件")
    
    def test_no_sync_flag_column(self):
        """同期フラグ列がない場合のテスト"""
        # 同期フラグ列なしのファイルを作成
        test_data = pd.DataFrame({
            '案件番号': ['2025-EX-999'],
            '顧客名': ['テスト社'],
            '数量': [999],
            '単価': [9999]
        })
        
        # ファイル名を設定に合わせる
        test_file = self.work_dir / "案件管理台帳_マスター_yamada.xlsm"
        test_data.to_excel(test_file, sheet_name='案件一覧', index=False, engine='openpyxl')
        
        syncer = IncrementalSync(str(self.config_file))
        
        # 未同期データ取得（同期フラグ列が自動追加されるはず）
        unsynced = syncer.get_unsynced_data('山田')
        
        assert not unsynced.empty
        assert '_同期済み' in unsynced.columns
        print("✅ 同期フラグ列の自動追加成功")


# 単体テスト実行
if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3: 差分同期機能テスト")
    print("=" * 60)
    
    # pytest実行
    pytest.main([__file__, '-v', '--tb=short'])

