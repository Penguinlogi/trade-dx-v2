#!/bin/bash
# 案件番号採番サーバー起動スクリプト（Linux/Mac用）

echo "========================================"
echo "案件番号採番サーバーを起動します"
echo "========================================"
echo ""

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# Pythonの確認
if ! command -v python3 &> /dev/null; then
    echo "[エラー] Python3が見つかりません"
    echo "Python3をインストールしてください"
    exit 1
fi

echo "[OK] Python3 が見つかりました"
echo ""

# サーバーの起動
echo "サーバーを起動しています..."
echo "ホスト: localhost"
echo "ポート: 8080"
echo ""
echo "Ctrl+C で停止します"
echo "========================================"
echo ""

python3 case_number_server.py --host localhost --port 8080


