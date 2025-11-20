#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
差分同期スクリプト (incremental_sync.py)
Phase 3で実装

30分ごとに個人ファイルの差分のみをマスターファイルに同期する。
- 未同期データの抽出
- マスターファイルへの反映
- 同期済みフラグの更新
"""

import sys
from pathlib import Path

# Phase1の共通モジュールをインポート
sys.path.append(str(Path(__file__).parent.parent / 'phase1'))

import pandas as pd
import json
from datetime import datetime
import logging
from common import load_config, setup_logger
from file_handler import read_excel_safe, write_excel_safe, check_file_locked


class IncrementalSync:
    """差分同期クラス"""
    
    def __init__(self, config_path: str = None):
        """
        初期化
        
        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        # 設定ファイルのパスを決定
        if config_path is None:
            # phase3ディレクトリからphase1/config.jsonへの相対パス
            config_path = str(Path(__file__).parent.parent / 'phase1' / 'config.json')
        
        # 設定の読み込み
        self.config = load_config(config_path)
        
        # パスの設定
        base_dir = Path(__file__).parent.parent.parent
        self.master_dir = base_dir / self.config['paths']['master_dir']
        self.work_dir = base_dir / self.config['paths']['work_dir']
        self.log_dir = base_dir / self.config['paths']['log_dir']
        
        # ログディレクトリの作成
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # ロギング設定
        self._setup_logging()
        
        # マスターファイルのパス
        master_filename = self.config['file_settings']['master_file_name']
        self.master_file = self.master_dir / master_filename
        
        # 同期フラグ列名
        self.SYNC_FLAG_COL = '_同期済み'
        self.SYNC_TIME_COL = '_同期日時'
        
        self.logger.info("IncrementalSync 初期化完了")
        self.logger.info(f"マスターファイル: {self.master_file}")
        self.logger.info(f"作業ディレクトリ: {self.work_dir}")
    
    def _setup_logging(self):
        """ロギング設定"""
        log_file = self.log_dir / f"sync_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ],
            force=True  # 既存のロガー設定を上書き
        )
        self.logger = logging.getLogger(__name__)
    
    def get_unsynced_data(self, user_name: str) -> pd.DataFrame:
        """
        未同期のデータを取得
        
        Args:
            user_name: ユーザー名
            
        Returns:
            pd.DataFrame: 未同期のデータ
        """
        # ユーザーファイルのパスを取得
        user_info = next((u for u in self.config['users'] if u['name'] == user_name), None)
        
        if not user_info:
            self.logger.warning(f"ユーザー情報が見つかりません: {user_name}")
            return pd.DataFrame()
        
        file_prefix = user_info.get('file_prefix', user_name.lower())
        master_filename = self.config['file_settings']['master_file_name']
        base_name = master_filename.rsplit('.', 1)[0]
        extension = master_filename.rsplit('.', 1)[1] if '.' in master_filename else 'xlsm'
        user_filename = f"{base_name}_{file_prefix}.{extension}"
        
        user_file = self.work_dir / user_filename
        
        if not user_file.exists():
            self.logger.warning(f"ファイルが存在しません: {user_file}")
            return pd.DataFrame()
        
        # ファイルロックチェック（5秒待機）
        if check_file_locked(user_file, timeout=5):
            self.logger.warning(f"ファイルがロック中（スキップ）: {user_name}")
            return pd.DataFrame()
        
        try:
            # ファイル読み込み
            df = read_excel_safe(user_file, sheet_name='案件一覧')
            
            if df is None or df.empty:
                self.logger.info(f"{user_name}: データなし")
                return pd.DataFrame()
            
            # 同期フラグ列がない場合は作成
            if self.SYNC_FLAG_COL not in df.columns:
                df[self.SYNC_FLAG_COL] = False
                self.logger.info(f"{user_name}: 同期フラグ列を追加")
            
            if self.SYNC_TIME_COL not in df.columns:
                df[self.SYNC_TIME_COL] = pd.NaT
                self.logger.info(f"{user_name}: 同期日時列を追加")
            
            # 未同期のデータを抽出（同期フラグがFalseまたはNaN）
            unsynced = df[
                (df[self.SYNC_FLAG_COL] == False) | 
                (df[self.SYNC_FLAG_COL].isna())
            ].copy()
            
            if not unsynced.empty:
                # ユーザー名を追加
                unsynced['_更新者'] = user_name
                self.logger.info(f"{user_name}: {len(unsynced)}件の未同期データ")
            else:
                self.logger.info(f"{user_name}: 未同期データなし")
            
            return unsynced
            
        except Exception as e:
            self.logger.error(f"データ取得エラー ({user_name}): {e}", exc_info=True)
            return pd.DataFrame()
    
    def mark_as_synced(self, user_name: str, case_numbers: list) -> bool:
        """
        同期済みフラグを更新
        
        Args:
            user_name: ユーザー名
            case_numbers: 同期済み案件番号のリスト
            
        Returns:
            bool: 成功した場合True
        """
        # ユーザーファイルのパスを取得
        user_info = next((u for u in self.config['users'] if u['name'] == user_name), None)
        
        if not user_info:
            self.logger.warning(f"ユーザー情報が見つかりません: {user_name}")
            return False
        
        file_prefix = user_info.get('file_prefix', user_name.lower())
        master_filename = self.config['file_settings']['master_file_name']
        base_name = master_filename.rsplit('.', 1)[0]
        extension = master_filename.rsplit('.', 1)[1] if '.' in master_filename else 'xlsm'
        user_filename = f"{base_name}_{file_prefix}.{extension}"
        
        user_file = self.work_dir / user_filename
        
        if not user_file.exists():
            self.logger.warning(f"ファイルが存在しません: {user_file}")
            return False
        
        try:
            # ファイル読み込み
            df = read_excel_safe(user_file, sheet_name='案件一覧')
            
            if df is None or df.empty:
                return False
            
            # 同期フラグ列がない場合は作成
            if self.SYNC_FLAG_COL not in df.columns:
                df[self.SYNC_FLAG_COL] = False
            
            if self.SYNC_TIME_COL not in df.columns:
                df[self.SYNC_TIME_COL] = pd.NaT
            
            # 該当案件の同期フラグを更新
            mask = df['案件番号'].isin(case_numbers)
            updated_count = mask.sum()
            
            if updated_count > 0:
                df.loc[mask, self.SYNC_FLAG_COL] = True
                df.loc[mask, self.SYNC_TIME_COL] = datetime.now()
                
                # 保存
                success = write_excel_safe(
                    df,
                    user_file,
                    sheet_name='案件一覧',
                    create_backup=False  # 頻繁な更新のためバックアップなし
                )
                
                if success:
                    self.logger.info(f"{user_name}: {updated_count}件を同期済みに更新")
                    return True
                else:
                    self.logger.error(f"{user_name}: 同期フラグ更新の保存に失敗")
                    return False
            else:
                self.logger.warning(f"{user_name}: 対象案件が見つかりませんでした")
                return False
            
        except Exception as e:
            self.logger.error(f"同期フラグ更新エラー ({user_name}): {e}", exc_info=True)
            return False
    
    def update_master(self, unsynced_data_list: list) -> int:
        """
        マスターファイルを更新
        
        Args:
            unsynced_data_list: 各ユーザーの未同期データのリスト
            
        Returns:
            int: 更新件数
        """
        if not unsynced_data_list:
            self.logger.info("更新対象データなし")
            return 0
        
        try:
            # マスター読み込み
            if self.master_file.exists():
                master_df = read_excel_safe(self.master_file, sheet_name='案件一覧')
                if master_df is None:
                    self.logger.error("マスターファイルの読み込みに失敗")
                    return 0
            else:
                self.logger.info("マスターファイルが存在しないため、新規作成します")
                master_df = pd.DataFrame()
            
            # 全未同期データを結合
            all_unsynced = pd.concat(unsynced_data_list, ignore_index=True)
            self.logger.info(f"結合後の未同期データ: {len(all_unsynced)}件")
            
            # マスターに存在しない案件番号（新規）と存在する案件番号（更新）を分ける
            if not master_df.empty and '案件番号' in master_df.columns:
                new_cases = all_unsynced[
                    ~all_unsynced['案件番号'].isin(master_df['案件番号'])
                ].copy()
                
                existing_cases = all_unsynced[
                    all_unsynced['案件番号'].isin(master_df['案件番号'])
                ].copy()
                
                self.logger.info(f"新規案件: {len(new_cases)}件、更新案件: {len(existing_cases)}件")
                
                # 既存案件を更新
                for _, row in existing_cases.iterrows():
                    case_no = row['案件番号']
                    mask = master_df['案件番号'] == case_no
                    
                    # 行を更新（内部列は除外）
                    for col in row.index:
                        if not col.startswith('_') and col in master_df.columns:
                            master_df.loc[mask, col] = row[col]
                
                # 新規案件を追加
                if not new_cases.empty:
                    # 内部列を削除
                    new_cases_clean = new_cases.drop(
                        columns=[c for c in new_cases.columns if c.startswith('_')],
                        errors='ignore'
                    )
                    master_df = pd.concat([master_df, new_cases_clean], ignore_index=True)
                
                update_count = len(existing_cases) + len(new_cases)
                
            else:
                # マスターが空の場合
                self.logger.info("マスターが空のため、全データを新規追加")
                master_df = all_unsynced.drop(
                    columns=[c for c in all_unsynced.columns if c.startswith('_')],
                    errors='ignore'
                )
                update_count = len(master_df)
            
            # マスター保存
            success = write_excel_safe(
                master_df,
                self.master_file,
                sheet_name='案件一覧',
                create_backup=True  # マスター更新時はバックアップを作成
            )
            
            if success:
                self.logger.info(f"マスター更新成功: {update_count}件")
                return update_count
            else:
                self.logger.error("マスターファイルの保存に失敗")
                return 0
            
        except Exception as e:
            self.logger.error(f"マスター更新エラー: {e}", exc_info=True)
            return 0
    
    def sync_all(self) -> dict:
        """
        全ユーザーの差分を同期
        
        Returns:
            dict: 同期結果
        """
        self.logger.info("=" * 60)
        self.logger.info(f"差分同期開始 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        self.logger.info("=" * 60)
        
        # 各ユーザーの未同期データを収集
        unsynced_data_list = []
        user_case_map = {}  # ユーザー名 → 案件番号リスト
        
        for user in self.config['users']:
            user_name = user['name']
            self.logger.info(f"ユーザー処理開始: {user_name}")
            
            unsynced = self.get_unsynced_data(user_name)
            
            if not unsynced.empty:
                unsynced_data_list.append(unsynced)
                if '案件番号' in unsynced.columns:
                    user_case_map[user_name] = unsynced['案件番号'].tolist()
                else:
                    self.logger.warning(f"{user_name}: 案件番号列が見つかりません")
        
        if not unsynced_data_list:
            self.logger.info("同期対象データなし")
            result = {
                'synced': 0,
                'users': 0,
                'timestamp': datetime.now().isoformat(),
                'status': 'no_data'
            }
            self.logger.info("=" * 60)
            return result
        
        # マスター更新
        self.logger.info("マスターファイル更新開始")
        synced_count = self.update_master(unsynced_data_list)
        
        # 各ユーザーファイルの同期フラグを更新
        self.logger.info("同期フラグ更新開始")
        for user_name, case_numbers in user_case_map.items():
            self.mark_as_synced(user_name, case_numbers)
        
        result = {
            'synced': synced_count,
            'users': len(user_case_map),
            'timestamp': datetime.now().isoformat(),
            'status': 'success' if synced_count > 0 else 'no_update'
        }
        
        self.logger.info("=" * 60)
        self.logger.info(f"差分同期完了: {synced_count}件、{len(user_case_map)}ユーザー")
        self.logger.info("=" * 60)
        
        return result


def main():
    """メイン処理"""
    try:
        syncer = IncrementalSync()
        result = syncer.sync_all()
        
        # 終了コード
        # 0: 正常終了
        # 1: エラー
        exit(0 if result.get('status') in ['success', 'no_data', 'no_update'] else 1)
        
    except Exception as e:
        logging.error(f"致命的エラー: {e}", exc_info=True)
        exit(2)


if __name__ == "__main__":
    main()

