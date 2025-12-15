@echo off
REM フロントエンド開発サーバー起動スクリプト
chcp 65001 > nul
echo ====================================
echo 貿易DX フロントエンド開発サーバー起動
echo ====================================
echo.

REM 現在のディレクトリがfrontendか確認
if not exist "package.json" (
    echo [エラー] package.json が見つかりません。
    echo frontend ディレクトリで実行してください。
    echo.
    echo 現在のディレクトリ: %CD%
    echo.
    echo 以下のコマンドでfrontendディレクトリに移動してください:
    echo   cd frontend
    echo   start_frontend.bat
    pause
    exit /b 1
)

REM node_modulesの確認
if not exist "node_modules" (
    echo [警告] node_modulesが見つかりません。
    echo 依存関係をインストールします...
    echo.
    call npm install
    if errorlevel 1 (
        echo [エラー] 依存関係のインストールに失敗しました。
        pause
        exit /b 1
    )
    echo [完了] 依存関係のインストールが完了しました。
    echo.
)

REM 開発サーバー起動
echo [起動中] 開発サーバーを起動します...
echo.
echo サーバーURL: http://localhost:3000
echo.
echo 停止するには Ctrl+C を押してください
echo.

call npm run dev

pause






