#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3 テストデータ作成スクリプト
手動動作確認用のサンプルデータを作成します
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Phase1のモジュールをインポート
sys.path.append(str(Path(__file__).parent.parent / 'phase1'))
from common import load_config

def create_test_data():
    """テスト用のExcelファイルを作成"""
    
    print("=" * 60)
    print("Phase 3 テストデータ作成")
    print("=" * 60)
    
    try:
        # 設定読み込み
        config_path = Path(__file__).parent.parent / 'phase1' / 'config.json'
        config = load_config(str(config_path))
        
        base_dir = Path(__file__).parent.parent.parent
        master_dir = base_dir / config['paths']['master_dir']
        work_dir = base_dir / config['paths']['work_dir']
        
        # ディレクトリ作成
        master_dir.mkdir(parents=True, exist_ok=True)
        work_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n[ディレクトリ]")
        print(f"  - マスター: {master_dir}")
        print(f"  - 作業: {work_dir}")
        
        # 1. マスターファイルの作成
        print("\n【1. マスターファイル作成】")
        master_data = pd.DataFrame({
            '案件番号': ['2025-EX-001', '2025-EX-002', '2025-IM-001'],
            '区分': ['輸出', '輸出', '輸入'],
            '顧客名': ['テスト商事株式会社', 'サンプル貿易', 'デモインポート'],
            '仕向地': ['アメリカ', 'ドイツ', '中国'],
            '数量': [100, 200, 150],
            '単価': [1000, 1500, 1200],
            '金額': [100000, 300000, 180000],
            'ステータス': ['進行中', '完了', '進行中'],
            '担当者': ['山田', '鈴木', '佐藤'],
            '備考': ['', '', ''],
            '最終更新日時': [
                datetime(2025, 11, 1, 10, 0, 0),
                datetime(2025, 11, 2, 15, 0, 0),
                datetime(2025, 11, 3, 9, 0, 0)
            ]
        })
        
        master_filename = config['file_settings']['master_file_name']
        master_file = master_dir / master_filename
        master_data.to_excel(master_file, sheet_name='案件一覧', index=False, engine='openpyxl')
        print(f"  [OK] 作成: {master_file.name}")
        print(f"     件数: {len(master_data)}件")
        
        # 2. 個人ファイルの作成（各ユーザー）
        print("\n【2. 個人ファイル作成】")
        
        for user in config['users']:
            user_name = user['name']
            file_prefix = user.get('file_prefix', user_name.lower())
            
            # ファイル名を生成
            base_name = master_filename.rsplit('.', 1)[0]
            extension = master_filename.rsplit('.', 1)[1]
            user_filename = f"{base_name}_{file_prefix}.{extension}"
            user_file = work_dir / user_filename
            
            # ユーザーごとのデータ
            if user_name == '山田':
                # 山田さん: 既存案件の更新 + 新規案件
                user_data = pd.DataFrame({
                    '案件番号': ['2025-EX-001', '2025-EX-004'],
                    '区分': ['輸出', '輸出'],
                    '顧客名': ['テスト商事株式会社', '新規顧客株式会社'],
                    '仕向地': ['アメリカ', 'フランス'],
                    '数量': [150, 300],  # EX-001は100→150に更新
                    '単価': [1000, 2000],
                    '金額': [150000, 600000],
                    'ステータス': ['進行中', '見積中'],
                    '担当者': ['山田', '山田'],
                    '備考': ['数量を更新しました', '新規案件です'],
                    '最終更新日時': [
                        datetime(2025, 11, 20, 10, 0, 0),
                        datetime(2025, 11, 20, 11, 0, 0)
                    ],
                    '_同期済み': [False, False]  # 両方未同期
                })
            
            elif user_name == '鈴木':
                # 鈴木さん: 既存案件（同期済み）のみ
                user_data = pd.DataFrame({
                    '案件番号': ['2025-EX-002'],
                    '区分': ['輸出'],
                    '顧客名': ['サンプル貿易'],
                    '仕向地': ['ドイツ'],
                    '数量': [200],
                    '単価': [1500],
                    '金額': [300000],
                    'ステータス': ['完了'],
                    '担当者': ['鈴木'],
                    '備考': [''],
                    '最終更新日時': [
                        datetime(2025, 11, 2, 15, 0, 0)
                    ],
                    '_同期済み': [True]  # 同期済み
                })
            
            elif user_name == '佐藤':
                # 佐藤さん: 既存案件の更新
                user_data = pd.DataFrame({
                    '案件番号': ['2025-IM-001'],
                    '区分': ['輸入'],
                    '顧客名': ['デモインポート'],
                    '仕向地': ['中国'],
                    '数量': [180],  # 150→180に更新
                    '単価': [1200],
                    '金額': [216000],
                    'ステータス': ['検査中'],
                    '担当者': ['佐藤'],
                    '備考': ['数量追加、検査開始'],
                    '最終更新日時': [
                        datetime(2025, 11, 20, 9, 30, 0)
                    ],
                    '_同期済み': [False]  # 未同期
                })
            
            else:
                # その他のユーザー: 空ファイル
                user_data = pd.DataFrame(columns=[
                    '案件番号', '区分', '顧客名', '仕向地', '数量', '単価', '金額',
                    'ステータス', '担当者', '備考', '最終更新日時', '_同期済み'
                ])
            
            # ファイル保存
            user_data.to_excel(user_file, sheet_name='案件一覧', index=False, engine='openpyxl')
            print(f"  [OK] 作成: {user_filename}")
            print(f"     件数: {len(user_data)}件")
            if not user_data.empty and '_同期済み' in user_data.columns:
                unsynced = len(user_data[user_data['_同期済み'] == False])
                print(f"     未同期: {unsynced}件")
        
        # サマリー
        print("\n" + "=" * 60)
        print("[完了] テストデータ作成完了")
        print("=" * 60)
        print("\n【作成されたファイル】")
        print(f"  マスター: {master_file}")
        print(f"  個人ファイル: {len(config['users'])}個")
        print("\n【期待される同期結果】")
        print("  - 山田さん: 2件同期（EX-001更新 + EX-004新規）")
        print("  - 鈴木さん: 0件（すでに同期済み）")
        print("  - 佐藤さん: 1件同期（IM-001更新）")
        print("  - 合計: 3件が同期されるはず")
        print("")
        
        return True
        
    except Exception as e:
        print(f"\n[エラー] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = create_test_data()
    exit(0 if success else 1)

