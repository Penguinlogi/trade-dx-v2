#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 手動テストスクリプト

サーバーが起動している状態で実行してください。
"""

import requests
import time
import sys
from datetime import datetime


def print_section(title):
    """セクション見出しを表示"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health_check():
    """ヘルスチェックテスト"""
    print_section("1. ヘルスチェック")
    
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        
        if response.status_code == 200:
            print("✅ ヘルスチェック成功")
            return True
        else:
            print("❌ ヘルスチェック失敗")
            return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        print("\n⚠️ サーバーが起動していません。")
        print("別のターミナルで以下を実行してください:")
        print("  cd scripts/phase2")
        print("  python case_number_server.py")
        return False


def test_generate_case_numbers():
    """案件番号生成テスト"""
    print_section("2. 案件番号生成テスト")
    
    case_types = ['EX', 'IM', 'TR', 'DO']
    generated_numbers = []
    
    for case_type in case_types:
        try:
            response = requests.get(
                "http://localhost:8080/generate",
                params={'type': case_type, 'user': 'test_user'},
                timeout=5
            )
            
            data = response.json()
            
            if data['success']:
                case_number = data['case_number']
                generated_numbers.append(case_number)
                print(f"✅ {case_type}: {case_number}")
            else:
                print(f"❌ {case_type}: {data['message']}")
        
        except Exception as e:
            print(f"❌ {case_type}: エラー - {e}")
    
    return generated_numbers


def test_concurrent_generation():
    """同時生成テスト"""
    print_section("3. 同時生成テスト（10件）")
    
    import threading
    
    results = []
    errors = []
    
    def generate(thread_id):
        try:
            response = requests.get(
                "http://localhost:8080/generate",
                params={'type': 'EX', 'user': f'user_{thread_id}'},
                timeout=5
            )
            data = response.json()
            if data['success']:
                results.append(data['case_number'])
            else:
                errors.append(data['message'])
        except Exception as e:
            errors.append(str(e))
    
    # 10スレッドで同時実行
    threads = []
    for i in range(10):
        thread = threading.Thread(target=generate, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"生成された案件番号: {len(results)}件")
    print(f"エラー: {len(errors)}件")
    
    # 重複チェック
    unique_count = len(set(results))
    print(f"ユニーク数: {unique_count}件")
    
    if unique_count == len(results):
        print("✅ 重複なし")
    else:
        print(f"❌ 重複検出: {len(results) - unique_count}件")
        print(f"案件番号: {results}")
    
    # 最初の5件を表示
    print("\n生成された案件番号（最初の5件）:")
    for i, num in enumerate(results[:5], 1):
        print(f"  {i}. {num}")


def test_status():
    """ステータス取得テスト"""
    print_section("4. ステータス取得")
    
    try:
        response = requests.get("http://localhost:8080/status", timeout=5)
        data = response.json()
        
        print(f"ステータスコード: {response.status_code}")
        print("\nカウンター状態:")
        
        for case_type, info in data['counters'].items():
            counter = info['counter']
            last_gen = info['last_generated']
            print(f"  {case_type}: {counter}件生成")
            if last_gen:
                print(f"      最終生成: {last_gen}")
        
        print(f"\n履歴件数: {data['history_count']}件")
        
        print("✅ ステータス取得成功")
    
    except Exception as e:
        print(f"❌ エラー: {e}")


def test_invalid_request():
    """無効なリクエストのテスト"""
    print_section("5. エラーハンドリングテスト")
    
    # 無効な案件種別
    print("\n5-1. 無効な案件種別")
    try:
        response = requests.get(
            "http://localhost:8080/generate",
            params={'type': 'INVALID', 'user': 'test'},
            timeout=5
        )
        data = response.json()
        
        if not data['success']:
            print(f"✅ 適切にエラーを返しました: {data['message']}")
        else:
            print("❌ エラーが検出されませんでした")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # typeパラメータ欠落
    print("\n5-2. typeパラメータ欠落")
    try:
        response = requests.get(
            "http://localhost:8080/generate",
            params={'user': 'test'},
            timeout=5
        )
        data = response.json()
        
        if not data['success']:
            print(f"✅ 適切にエラーを返しました: {data['message']}")
        else:
            print("❌ エラーが検出されませんでした")
    except Exception as e:
        print(f"❌ エラー: {e}")


def main():
    """メイン関数"""
    print("\n" + "█" * 60)
    print("  Phase 2: 案件番号サーバー 手動テスト")
    print("█" * 60)
    
    print("\n⚠️ このテストを実行する前に、サーバーを起動してください:")
    print("  cd scripts/phase2")
    print("  python case_number_server.py")
    print("\nサーバーが起動したら、Enterキーを押してください...")
    input()
    
    # テスト実行
    if not test_health_check():
        print("\n❌ サーバーに接続できないため、テストを中止します")
        sys.exit(1)
    
    test_generate_case_numbers()
    test_concurrent_generation()
    test_status()
    test_invalid_request()
    
    # 完了
    print_section("テスト完了")
    print("\n✅ 全てのテストが完了しました")
    print("\n次のステップ:")
    print("  1. サーバーを停止（Ctrl+C）")
    print("  2. Phase 3の開発に進む")


if __name__ == '__main__':
    main()


