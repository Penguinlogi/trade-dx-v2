#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ファイル操作モジュール (file_handler.py)
Phase 1で実装

このモジュールは、Excelファイルの安全な読み書き機能を提供します。
- ファイルロック検知
- 安全なExcel読み込み
- 安全なExcel書き込み
- バックアップ作成
"""

import os
import sys
import shutil
import time
from pathlib import Path
from typing import Optional, Union, List
from datetime import datetime

import pandas as pd

# 同じディレクトリのcommon.pyをインポート
sys.path.append(str(Path(__file__).parent))
from common import setup_logger, get_timestamp, load_config


# ロガーの初期化
logger = setup_logger("file_handler")


def check_file_locked(file_path: Union[str, Path], timeout: int = 5) -> bool:
    """
    ファイルがロックされているかチェックする
    
    Args:
        file_path: チェックするファイルのパス
        timeout: タイムアウト時間（秒）
    
    Returns:
        bool: ロックされている場合True、されていない場合False
    
    Example:
        >>> is_locked = check_file_locked("../../master/案件管理台帳_マスター.xlsm")
        >>> if is_locked:
        ...     print("ファイルは使用中です")
    """
    file_path = Path(file_path)
    
    # ファイルが存在しない場合はロックされていないと判定
    if not file_path.exists():
        logger.warning(f"ファイルが存在しません: {file_path}")
        return False
    
    try:
        # ファイルを排他モードで開いてみる
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Windows: 排他的にファイルを開く
                with open(file_path, 'a') as f:
                    pass
                
                logger.debug(f"ファイルはロックされていません: {file_path}")
                return False
            
            except (IOError, OSError, PermissionError):
                # ファイルがロックされている
                time.sleep(0.5)
                continue
        
        # タイムアウト
        logger.warning(f"ファイルロックのタイムアウト: {file_path}")
        return True
    
    except Exception as e:
        logger.error(f"ファイルロックチェック中にエラー: {e}")
        return True


def read_excel_safe(
    file_path: Union[str, Path],
    sheet_name: Optional[str] = None,
    retry_count: int = 3,
    retry_interval: int = 60
) -> Optional[pd.DataFrame]:
    """
    Excelファイルを安全に読み込む
    
    ファイルがロックされている場合は指定回数リトライします。
    
    Args:
        file_path: 読み込むExcelファイルのパス
        sheet_name: シート名（Noneの場合は最初のシート）
        retry_count: リトライ回数
        retry_interval: リトライ間隔（秒）
    
    Returns:
        Optional[pd.DataFrame]: 読み込んだデータフレーム（失敗時はNone）
    
    Raises:
        FileNotFoundError: ファイルが見つからない場合
    
    Example:
        >>> df = read_excel_safe("../../master/案件管理台帳_マスター.xlsm", "案件一覧")
        >>> if df is not None:
        ...     print(f"読み込み成功: {len(df)}件")
    """
    file_path = Path(file_path)
    
    # ファイルの存在チェック
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    
    logger.info(f"Excelファイル読み込み開始: {file_path}")
    
    # リトライループ
    for attempt in range(retry_count):
        try:
            # ファイルロックチェック
            if check_file_locked(file_path):
                logger.warning(f"ファイルがロックされています（試行 {attempt + 1}/{retry_count}）: {file_path}")
                
                if attempt < retry_count - 1:
                    logger.info(f"{retry_interval}秒後にリトライします...")
                    time.sleep(retry_interval)
                    continue
                else:
                    logger.error(f"リトライ回数超過: {file_path}")
                    return None
            
            # Excelファイルを読み込み
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
            else:
                df = pd.read_excel(file_path, engine='openpyxl')
            
            logger.info(f"読み込み成功: {len(df)}行 × {len(df.columns)}列")
            return df
        
        except PermissionError as e:
            logger.warning(f"アクセス権限エラー（試行 {attempt + 1}/{retry_count}）: {e}")
            
            if attempt < retry_count - 1:
                time.sleep(retry_interval)
                continue
            else:
                logger.error(f"アクセス権限エラーでリトライ回数超過")
                return None
        
        except Exception as e:
            logger.error(f"Excelファイル読み込みエラー: {type(e).__name__}: {e}")
            return None
    
    return None


def write_excel_safe(
    df: pd.DataFrame,
    file_path: Union[str, Path],
    sheet_name: str = "Sheet1",
    create_backup: bool = True,
    retry_count: int = 3,
    retry_interval: int = 60
) -> bool:
    """
    Excelファイルを安全に書き込む
    
    ファイルがロックされている場合は指定回数リトライします。
    書き込み前に自動バックアップを作成できます。
    
    Args:
        df: 書き込むデータフレーム
        file_path: 書き込み先のExcelファイルパス
        sheet_name: シート名
        create_backup: バックアップを作成するか
        retry_count: リトライ回数
        retry_interval: リトライ間隔（秒）
    
    Returns:
        bool: 成功した場合True、失敗した場合False
    
    Example:
        >>> df = pd.DataFrame({'案件番号': ['EX-001', 'IM-001'], '顧客名': ['A社', 'B社']})
        >>> success = write_excel_safe(df, "../../master/案件管理台帳_マスター.xlsm")
        >>> if success:
        ...     print("書き込み成功")
    """
    file_path = Path(file_path)
    
    logger.info(f"Excelファイル書き込み開始: {file_path}")
    
    # バックアップ作成
    if create_backup and file_path.exists():
        backup_path = create_backup_file(file_path)
        if backup_path:
            logger.info(f"バックアップ作成: {backup_path}")
    
    # リトライループ
    for attempt in range(retry_count):
        try:
            # ファイルロックチェック
            if file_path.exists() and check_file_locked(file_path):
                logger.warning(f"ファイルがロックされています（試行 {attempt + 1}/{retry_count}）: {file_path}")
                
                if attempt < retry_count - 1:
                    logger.info(f"{retry_interval}秒後にリトライします...")
                    time.sleep(retry_interval)
                    continue
                else:
                    logger.error(f"リトライ回数超過: {file_path}")
                    return False
            
            # ディレクトリが存在しない場合は作成
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Excelファイルに書き込み
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.info(f"書き込み成功: {len(df)}行 × {len(df.columns)}列")
            return True
        
        except PermissionError as e:
            logger.warning(f"アクセス権限エラー（試行 {attempt + 1}/{retry_count}）: {e}")
            
            if attempt < retry_count - 1:
                time.sleep(retry_interval)
                continue
            else:
                logger.error(f"アクセス権限エラーでリトライ回数超過")
                return False
        
        except Exception as e:
            logger.error(f"Excelファイル書き込みエラー: {type(e).__name__}: {e}")
            return False
    
    return False


def create_backup_file(
    source_path: Union[str, Path],
    backup_dir: Optional[Union[str, Path]] = None
) -> Optional[Path]:
    """
    ファイルのバックアップを作成する
    
    Args:
        source_path: バックアップ元のファイルパス
        backup_dir: バックアップ先ディレクトリ（Noneの場合は../../backup/）
    
    Returns:
        Optional[Path]: 作成したバックアップファイルのパス（失敗時はNone）
    
    Example:
        >>> backup_path = create_backup_file("../../master/案件管理台帳_マスター.xlsm")
        >>> if backup_path:
        ...     print(f"バックアップ作成: {backup_path}")
    """
    source_path = Path(source_path)
    
    # ファイルの存在チェック
    if not source_path.exists():
        logger.error(f"バックアップ元ファイルが存在しません: {source_path}")
        return None
    
    try:
        # バックアップディレクトリの決定
        if backup_dir is None:
            # デフォルトのバックアップディレクトリ
            config = load_config()
            # プロジェクトルートを取得（このファイルの2階層上）
            project_root = Path(__file__).parent.parent.parent
            backup_dir = project_root / config['paths']['backup_dir']
        else:
            backup_dir = Path(backup_dir)
        
        # バックアップディレクトリを作成
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # バックアップファイル名を生成（タイムスタンプ付き）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_stem = source_path.stem  # 拡張子を除いたファイル名
        file_suffix = source_path.suffix  # 拡張子
        backup_name = f"{file_stem}_backup_{timestamp}{file_suffix}"
        backup_path = backup_dir / backup_name
        
        # ファイルをコピー
        shutil.copy2(source_path, backup_path)
        
        logger.info(f"バックアップ作成成功: {backup_path}")
        return backup_path
    
    except Exception as e:
        logger.error(f"バックアップ作成エラー: {type(e).__name__}: {e}")
        return None


def cleanup_old_backups(
    backup_dir: Union[str, Path],
    retention_days: int = 30,
    file_pattern: str = "*_backup_*"
) -> int:
    """
    古いバックアップファイルを削除する
    
    Args:
        backup_dir: バックアップディレクトリ
        retention_days: 保持日数
        file_pattern: 削除対象のファイルパターン
    
    Returns:
        int: 削除したファイル数
    
    Example:
        >>> deleted_count = cleanup_old_backups("../../backup/", retention_days=30)
        >>> print(f"{deleted_count}件の古いバックアップを削除しました")
    """
    backup_dir = Path(backup_dir)
    
    if not backup_dir.exists():
        logger.warning(f"バックアップディレクトリが存在しません: {backup_dir}")
        return 0
    
    try:
        deleted_count = 0
        current_time = time.time()
        retention_seconds = retention_days * 24 * 60 * 60
        
        # パターンに一致するファイルを検索
        for backup_file in backup_dir.glob(file_pattern):
            if not backup_file.is_file():
                continue
            
            # ファイルの更新日時をチェック
            file_age = current_time - backup_file.stat().st_mtime
            
            if file_age > retention_seconds:
                try:
                    backup_file.unlink()
                    logger.info(f"古いバックアップを削除: {backup_file.name}")
                    deleted_count += 1
                except Exception as e:
                    logger.error(f"ファイル削除エラー: {backup_file.name}: {e}")
        
        logger.info(f"バックアップクリーンアップ完了: {deleted_count}件削除")
        return deleted_count
    
    except Exception as e:
        logger.error(f"バックアップクリーンアップエラー: {e}")
        return 0


def get_file_info(file_path: Union[str, Path]) -> dict:
    """
    ファイル情報を取得する
    
    Args:
        file_path: ファイルパス
    
    Returns:
        dict: ファイル情報（サイズ、更新日時など）
    
    Example:
        >>> info = get_file_info("../../master/案件管理台帳_マスター.xlsm")
        >>> print(f"ファイルサイズ: {info['size_mb']:.2f} MB")
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {
            'exists': False,
            'error': 'ファイルが存在しません'
        }
    
    try:
        stat = file_path.stat()
        
        return {
            'exists': True,
            'path': str(file_path),
            'name': file_path.name,
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified_time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'created_time': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'is_locked': check_file_locked(file_path, timeout=1)
        }
    
    except Exception as e:
        return {
            'exists': True,
            'error': f'情報取得エラー: {e}'
        }


# モジュールレベルでのテスト
if __name__ == "__main__":
    print("=== file_handler.py モジュールテスト ===")
    
    try:
        # テスト用のサンプルデータ作成
        print("\n1. サンプルデータ作成")
        test_data = pd.DataFrame({
            '案件番号': ['EX-001', 'EX-002', 'IM-001'],
            '顧客名': ['A社', 'B社', 'C社'],
            '数量': [100, 200, 150],
            '単価': [1000, 1500, 1200]
        })
        print(f"   サンプルデータ: {len(test_data)}行")
        
        # テスト用ディレクトリの作成
        test_dir = Path("../../test_output")
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = test_dir / "test_file.xlsx"
        
        # 書き込みテスト
        print("\n2. Excelファイル書き込みテスト")
        success = write_excel_safe(
            test_data,
            test_file,
            sheet_name="テストシート",
            create_backup=False
        )
        if success:
            print(f"   ✅ 書き込み成功: {test_file}")
        else:
            print(f"   ❌ 書き込み失敗")
        
        # 読み込みテスト
        print("\n3. Excelファイル読み込みテスト")
        df = read_excel_safe(test_file, sheet_name="テストシート")
        if df is not None:
            print(f"   ✅ 読み込み成功: {len(df)}行 × {len(df.columns)}列")
        else:
            print(f"   ❌ 読み込み失敗")
        
        # ファイル情報取得テスト
        print("\n4. ファイル情報取得テスト")
        info = get_file_info(test_file)
        if info['exists']:
            print(f"   ファイル名: {info['name']}")
            print(f"   サイズ: {info['size_mb']:.4f} MB")
            print(f"   更新日時: {info['modified_time']}")
            print(f"   ロック状態: {'ロック中' if info['is_locked'] else '使用可能'}")
        
        # バックアップ作成テスト
        print("\n5. バックアップ作成テスト")
        backup_path = create_backup_file(test_file, test_dir)
        if backup_path:
            print(f"   ✅ バックアップ作成成功: {backup_path.name}")
        else:
            print(f"   ❌ バックアップ作成失敗")
        
        print("\n✅ すべてのテストが完了しました")
        print(f"\n※ テストファイルは {test_dir} に保存されています")
    
    except Exception as e:
        print(f"\n❌ テスト失敗: {e}")
        import traceback
        traceback.print_exc()

