#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
未同期データを追加するスクリプト
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent / 'phase1'))

def add_unsynced_data():
    """山田さんのファイルに未同期データを追加"""
    
    project_root = Path(__file__).parent.parent.parent
    yamada_file = project_root / 'work' / '案件管理台帳_マスター_yamada.xlsx'
    
    if not yamada_file.exists():
        print(f"エラー: ファイルが見つかりません - {yamada_file}")
        return False
    
    try:
        # 既存データを読み込み
        df = pd.read_excel(yamada_file, sheet_name='案件一覧', engine='openpyxl')
        
        # 新しい未同期データを追加
        new_row = pd.DataFrame({
            '案件番号': ['2025-EX-005'],
            '区分': ['輸出'],
            '顧客名': ['テスト追加株式会社'],
            '仕向地': ['イギリス'],
            '数量': [500],
            '単価': [2500],
            '金額': [1250000],
            'ステータス': ['見積中'],
            '担当者': ['山田'],
            '備考': ['バックアップテスト用の新規案件'],
            '最終更新日時': [datetime.now()],
            '_同期済み': [False],
            '_同期日時': [pd.NaT]
        })
        
        # データを結合
        df = pd.concat([df, new_row], ignore_index=True)
        
        # 保存
        df.to_excel(yamada_file, sheet_name='案件一覧', index=False, engine='openpyxl')
        
        print("=" * 60)
        print("未同期データを追加しました")
        print("=" * 60)
        print(f"ファイル: {yamada_file.name}")
        print(f"追加データ: 2025-EX-005")
        print("\n次のコマンドで差分同期を実行してください:")
        print("  python scripts\\phase3\\incremental_sync.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = add_unsynced_data()
    exit(0 if success else 1)

