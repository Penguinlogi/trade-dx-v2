@echo off
REM テスト用依存関係のインストールスクリプト
chcp 65001 > nul

echo ========================================
echo テスト用依存関係のインストール
echo ========================================
echo.

if not exist venv\Scripts\python.exe (
    echo [エラー] 仮想環境が見つかりません
    echo 先に仮想環境を作成してください
    pause
    exit /b 1
)

echo [インストール中] テスト用ライブラリをインストールしています...
echo.

venv\Scripts\python.exe -m pip install pytest pytest-asyncio pytest-cov httpx

if errorlevel 1 (
    echo.
    echo [エラー] インストールに失敗しました
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo インストール完了
echo ========================================
echo.
echo 以下のコマンドでテストを実行できます:
echo   run_tests.bat
echo.
pause
