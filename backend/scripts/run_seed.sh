#!/bin/bash
# シードデータ投入スクリプト実行用シェルスクリプト

echo "========================================"
echo "シードデータ投入スクリプト"
echo "========================================"
echo

cd "$(dirname "$0")/.."

echo "[1/2] シードデータを投入中..."
python scripts/seed_data.py
if [ $? -ne 0 ]; then
    echo
    echo "エラー: シードデータの投入に失敗しました"
    exit 1
fi

echo
echo "[2/2] テストデータを投入中..."
python scripts/test_data.py
if [ $? -ne 0 ]; then
    echo
    echo "エラー: テストデータの投入に失敗しました"
    exit 1
fi

echo
echo "========================================"
echo "すべてのデータ投入が完了しました"
echo "========================================"












