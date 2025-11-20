#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共通関数モジュール (common.py)
Phase 1で実装

このモジュールは、貿易DXシステム全体で使用される共通機能を提供します。
- 設定ファイルの読み込み
- ロガーのセットアップ
- ファイルパスの生成
- エラーハンドリング用デコレータ
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from functools import wraps
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler


def load_config(config_path: str = "phase1/config.json") -> Dict[str, Any]:
    """
    設定ファイルを読み込む
    
    Args:
        config_path: 設定ファイルのパス（デフォルト: phase1/config.json）
    
    Returns:
        Dict[str, Any]: 設定内容を格納した辞書
    
    Raises:
        FileNotFoundError: 設定ファイルが見つからない場合
        json.JSONDecodeError: JSONのパースに失敗した場合
    
    Example:
        >>> config = load_config()
        >>> print(config['version'])
        '2.1'
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {config_path}")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 設定の基本的な検証
        required_keys = ['version', 'paths', 'users']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"設定ファイルに必須項目が不足しています: {key}")
        
        return config
    
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"設定ファイルのJSON形式が不正です: {e.msg}",
            e.doc,
            e.pos
        )


def setup_logger(
    name: str = "tradedx",
    log_dir: str = "../../logs",
    config: Optional[Dict[str, Any]] = None
) -> logging.Logger:
    """
    ロガーをセットアップする
    
    Args:
        name: ロガー名（デフォルト: tradedx）
        log_dir: ログディレクトリ（デフォルト: ../../logs）
        config: 設定辞書（Noneの場合はデフォルト設定を使用）
    
    Returns:
        logging.Logger: 設定済みのロガーオブジェクト
    
    Example:
        >>> logger = setup_logger("phase1_test")
        >>> logger.info("テストメッセージ")
    """
    # 既存のロガーがある場合は返す
    if logging.getLogger(name).handlers:
        return logging.getLogger(name)
    
    # 設定を読み込む
    if config is None:
        try:
            config = load_config()
        except (FileNotFoundError, json.JSONDecodeError):
            # デフォルト設定を使用
            config = {
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'date_format': '%Y-%m-%d %H:%M:%S',
                    'max_bytes': 10485760,
                    'backup_count': 5
                }
            }
    
    # ログディレクトリを作成
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # ロガーを作成
    logger = logging.getLogger(name)
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    logger.setLevel(log_level)
    
    # ファイルハンドラー（ローテーション）
    log_file = log_path / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_config.get('max_bytes', 10485760),  # 10MB
        backupCount=log_config.get('backup_count', 5),
        encoding='utf-8'
    )
    
    # コンソールハンドラー
    console_handler = logging.StreamHandler()
    
    # フォーマッターを設定
    formatter = logging.Formatter(
        log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        datefmt=log_config.get('date_format', '%Y-%m-%d %H:%M:%S')
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # ハンドラーを追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_file_path(
    file_type: str,
    config: Optional[Dict[str, Any]] = None,
    user_name: Optional[str] = None,
    custom_name: Optional[str] = None
) -> Path:
    """
    ファイルパスを生成する
    
    Args:
        file_type: ファイルタイプ（'master', 'work', 'backup', 'log'）
        config: 設定辞書（Noneの場合は自動読み込み）
        user_name: ユーザー名（workファイルの場合に使用）
        custom_name: カスタムファイル名（指定された場合は優先）
    
    Returns:
        Path: 生成されたファイルパス
    
    Raises:
        ValueError: 無効なfile_typeが指定された場合
    
    Example:
        >>> path = get_file_path('master')
        >>> print(path)
        ../../master/案件管理台帳_マスター.xlsm
        
        >>> path = get_file_path('work', user_name='山田')
        >>> print(path)
        ../../work/案件管理台帳_yamada.xlsm
    """
    if config is None:
        config = load_config()
    
    paths = config.get('paths', {})
    file_settings = config.get('file_settings', {})
    
    # ベースディレクトリを取得
    valid_types = ['master', 'work', 'backup', 'log']
    if file_type not in valid_types:
        raise ValueError(f"無効なfile_typeです: {file_type}. 有効な値: {valid_types}")
    
    # プロジェクトルートを取得（このファイルの2階層上）
    project_root = Path(__file__).parent.parent.parent
    base_dir = project_root / paths.get(f'{file_type}_dir', file_type)
    
    # カスタム名が指定されている場合はそれを使用
    if custom_name:
        return base_dir / custom_name
    
    # ファイル名を生成
    master_file = file_settings.get('master_file_name', '案件管理台帳_マスター.xlsm')
    
    if file_type == 'master':
        return base_dir / master_file
    
    elif file_type == 'work':
        if not user_name:
            raise ValueError("workファイルのパスを生成するにはuser_nameが必要です")
        
        # ユーザー情報からfile_prefixを取得
        users = config.get('users', [])
        user_info = next((u for u in users if u['name'] == user_name), None)
        
        if user_info:
            prefix = user_info.get('file_prefix', user_name.lower())
        else:
            prefix = user_name.lower()
        
        # ファイル名を生成（拡張子を除いて置換）
        base_name = master_file.rsplit('.', 1)[0]
        extension = master_file.rsplit('.', 1)[1] if '.' in master_file else 'xlsm'
        work_file = f"{base_name}_{prefix}.{extension}"
        
        return base_dir / work_file
    
    elif file_type == 'backup':
        # バックアップファイルはタイムスタンプ付き
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = master_file.rsplit('.', 1)[0]
        extension = master_file.rsplit('.', 1)[1] if '.' in master_file else 'xlsm'
        backup_file = f"{base_name}_backup_{timestamp}.{extension}"
        
        return base_dir / backup_file
    
    elif file_type == 'log':
        # ログファイルは日付付き
        log_date = datetime.now().strftime('%Y%m%d')
        log_file = f"tradedx_{log_date}.log"
        
        return base_dir / log_file
    
    return base_dir


def error_handler(logger: Optional[logging.Logger] = None):
    """
    エラーハンドリング用デコレータ
    
    関数実行時に発生した例外をキャッチし、ログに記録します。
    
    Args:
        logger: ロガーオブジェクト（Noneの場合は新規作成）
    
    Example:
        >>> @error_handler()
        ... def risky_function():
        ...     return 1 / 0
        >>> risky_function()  # エラーをログに記録してNoneを返す
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ロガーの取得
            nonlocal logger
            if logger is None:
                logger = setup_logger()
            
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                # エラーログを出力
                logger.error(
                    f"関数 {func.__name__} でエラーが発生しました: {type(e).__name__}: {str(e)}",
                    exc_info=True
                )
                
                # エラーを再送出（呼び出し元で処理できるように）
                raise
        
        return wrapper
    return decorator


def get_timestamp(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    現在のタイムスタンプを取得する
    
    Args:
        format_str: 日時フォーマット文字列
    
    Returns:
        str: フォーマットされた現在日時
    
    Example:
        >>> timestamp = get_timestamp()
        >>> print(timestamp)
        2025-11-18 10:30:45
    """
    return datetime.now().strftime(format_str)


def validate_config(config: Dict[str, Any]) -> bool:
    """
    設定ファイルの内容を検証する
    
    Args:
        config: 検証する設定辞書
    
    Returns:
        bool: 検証結果（True=正常、False=異常）
    
    Raises:
        ValueError: 必須項目が不足している場合
    """
    # 必須トップレベルキー
    required_keys = ['version', 'paths', 'users']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"必須項目が不足しています: {key}")
    
    # pathsの検証
    paths = config.get('paths', {})
    required_paths = ['master_dir', 'work_dir', 'backup_dir', 'log_dir']
    for path_key in required_paths:
        if path_key not in paths:
            raise ValueError(f"paths に必須項目が不足しています: {path_key}")
    
    # usersの検証
    users = config.get('users', [])
    if not isinstance(users, list) or len(users) == 0:
        raise ValueError("users は空でない配列である必要があります")
    
    for user in users:
        if 'name' not in user:
            raise ValueError("各ユーザーには name が必要です")
    
    return True


# モジュールレベルでのテスト
if __name__ == "__main__":
    # 簡易テスト
    print("=== common.py モジュールテスト ===")
    
    try:
        # 設定ファイル読み込みテスト
        print("\n1. 設定ファイル読み込みテスト")
        config = load_config()
        print(f"   バージョン: {config['version']}")
        print(f"   ユーザー数: {len(config['users'])}")
        
        # ロガーセットアップテスト
        print("\n2. ロガーセットアップテスト")
        logger = setup_logger("test")
        logger.info("テストログメッセージ")
        print("   ロガー作成成功")
        
        # ファイルパス生成テスト
        print("\n3. ファイルパス生成テスト")
        master_path = get_file_path('master', config)
        print(f"   マスターパス: {master_path}")
        
        work_path = get_file_path('work', config, user_name='山田')
        print(f"   作業ファイルパス: {work_path}")
        
        # タイムスタンプ取得テスト
        print("\n4. タイムスタンプ取得テスト")
        timestamp = get_timestamp()
        print(f"   現在時刻: {timestamp}")
        
        print("\n✅ すべてのテストが成功しました")
    
    except Exception as e:
        print(f"\n❌ テスト失敗: {e}")

