@echo off
chcp 65001 > nul
REM 案件番号採番サーバー起動スクリプト

echo ========================================
echo 案件番号採番サーバーを起動します
echo ========================================
echo.

cd /d %~dp0

REM Pythonの確認
python --version > nul 2>&1
if errorlevel 1 (
    echo [エラー] Pythonが見つかりません
    echo Pythonがインストールされているか確認してください
    pause
    exit /b 1
)

echo [OK] Python が見つかりました
echo.

REM サーバーの起動
echo サーバーを起動しています...
echo ホスト: localhost
echo ポート: 8080
echo.
echo Ctrl+C で停止します
echo ========================================
echo.

python case_number_server.py --host localhost --port 8080

pause


