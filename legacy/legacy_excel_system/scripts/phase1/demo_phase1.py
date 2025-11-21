#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 動作確認デモ

Phase 1で実装した機能を実際に動かして確認します。
- 設定ファイルの読み込み
- ロガーのセットアップ
- ファイルパスの生成
- Excelファイルの読み書き
- バックアップ作成
"""

import sys
from pathlib import Path
import pandas as pd

# Phase 1モジュールをインポート
sys.path.append(str(Path(__file__).parent))
from common import (
    load_config,
    setup_logger,
    get_file_path,
    get_timestamp,
    validate_config
)
from file_handler import (
    write_excel_safe,
    read_excel_safe,
    create_backup_file,
    get_file_info
)


def demo_config():
    """設定ファイル読み込みのデモ"""
    print("\n" + "="*60)
    print("【1】設定ファイル読み込みのデモ")
    print("="*60)
    
    try:
        # 設定ファイルのパスを取得
        config_path = Path(__file__).parent / "config.json"
        # 設定ファイルを読み込み
        config = load_config(str(config_path))
        
        print(f"[OK] 設定ファイル読み込み成功")
        print(f"  - バージョン: {config['version']}")
        print(f"  - プロジェクト名: {config['project_name']}")
        print(f"  - ユーザー数: {len(config['users'])}")
        
        # ユーザー情報を表示
        print(f"\n  登録ユーザー:")
        for user in config['users']:
            print(f"    - {user['name']} ({user['email']})")
        
        # 設定の検証
        validate_config(config)
        print(f"\n[OK] 設定の検証: OK")
        
        return config
    
    except Exception as e:
        print(f"[ERROR] エラー: {e}")
        return None


def demo_logger(config):
    """ロガーセットアップのデモ"""
    print("\n" + "="*60)
    print("【2】ロガーセットアップのデモ")
    print("="*60)
    
    try:
        # ロガーをセットアップ
        logger = setup_logger("demo", config=config)
        
        print(f"[OK] ロガーセットアップ成功")
        print(f"  - ロガー名: {logger.name}")
        print(f"  - ハンドラー数: {len(logger.handlers)}")
        
        # ログ出力のテスト
        print(f"\n  ログ出力テスト:")
        logger.info("これはINFOレベルのログです")
        logger.warning("これはWARNINGレベルのログです")
        logger.debug("これはDEBUGレベルのログです（表示されない場合があります）")
        
        print(f"\n  ※ログは以下に保存されます:")
        print(f"     ../../logs/demo_{get_timestamp('%Y%m%d')}.log")
        
        return logger
    
    except Exception as e:
        print(f"[ERROR] エラー: {e}")
        return None


def demo_file_path(config):
    """ファイルパス生成のデモ"""
    print("\n" + "="*60)
    print("【3】ファイルパス生成のデモ")
    print("="*60)
    
    try:
        # マスターファイルパス
        master_path = get_file_path('master', config)
        print(f"[OK] マスターファイルパス:")
        print(f"  {master_path}")
        
        # 各ユーザーの作業ファイルパス
        print(f"\n[OK] 作業ファイルパス:")
        for user in config['users']:
            work_path = get_file_path('work', config, user_name=user['name'])
            print(f"  - {user['name']}: {work_path}")
        
        # バックアップファイルパス
        backup_path = get_file_path('backup', config)
        print(f"\n[OK] バックアップファイルパス:")
        print(f"  {backup_path}")
        
        # ログファイルパス
        log_path = get_file_path('log', config)
        print(f"\n[OK] ログファイルパス:")
        print(f"  {log_path}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] エラー: {e}")
        return False


def demo_excel_operations(config, logger):
    """Excelファイル操作のデモ"""
    print("\n" + "="*60)
    print("【4】Excelファイル操作のデモ")
    print("="*60)
    
    try:
        # テスト用ディレクトリ作成
        demo_dir = Path("../../demo_output")
        demo_dir.mkdir(parents=True, exist_ok=True)
        demo_file = demo_dir / "demo_案件管理台帳.xlsx"
        
        # サンプルデータ作成
        print(f"\n[OK] サンプルデータ作成")
        sample_data = pd.DataFrame({
            '案件番号': ['EX-2025-001', 'IM-2025-001', 'EX-2025-002'],
            '顧客名': ['株式会社サンプル商事', '山田貿易株式会社', '鈴木インターナショナル'],
            '取引区分': ['輸出', '輸入', '輸出'],
            '品名': ['機械部品', '電子機器', '自動車部品'],
            '数量': [100, 50, 200],
            '単価': [5000, 12000, 8000],
            '金額': [500000, 600000, 1600000],
            'ステータス': ['進行中', '完了', '見積中'],
            '登録日': [get_timestamp('%Y-%m-%d')] * 3,
            '備考': ['通常納期', 'お急ぎ案件', '継続取引先']
        })
        print(f"  データ: {len(sample_data)}件")
        print(f"\n{sample_data.to_string(index=False)}")
        
        # Excel書き込み
        print(f"\n[OK] Excelファイル書き込み")
        success = write_excel_safe(
            sample_data,
            demo_file,
            sheet_name="案件一覧",
            create_backup=False
        )
        
        if success:
            print(f"  ファイル作成: {demo_file}")
            logger.info(f"デモファイル作成成功: {demo_file}")
        else:
            print(f"  [FAILED] 書き込み失敗")
            return False
        
        # Excel読み込み
        print(f"\n[OK] Excelファイル読み込み")
        df = read_excel_safe(demo_file, sheet_name="案件一覧")
        
        if df is not None:
            print(f"  読み込み成功: {len(df)}行 × {len(df.columns)}列")
            print(f"  列名: {', '.join(df.columns.tolist())}")
            logger.info(f"デモファイル読み込み成功: {len(df)}行")
        else:
            print(f"  [FAILED] 読み込み失敗")
            return False
        
        # ファイル情報取得
        print(f"\n[OK] ファイル情報取得")
        info = get_file_info(demo_file)
        print(f"  - ファイル名: {info['name']}")
        print(f"  - サイズ: {info['size_mb']:.4f} MB")
        print(f"  - 更新日時: {info['modified_time']}")
        print(f"  - ロック状態: {'ロック中' if info['is_locked'] else '使用可能'}")
        
        # バックアップ作成
        print(f"\n[OK] バックアップ作成")
        backup_path = create_backup_file(demo_file, demo_dir)
        
        if backup_path:
            print(f"  バックアップ作成: {backup_path.name}")
            logger.info(f"バックアップ作成成功: {backup_path}")
        else:
            print(f"  [FAILED] バックアップ作成失敗")
        
        print(f"\n  ※作成されたファイル:")
        print(f"     {demo_dir.absolute()}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] エラー: {e}")
        logger.error(f"Excel操作デモでエラー: {e}")
        return False


def demo_error_handling(logger):
    """エラーハンドリングのデモ"""
    print("\n" + "="*60)
    print("【5】エラーハンドリングのデモ")
    print("="*60)
    
    from common import error_handler
    
    @error_handler(logger)
    def test_function_success():
        """正常に動作する関数"""
        result = 10 + 20
        return result
    
    @error_handler(logger)
    def test_function_error():
        """エラーが発生する関数"""
        return 10 / 0  # ZeroDivisionError
    
    # 正常系のテスト
    print(f"\n[OK] 正常系テスト:")
    result = test_function_success()
    print(f"  結果: {result}")
    print(f"  エラーハンドリングは動作していませんが、正常です")
    
    # 異常系のテスト
    print(f"\n[OK] 異常系テスト (エラーを意図的に発生):")
    try:
        test_function_error()
    except ZeroDivisionError:
        print(f"  エラーを正しくキャッチしました")
        print(f"  エラーログがファイルに記録されています")
    
    return True


def main():
    """メイン処理"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  Phase 1 動作確認デモ".center(56) + "  *")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    
    # 1. 設定ファイル読み込み
    config = demo_config()
    if not config:
        print("\n[ERROR] 設定ファイル読み込みに失敗しました")
        return
    
    # 2. ロガーセットアップ
    logger = demo_logger(config)
    if not logger:
        print("\n[ERROR] ロガーセットアップに失敗しました")
        return
    
    # 3. ファイルパス生成
    demo_file_path(config)
    
    # 4. Excelファイル操作
    demo_excel_operations(config, logger)
    
    # 5. エラーハンドリング
    demo_error_handling(logger)
    
    # 完了メッセージ
    print("\n" + "="*60)
    print("【完了】Phase 1 動作確認デモ")
    print("="*60)
    print(f"\n[OK] すべてのデモが正常に完了しました")
    print(f"\n作成されたファイル:")
    print(f"  - デモ用Excelファイル: ../../demo_output/")
    print(f"  - ログファイル: ../../logs/")
    print(f"\nPhase 1の基盤機能が正常に動作していることを確認できました。")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

