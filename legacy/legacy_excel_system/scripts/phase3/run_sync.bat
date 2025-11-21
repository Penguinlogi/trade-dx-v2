@echo off
chcp 65001 > nul
REM 差分同期スクリプト実行バッチファイル

echo ==========================================
echo 差分同期スクリプト実行
echo ==========================================
echo.

REM Pythonの存在確認
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [エラー] Pythonが見つかりません
    echo Python 3.8以上をインストールしてください
    pause
    exit /b 1
)

echo [実行] 差分同期を開始します...
echo.

REM スクリプトの実行
python "%~dp0incremental_sync.py"

if %ERRORLEVEL% equ 0 (
    echo.
    echo [成功] 差分同期が完了しました
) else (
    echo.
    echo [エラー] 差分同期中にエラーが発生しました（終了コード: %ERRORLEVEL%）
    echo ログファイルを確認してください
)

echo.
echo ==========================================
pause

