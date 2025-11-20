#!/bin/bash
# 差分同期スクリプト実行シェルスクリプト

echo "=========================================="
echo "差分同期スクリプト実行"
echo "=========================================="
echo ""

# Pythonの存在確認
if ! command -v python3 &> /dev/null; then
    echo "[エラー] Python3が見つかりません"
    echo "Python 3.8以上をインストールしてください"
    exit 1
fi

echo "[実行] 差分同期を開始します..."
echo ""

# スクリプトディレクトリに移動
cd "$(dirname "$0")"

# スクリプトの実行
python3 incremental_sync.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[成功] 差分同期が完了しました"
else
    echo ""
    echo "[エラー] 差分同期中にエラーが発生しました（終了コード: $?）"
    echo "ログファイルを確認してください"
    exit 1
fi

echo ""
echo "=========================================="

