#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合処理スクリプト（改良版）
Phase 4: 項目単位の競合解決とリトライ機構

【機能】
1. 項目単位の競合解決
   - 同じ案件を複数人が更新した場合、各項目ごとに最新の値を採用
   - データロスト防止
   
2. ファイルロック検知
   - Excelファイルが開かれている場合を検知
   - 自動リトライ機構（最大3回、1分間隔）
   
3. 競合ログ出力
   - どの項目で競合が発生したかを記録
   - JSON形式で保存

【使用方法】
    python integrate_data.py

【作成日】2025-11-20
【バージョン】V2.1
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
import pandas as pd
import logging

# Phase 1の共通モジュールをインポート
sys.path.append(str(Path(__file__).parent.parent / 'phase1'))
from common import load_config, setup_logger, error_handler
from file_handler import read_excel_safe, write_excel_safe, check_file_locked, create_backup_file


class DataIntegrator:
    """統合処理クラス（V2.1改良版）"""
    
    def __init__(self, config_path: str = None):
        """
        初期化
        
        Args:
            config_path (str): 設定ファイルのパス（デフォルトは phase1/config.json）
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'phase1' / 'config.json'
        
        self.config = load_config(str(config_path))
        
        # ディレクトリパス
        base_dir = Path(__file__).parent.parent.parent
        self.master_dir = base_dir / self.config['paths']['master_dir']
        self.work_dir = base_dir / self.config['paths']['work_dir']
        self.backup_dir = base_dir / self.config['paths']['backup_dir']
        self.log_dir = base_dir / self.config['paths']['log_dir']
        
        # ロガーの設定（log_dirを文字列で渡す）
        self.logger = setup_logger('integrate', str(self.log_dir), self.config)
        
        # 設定値
        self.max_retry = self.config.get('file_settings', {}).get('file_lock_retry', 3)
        self.retry_interval = self.config.get('file_settings', {}).get('file_lock_wait', 60)
        
        self.logger.info("DataIntegrator 初期化完了")
    
    def load_master_data(self) -> pd.DataFrame:
        """
        マスターデータを読み込み
        
        Returns:
            pd.DataFrame: マスターデータ
        """
        master_file = self.master_dir / self.config['file_settings']['master_file_name']
        sheet_name = self.config['file_settings']['sheet_name']
        
        if not master_file.exists():
            self.logger.warning(f"マスターファイルが存在しません: {master_file}")
            return pd.DataFrame()
        
        df = read_excel_safe(master_file, sheet_name)
        
        if df is not None:
            self.logger.info(f"マスターデータ読み込み: {len(df)}件")
            return df
        else:
            self.logger.warning("マスターデータの読み込みに失敗しました")
            return pd.DataFrame()
    
    def load_user_data(self, user_name: str) -> pd.DataFrame:
        """
        ユーザーのデータを読み込み
        
        Args:
            user_name (str): ユーザー名
            
        Returns:
            pd.DataFrame: ユーザーデータ
        """
        # ユーザー情報を取得
        user_info = None
        for user in self.config['users']:
            if user['name'] == user_name:
                user_info = user
                break
        
        if user_info is None:
            self.logger.error(f"ユーザー '{user_name}' が見つかりません")
            return pd.DataFrame()
        
        # ファイルパスを構築
        user_file = self.work_dir / f"案件管理台帳_マスター_{user_info['file_prefix']}.xlsx"
        sheet_name = self.config['file_settings']['sheet_name']
        
        if not user_file.exists():
            self.logger.debug(f"ユーザーファイルが存在しません: {user_file}")
            return pd.DataFrame()
        
        df = read_excel_safe(user_file, sheet_name)
        
        if df is not None and not df.empty:
            self.logger.info(f"ユーザーデータ読み込み ({user_name}): {len(df)}件")
            return df
        else:
            self.logger.debug(f"ユーザーデータなし: {user_name}")
            return pd.DataFrame()
    
    def merge_with_field_level_resolution(self, 
                                         master_df: pd.DataFrame, 
                                         user_dfs: list) -> pd.DataFrame:
        """
        項目単位で最新のデータをマージ（V2.1の新機能）
        
        同じ案件を複数人が更新した場合、各項目ごとに最新のタイムスタンプを持つ値を採用する。
        これにより、異なる項目を更新した場合でもデータロストが発生しない。
        
        Args:
            master_df (pd.DataFrame): マスターデータ
            user_dfs (list): 各ユーザーのデータフレームのリスト
            
        Returns:
            pd.DataFrame: マージ結果
        """
        self.logger.info("=" * 60)
        self.logger.info("項目単位マージ開始（V2.1機能）")
        self.logger.info("=" * 60)
        
        # 競合ログ
        conflicts_log = []
        
        # 全データを結合（マスター + 全ユーザー）
        all_dfs = [master_df] + user_dfs if not master_df.empty else user_dfs
        
        if not all_dfs:
            self.logger.warning("マージ対象データがありません")
            return pd.DataFrame()
        
        # 全データを結合
        all_data = pd.concat(all_dfs, ignore_index=True)
        
        # 案件番号でグループ化
        if '案件番号' not in all_data.columns:
            self.logger.error("'案件番号' 列が存在しません")
            return pd.DataFrame()
        
        grouped = all_data.groupby('案件番号')
        merged_rows = []
        
        for case_no, group in grouped:
            if len(group) == 1:
                # 競合なし（1つのデータソースのみ）
                merged_rows.append(group.iloc[0].to_dict())
                continue
            
            # 競合あり - 項目単位でマージ
            merged_row = {}
            conflict_detected = False
            conflict_details = []
            
            # 案件番号は固定
            merged_row['案件番号'] = case_no
            
            # 各項目について、最新のタイムスタンプを持つ値を採用
            for column in group.columns:
                if column in ['案件番号', '最終更新日時', '更新者']:
                    continue
                
                # 各行の値とタイムスタンプを取得
                values = []
                for idx, row in group.iterrows():
                    value = row[column]
                    timestamp = row.get('最終更新日時', pd.NaT)
                    updater = row.get('更新者', '不明')
                    
                    values.append({
                        'value': value,
                        'timestamp': timestamp,
                        'updater': updater
                    })
                
                # 空でない値のみを対象
                non_empty_values = [
                    v for v in values 
                    if pd.notna(v['value']) and str(v['value']).strip() != ''
                ]
                
                if not non_empty_values:
                    merged_row[column] = ''
                    continue
                
                # 最新のタイムスタンプを持つ値を採用
                latest = max(
                    non_empty_values, 
                    key=lambda x: x['timestamp'] if pd.notna(x['timestamp']) else pd.Timestamp.min
                )
                merged_row[column] = latest['value']
                
                # 競合があるかチェック（複数の異なる値がある場合）
                unique_values = set([str(v['value']) for v in non_empty_values])
                if len(unique_values) > 1:
                    conflict_detected = True
                    conflict_details.append({
                        'column': column,
                        'values': non_empty_values,
                        'selected': latest
                    })
            
            # 最終更新日時と更新者は最新のものを設定
            if '最終更新日時' in group.columns:
                latest_idx = group['最終更新日時'].idxmax()
                latest_row = group.loc[latest_idx]
                merged_row['最終更新日時'] = latest_row.get('最終更新日時', datetime.now())
                merged_row['更新者'] = latest_row.get('更新者', '不明')
            else:
                merged_row['最終更新日時'] = datetime.now()
                merged_row['更新者'] = '統合処理'
            
            merged_rows.append(merged_row)
            
            # 競合をログに記録
            if conflict_detected:
                conflicts_log.append({
                    'case_number': case_no,
                    'conflicts': conflict_details,
                    'timestamp': datetime.now().isoformat()
                })
                
                self.logger.warning(f"競合検出: {case_no}")
                for conflict in conflict_details:
                    self.logger.warning(f"  項目: {conflict['column']}")
                    for v in conflict['values']:
                        timestamp_str = v['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(v['timestamp']) else '不明'
                        self.logger.warning(f"    - {v['updater']}: {v['value']} ({timestamp_str})")
                    self.logger.warning(f"  → 採用: {conflict['selected']['updater']}の値")
        
        # 競合ログを保存
        if conflicts_log:
            conflict_log_file = self.log_dir / f"conflicts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(conflict_log_file, 'w', encoding='utf-8') as f:
                json.dump(conflicts_log, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"競合ログ保存: {conflict_log_file}")
        
        # DataFrameに変換
        merged_df = pd.DataFrame(merged_rows)
        
        self.logger.info(f"マージ完了: {len(merged_df)}件（競合: {len(conflicts_log)}件）")
        self.logger.info("=" * 60)
        
        return merged_df
    
    def save_master_data(self, df: pd.DataFrame) -> bool:
        """
        マスターデータを保存
        
        Args:
            df (pd.DataFrame): 保存するデータ
            
        Returns:
            bool: 成功した場合True
        """
        master_file = self.master_dir / self.config['file_settings']['master_file_name']
        sheet_name = self.config['file_settings']['sheet_name']
        
        # バックアップ作成
        if master_file.exists():
            backup_path = create_backup_file(master_file, self.backup_dir)
            if backup_path:
                self.logger.info(f"バックアップ作成: {backup_path.name}")
        
        # 保存
        success = write_excel_safe(master_file, df, sheet_name)
        
        if success:
            self.logger.info(f"マスターデータ保存完了: {len(df)}件")
            return True
        else:
            self.logger.error("マスターデータの保存に失敗しました")
            return False
    
    def check_all_files_accessible(self) -> list:
        """
        全てのファイルがアクセス可能かチェック
        
        Returns:
            list: ロックされているユーザー名のリスト
        """
        locked_users = []
        
        # マスターファイルのチェック
        master_file = self.master_dir / self.config['file_settings']['master_file_name']
        if master_file.exists() and check_file_locked(master_file):
            locked_users.append('マスター')
        
        # 各ユーザーファイルのチェック
        for user in self.config['users']:
            user_file = self.work_dir / f"案件管理台帳_マスター_{user['file_prefix']}.xlsx"
            
            if not user_file.exists():
                continue
            
            if check_file_locked(user_file):
                locked_users.append(user['name'])
        
        return locked_users
    
    def send_alert_email(self, subject: str, message: str):
        """
        アラートメール送信
        
        Args:
            subject (str): メール件名
            message (str): メール本文
        """
        email_settings = self.config.get('email_settings', {})
        
        if not email_settings:
            self.logger.info("メール設定が見つかりません（送信スキップ）")
            return
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = f'[貿易DX] {subject}'
            msg['From'] = email_settings.get('from_address', 'tradedx@example.com')
            msg['To'] = ', '.join(email_settings.get('alert_recipients', []))
            
            # SMTP設定
            smtp_server = email_settings.get('smtp_server', 'smtp.example.com')
            smtp_port = email_settings.get('smtp_port', 587)
            use_tls = email_settings.get('use_tls', True)
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if use_tls:
                    server.starttls()
                server.send_message(msg)
            
            self.logger.info(f"アラートメール送信: {subject}")
            
        except Exception as e:
            self.logger.error(f"メール送信エラー: {e}")
    
    def integrate_all_data(self) -> bool:
        """
        全データを統合（V2.1版）
        
        Returns:
            bool: 成功した場合True
        """
        self.logger.info("=" * 60)
        self.logger.info("データ統合開始（V2.1 - 項目単位マージ）")
        self.logger.info("=" * 60)
        
        try:
            # マスター読み込み
            master_df = self.load_master_data()
            
            # 各ユーザーのデータ読み込み
            user_dfs = []
            for user in self.config['users']:
                user_df = self.load_user_data(user['name'])
                if not user_df.empty:
                    # 更新者を記録（列がない場合は追加）
                    if '更新者' not in user_df.columns:
                        user_df['更新者'] = user['name']
                    else:
                        user_df['更新者'] = user_df['更新者'].fillna(user['name'])
                    
                    # 最終更新日時がない場合は現在時刻を設定
                    if '最終更新日時' not in user_df.columns:
                        user_df['最終更新日時'] = datetime.now()
                    
                    user_dfs.append(user_df)
            
            if not user_dfs:
                self.logger.info("統合対象データなし")
                return True
            
            # 項目単位でマージ（V2.1の新機能）
            merged_df = self.merge_with_field_level_resolution(master_df, user_dfs)
            
            if merged_df.empty:
                self.logger.warning("マージ結果が空です")
                return False
            
            # マスターに保存
            success = self.save_master_data(merged_df)
            
            if success:
                self.logger.info(f"統合完了: {len(merged_df)}件")
                self.logger.info("=" * 60)
            
            return success
            
        except Exception as e:
            self.logger.error(f"統合エラー: {e}", exc_info=True)
            return False
    
    def integrate_with_retry(self) -> bool:
        """
        リトライ機能付き統合処理
        
        ファイルがロックされている場合、自動的にリトライする。
        最大リトライ回数に達した場合は、アラートメールを送信する。
        
        Returns:
            bool: 成功した場合True
        """
        self.logger.info("=" * 70)
        self.logger.info("統合処理開始（リトライ機能付き）")
        self.logger.info(f"最大リトライ回数: {self.max_retry}")
        self.logger.info(f"リトライ間隔: {self.retry_interval}秒")
        self.logger.info("=" * 70)
        
        for attempt in range(self.max_retry):
            self.logger.info(f"\n試行 {attempt + 1}/{self.max_retry}")
            
            # ファイルロックチェック
            locked_users = self.check_all_files_accessible()
            
            if not locked_users:
                # 全てのファイルがアクセス可能
                self.logger.info("✓ 全ファイルがアクセス可能")
                
                # 統合実行
                success = self.integrate_all_data()
                
                if success:
                    self.logger.info("✓ 統合成功")
                    return True
                else:
                    # 統合失敗（ファイルロック以外のエラー）
                    if attempt < self.max_retry - 1:
                        self.logger.warning(f"統合失敗。{self.retry_interval}秒後にリトライ...")
                        time.sleep(self.retry_interval)
                    else:
                        self.logger.error("最大リトライ回数に達しました（統合エラー）")
                        self.send_alert_email(
                            "統合失敗",
                            "データ統合処理がエラーにより失敗しました。\n\nログファイルを確認してください。"
                        )
                        return False
            else:
                # 一部のファイルがロック中
                self.logger.warning(f"✗ ファイルがロック中: {', '.join(locked_users)}")
                
                if attempt < self.max_retry - 1:
                    self.logger.info(f"{self.retry_interval}秒後にリトライ...")
                    time.sleep(self.retry_interval)
                else:
                    # 最終リトライでも失敗
                    self.logger.error("最大リトライ回数に達しました（ファイルロック）")
                    
                    # アラートメール送信
                    alert_message = f"""データ統合処理が失敗しました。

ロック中のファイル:
{chr(10).join([f"  - {user}" for user in locked_users])}

対処方法:
1. 該当ユーザーにファイルを閉じてもらう
2. 手動で統合スクリプトを再実行する

実行コマンド:
  cd scripts/phase4
  python integrate_data.py
"""
                    self.send_alert_email("統合失敗（ファイルロック）", alert_message)
                    return False
        
        return False


def main():
    """メイン処理"""
    print("=" * 70)
    print("統合処理スクリプト（V2.1 - 改良版）")
    print("Phase 4: 項目単位の競合解決とリトライ機構")
    print("=" * 70)
    print()
    
    try:
        integrator = DataIntegrator()
        
        # リトライ機能付き統合実行
        success = integrator.integrate_with_retry()
        
        if success:
            print("\n✓ 統合処理が正常に完了しました")
            exit(0)
        else:
            print("\n✗ 統合処理が失敗しました")
            exit(1)
        
    except KeyboardInterrupt:
        print("\n\n処理が中断されました")
        exit(130)
    except Exception as e:
        print(f"\n✗ 致命的エラー: {e}")
        logging.error(f"致命的エラー: {e}", exc_info=True)
        exit(2)


if __name__ == "__main__":
    main()

