@echo off
chcp 65001 > nul
echo ========================================
echo フェーズ2 クイックテスト
echo ========================================
echo.
echo このスクリプトは、サーバーが起動している前提で実行してください。
echo.
echo サーバーを起動していない場合は、別のウィンドウで以下を実行：
echo   cd scripts\phase2
echo   python case_number_server.py
echo.
pause
echo.
echo ========================================
echo テスト開始
echo ========================================
echo.

echo [1] ヘルスチェック
python -c "import requests; r = requests.get('http://localhost:8080/health'); print('Status:', r.status_code); print(r.json())"
echo.

echo [2] 輸出案件番号を生成
python -c "import requests; r = requests.get('http://localhost:8080/generate?type=EX&user=test'); print('Status:', r.status_code); print(r.json())"
echo.

echo [3] 輸入案件番号を生成
python -c "import requests; r = requests.get('http://localhost:8080/generate?type=IM&user=test'); print('Status:', r.status_code); print(r.json())"
echo.

echo [4] 三国間案件番号を生成
python -c "import requests; r = requests.get('http://localhost:8080/generate?type=TR&user=test'); print('Status:', r.status_code); print(r.json())"
echo.

echo [5] 国内輸送案件番号を生成
python -c "import requests; r = requests.get('http://localhost:8080/generate?type=DO&user=test'); print('Status:', r.status_code); print(r.json())"
echo.

echo [6] ステータス確認
python -c "import requests; r = requests.get('http://localhost:8080/status'); print('Status:', r.status_code); import json; print(json.dumps(r.json(), indent=2, ensure_ascii=False))"
echo.

echo ========================================
echo テスト完了
echo ========================================
echo.
echo 上記の結果を確認してください：
echo - ヘルスチェック: "status": "healthy" が表示されること
echo - 案件番号生成: "success": true と案件番号が表示されること
echo - ステータス: カウンターの値が表示されること
echo.
pause

