#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案件番号採番サーバー (case_number_server.py)
Phase 2で実装

中央集権型の案件番号採番サーバー
HTTPサーバーとして動作し、複数クライアントから同時アクセスを受け付ける
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import sys
import traceback

# Phase1の共通モジュールを使用
sys.path.append('../phase1')
try:
    from common import setup_logger, get_timestamp
except ImportError:
    # 開発環境でのフォールバック
    def setup_logger(name, log_dir, config):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def get_timestamp(format_str='%Y%m%d_%H%M%S'):
        return datetime.now().strftime(format_str)


class CaseNumberManager:
    """
    案件番号管理クラス
    
    スレッドセーフな案件番号採番機能を提供
    """
    
    def __init__(self, data_file: str = "./case_numbers.json", logger=None):
        """
        初期化
        
        Args:
            data_file: 案件番号データファイルのパス
            logger: ロガーインスタンス
        """
        self.data_file = Path(data_file)
        self.lock = threading.Lock()
        self.logger = logger or logging.getLogger(__name__)
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """
        データファイルを読み込む
        
        Returns:
            案件番号データ辞書
        """
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"データファイルを読み込みました: {self.data_file}")
                    return data
            except Exception as e:
                self.logger.error(f"データファイルの読み込みに失敗: {e}")
                return self._create_initial_data()
        else:
            self.logger.info("データファイルが存在しないため、新規作成します")
            return self._create_initial_data()
    
    def _create_initial_data(self) -> dict:
        """
        初期データ構造を作成
        
        Returns:
            初期化された案件番号データ辞書
        """
        return {
            "EX": {  # 輸出
                "counter": 0,
                "last_generated": None
            },
            "IM": {  # 輸入
                "counter": 0,
                "last_generated": None
            },
            "TR": {  # 三国間
                "counter": 0,
                "last_generated": None
            },
            "DO": {  # 国内輸送
                "counter": 0,
                "last_generated": None
            },
            "history": []  # 生成履歴（最新100件）
        }
    
    def _save_data(self):
        """
        データファイルに保存
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            self.logger.info("データファイルを保存しました")
        except Exception as e:
            self.logger.error(f"データファイルの保存に失敗: {e}")
            raise
    
    def generate_case_number(self, case_type: str, user: str) -> dict:
        """
        案件番号を生成
        
        Args:
            case_type: 案件種別 (EX, IM, TR, DO)
            user: ユーザー名
        
        Returns:
            生成結果辞書 {success: bool, case_number: str, message: str}
        """
        # 入力検証
        if case_type not in ['EX', 'IM', 'TR', 'DO']:
            return {
                'success': False,
                'case_number': None,
                'message': f'無効な案件種別です: {case_type}'
            }
        
        with self.lock:  # スレッドセーフに処理
            try:
                # カウンターをインクリメント
                self.data[case_type]['counter'] += 1
                counter = self.data[case_type]['counter']
                
                # 案件番号を生成 (例: EX-250001)
                year_suffix = datetime.now().strftime('%y')
                case_number = f"{case_type}-{year_suffix}{counter:04d}"
                
                # タイムスタンプ
                timestamp = datetime.now().isoformat()
                
                # 履歴に記録
                history_entry = {
                    'case_number': case_number,
                    'case_type': case_type,
                    'user': user,
                    'timestamp': timestamp,
                    'counter': counter
                }
                
                self.data[case_type]['last_generated'] = timestamp
                self.data['history'].append(history_entry)
                
                # 履歴は最新100件のみ保持
                if len(self.data['history']) > 100:
                    self.data['history'] = self.data['history'][-100:]
                
                # ファイルに保存
                self._save_data()
                
                self.logger.info(f"案件番号を生成しました: {case_number} (ユーザー: {user})")
                
                return {
                    'success': True,
                    'case_number': case_number,
                    'message': '案件番号を生成しました',
                    'timestamp': timestamp
                }
                
            except Exception as e:
                self.logger.error(f"案件番号生成エラー: {e}")
                return {
                    'success': False,
                    'case_number': None,
                    'message': f'エラーが発生しました: {str(e)}'
                }
    
    def get_status(self) -> dict:
        """
        現在のステータスを取得
        
        Returns:
            ステータス辞書
        """
        with self.lock:
            return {
                'success': True,
                'counters': {
                    case_type: {
                        'counter': self.data[case_type]['counter'],
                        'last_generated': self.data[case_type]['last_generated']
                    }
                    for case_type in ['EX', 'IM', 'TR', 'DO']
                },
                'history_count': len(self.data['history']),
                'latest_history': self.data['history'][-10:] if self.data['history'] else []
            }
    
    def reset_counter(self, case_type: str = None) -> dict:
        """
        カウンターをリセット（管理用）
        
        Args:
            case_type: リセットする案件種別（Noneの場合は全て）
        
        Returns:
            結果辞書
        """
        with self.lock:
            try:
                if case_type:
                    if case_type in ['EX', 'IM', 'TR', 'DO']:
                        self.data[case_type]['counter'] = 0
                        self.data[case_type]['last_generated'] = None
                        message = f'{case_type}のカウンターをリセットしました'
                    else:
                        return {'success': False, 'message': '無効な案件種別です'}
                else:
                    for ct in ['EX', 'IM', 'TR', 'DO']:
                        self.data[ct]['counter'] = 0
                        self.data[ct]['last_generated'] = None
                    message = '全てのカウンターをリセットしました'
                
                self._save_data()
                self.logger.warning(f"カウンターリセット: {message}")
                
                return {'success': True, 'message': message}
                
            except Exception as e:
                return {'success': False, 'message': str(e)}


class CaseNumberRequestHandler(BaseHTTPRequestHandler):
    """
    HTTPリクエストハンドラ
    """
    
    def log_message(self, format, *args):
        """
        ログメッセージをカスタマイズ
        """
        self.server.logger.info(f"{self.client_address[0]} - {format % args}")
    
    def _send_json_response(self, data: dict, status_code: int = 200):
        """
        JSON形式でレスポンスを送信
        
        Args:
            data: レスポンスデータ
            status_code: HTTPステータスコード
        """
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')  # CORS対応
        self.end_headers()
        
        response_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def do_GET(self):
        """
        GETリクエストの処理
        """
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_params = parse_qs(parsed_path.query)
            
            # /health - ヘルスチェック
            if path == '/health':
                self._send_json_response({
                    'success': True,
                    'status': 'healthy',
                    'message': 'サーバーは正常に動作しています',
                    'timestamp': datetime.now().isoformat()
                })
            
            # /status - ステータス取得
            elif path == '/status':
                status_data = self.server.manager.get_status()
                self._send_json_response(status_data)
            
            # /generate - 案件番号生成
            elif path == '/generate':
                case_type = query_params.get('type', [None])[0]
                user = query_params.get('user', ['unknown'])[0]
                
                if not case_type:
                    self._send_json_response({
                        'success': False,
                        'message': 'typeパラメータが必要です'
                    }, 400)
                    return
                
                result = self.server.manager.generate_case_number(
                    case_type=case_type.upper(),
                    user=user
                )
                
                status_code = 200 if result['success'] else 400
                self._send_json_response(result, status_code)
            
            # /reset - カウンターリセット（管理用）
            elif path == '/reset':
                case_type = query_params.get('type', [None])[0]
                result = self.server.manager.reset_counter(
                    case_type=case_type.upper() if case_type else None
                )
                
                status_code = 200 if result['success'] else 400
                self._send_json_response(result, status_code)
            
            # その他のパス
            else:
                self._send_json_response({
                    'success': False,
                    'message': 'エンドポイントが見つかりません',
                    'available_endpoints': [
                        '/health - ヘルスチェック',
                        '/status - ステータス取得',
                        '/generate?type=XX&user=YY - 案件番号生成',
                        '/reset?type=XX - カウンターリセット'
                    ]
                }, 404)
        
        except Exception as e:
            self.server.logger.error(f"リクエスト処理エラー: {e}\n{traceback.format_exc()}")
            self._send_json_response({
                'success': False,
                'message': f'サーバーエラー: {str(e)}'
            }, 500)
    
    def do_OPTIONS(self):
        """
        OPTIONSリクエストの処理（CORS対応）
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


class CaseNumberServer:
    """
    案件番号サーバー
    """
    
    def __init__(self, host: str = 'localhost', port: int = 8080,
                 data_file: str = './case_numbers.json', log_dir: str = '../../logs'):
        """
        初期化
        
        Args:
            host: ホスト名
            port: ポート番号
            data_file: データファイルパス
            log_dir: ログディレクトリ
        """
        self.host = host
        self.port = port
        self.data_file = data_file
        
        # ログディレクトリの作成
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # ロガーのセットアップ
        self.logger = logging.getLogger('CaseNumberServer')
        self.logger.setLevel(logging.INFO)
        
        # ファイルハンドラ
        log_file = log_path / f"case_number_server_{datetime.now().strftime('%Y%m%d')}.log"
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # コンソールハンドラ
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # フォーマッター
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
        # 案件番号マネージャーの初期化
        self.manager = CaseNumberManager(data_file=data_file, logger=self.logger)
        
        # HTTPサーバーの作成
        self.httpd = HTTPServer((host, port), CaseNumberRequestHandler)
        self.httpd.logger = self.logger
        self.httpd.manager = self.manager
    
    def start(self):
        """
        サーバーを起動
        """
        self.logger.info("=" * 60)
        self.logger.info("案件番号採番サーバーを起動します")
        self.logger.info(f"ホスト: {self.host}")
        self.logger.info(f"ポート: {self.port}")
        self.logger.info(f"データファイル: {self.data_file}")
        self.logger.info("=" * 60)
        self.logger.info("")
        self.logger.info("利用可能なエンドポイント:")
        self.logger.info(f"  - http://{self.host}:{self.port}/health")
        self.logger.info(f"  - http://{self.host}:{self.port}/status")
        self.logger.info(f"  - http://{self.host}:{self.port}/generate?type=EX&user=yamada")
        self.logger.info("")
        self.logger.info("Ctrl+C で終了します")
        self.logger.info("=" * 60)
        
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.logger.info("\nサーバーを停止します...")
            self.httpd.shutdown()
            self.logger.info("サーバーを停止しました")
    
    def stop(self):
        """
        サーバーを停止
        """
        self.httpd.shutdown()


def main():
    """
    メイン関数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='案件番号採番サーバー')
    parser.add_argument('--host', default='localhost', help='ホスト名（デフォルト: localhost）')
    parser.add_argument('--port', type=int, default=8080, help='ポート番号（デフォルト: 8080）')
    parser.add_argument('--data-file', default='./case_numbers.json',
                       help='データファイルパス（デフォルト: ./case_numbers.json）')
    parser.add_argument('--log-dir', default='../../logs',
                       help='ログディレクトリ（デフォルト: ../../logs）')
    
    args = parser.parse_args()
    
    server = CaseNumberServer(
        host=args.host,
        port=args.port,
        data_file=args.data_file,
        log_dir=args.log_dir
    )
    
    server.start()


if __name__ == '__main__':
    main()

