#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3 手動テストスクリプト
差分同期機能の動作確認
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Phase3のモジュールをインポート
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent / 'phase1'))

from incremental_sync import IncrementalSync


def print_header(title: str):
    """ヘッダーを表示"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_dataframe(df: pd.DataFrame, max_rows: int = 10):
    """データフレームを見やすく表示"""
    if df.empty:
        print("  （データなし）")
        return
    
    print(f"  件数: {len(df)}行")
    print(f"\n{df.head(max_rows).to_string(index=False)}")
    
    if len(df) > max_rows:
        print(f"  ... （残り {len(df) - max_rows} 行）")


def test_1_initialization():
    """テスト1: 初期化とファイル確認"""
    print_header("テスト1: 初期化とファイル確認")
    
    try:
        syncer = IncrementalSync()
        
        print(f"\n✅ IncrementalSync 初期化成功")
        print(f"  - マスターファイル: {syncer.master_file}")
        print(f"  - 作業ディレクトリ: {syncer.work_dir}")
        print(f"  - ログディレクトリ: {syncer.log_dir}")
        print(f"  - 同期フラグ列: {syncer.SYNC_FLAG_COL}")
        print(f"  - 同期日時列: {syncer.SYNC_TIME_COL}")
        
        # ファイルの存在確認
        print(f"\nファイル存在確認:")
        print(f"  - マスターファイル: {'存在' if syncer.master_file.exists() else '不在'}")
        
        # ユーザーファイルの確認
        for user in syncer.config['users']:
            user_name = user['name']
            file_prefix = user.get('file_prefix', user_name.lower())
            master_filename = syncer.config['file_settings']['master_file_name']
            base_name = master_filename.rsplit('.', 1)[0]
            extension = master_filename.rsplit('.', 1)[1]
            user_filename = f"{base_name}_{file_prefix}.{extension}"
            user_file = syncer.work_dir / user_filename
            
            print(f"  - {user_name}の個人ファイル: {'存在' if user_file.exists() else '不在'}")
        
        return syncer
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_2_get_unsynced_data(syncer: IncrementalSync):
    """テスト2: 未同期データの取得"""
    print_header("テスト2: 未同期データの取得")
    
    if not syncer:
        print("⚠️ スキップ（syncerが初期化されていません）")
        return
    
    try:
        for user in syncer.config['users']:
            user_name = user['name']
            print(f"\n【{user_name}さんの未同期データ】")
            
            unsynced = syncer.get_unsynced_data(user_name)
            print_dataframe(unsynced)
        
        print("\n✅ 未同期データ取得完了")
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()


def test_3_sync_all(syncer: IncrementalSync):
    """テスト3: 差分同期の実行"""
    print_header("テスト3: 差分同期の実行")
    
    if not syncer:
        print("⚠️ スキップ（syncerが初期化されていません）")
        return None
    
    try:
        # 同期実行
        result = syncer.sync_all()
        
        print(f"\n✅ 差分同期完了")
        print(f"  - 同期件数: {result['synced']}件")
        print(f"  - ユーザー数: {result['users']}人")
        print(f"  - ステータス: {result['status']}")
        print(f"  - 実行日時: {result['timestamp']}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_4_verify_master(syncer: IncrementalSync):
    """テスト4: マスターファイルの確認"""
    print_header("テスト4: マスターファイルの確認")
    
    if not syncer:
        print("⚠️ スキップ（syncerが初期化されていません）")
        return
    
    try:
        if not syncer.master_file.exists():
            print("⚠️ マスターファイルが存在しません")
            return
        
        master_df = pd.read_excel(
            syncer.master_file,
            sheet_name='案件一覧',
            engine='openpyxl'
        )
        
        print(f"\n【マスターファイルの内容】")
        print_dataframe(master_df)
        
        print(f"\n✅ マスターファイル確認完了")
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()


def test_5_verify_sync_flags(syncer: IncrementalSync):
    """テスト5: 同期フラグの確認"""
    print_header("テスト5: 同期フラグの確認")
    
    if not syncer:
        print("⚠️ スキップ（syncerが初期化されていません）")
        return
    
    try:
        for user in syncer.config['users']:
            user_name = user['name']
            file_prefix = user.get('file_prefix', user_name.lower())
            master_filename = syncer.config['file_settings']['master_file_name']
            base_name = master_filename.rsplit('.', 1)[0]
            extension = master_filename.rsplit('.', 1)[1]
            user_filename = f"{base_name}_{file_prefix}.{extension}"
            user_file = syncer.work_dir / user_filename
            
            if not user_file.exists():
                print(f"\n【{user_name}さん】ファイルが存在しません")
                continue
            
            user_df = pd.read_excel(
                user_file,
                sheet_name='案件一覧',
                engine='openpyxl'
            )
            
            print(f"\n【{user_name}さんの同期フラグ】")
            
            if syncer.SYNC_FLAG_COL in user_df.columns:
                synced_count = user_df[syncer.SYNC_FLAG_COL].sum()
                total_count = len(user_df)
                print(f"  - 同期済み: {synced_count}/{total_count}件")
                
                # 未同期データがあれば表示
                unsynced = user_df[user_df[syncer.SYNC_FLAG_COL] == False]
                if not unsynced.empty:
                    print(f"  - 未同期案件番号: {unsynced['案件番号'].tolist()}")
            else:
                print(f"  - 同期フラグ列なし")
        
        print(f"\n✅ 同期フラグ確認完了")
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()


def test_6_second_sync(syncer: IncrementalSync):
    """テスト6: 2回目の同期（重複確認）"""
    print_header("テスト6: 2回目の同期（重複確認）")
    
    if not syncer:
        print("⚠️ スキップ（syncerが初期化されていません）")
        return
    
    try:
        print("\n2回目の同期を実行します...")
        result = syncer.sync_all()
        
        print(f"\n✅ 2回目の同期完了")
        print(f"  - 同期件数: {result['synced']}件（0件であればOK）")
        print(f"  - ステータス: {result['status']}")
        
        if result['synced'] == 0:
            print("\n✅ 重複なし！正常に動作しています")
        else:
            print("\n⚠️ 警告: 同期済みデータが再度同期されました")
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()


def main():
    """メイン処理"""
    print("=" * 60)
    print("  Phase 3: 差分同期機能 - 手動テスト")
    print("=" * 60)
    print("\n【注意】")
    print("  - このテストは実際のファイルを使用します")
    print("  - 本番環境では実行しないでください")
    print("  - テスト前にバックアップを取ることを推奨します")
    print("")
    
    input("Enterキーを押すとテストを開始します...")
    
    # テスト実行
    syncer = test_1_initialization()
    test_2_get_unsynced_data(syncer)
    test_3_sync_all(syncer)
    test_4_verify_master(syncer)
    test_5_verify_sync_flags(syncer)
    test_6_second_sync(syncer)
    
    # サマリー
    print_header("テスト完了")
    print("\n全てのテストが完了しました。")
    print("ログファイルを確認してください。")
    print("")


if __name__ == "__main__":
    main()

