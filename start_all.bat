@echo off
REM フロントエンドとバックエンドを同時に起動するスクリプト
chcp 65001 > nul
echo ====================================
echo 貿易DX 開発サーバー起動（フロントエンド + バックエンド）
echo ====================================
echo.

REM プロジェクトルートディレクトリに移動
cd /d "%~dp0"

REM 新しいコマンドプロンプトでバックエンドサーバーを起動
echo [1/2] バックエンドサーバーを起動中...
start "貿易DX バックエンドサーバー" cmd /k "cd backend && start_server.bat"

REM 少し待ってからフロントエンドサーバーを起動
timeout /t 3 /nobreak > nul

REM 新しいコマンドプロンプトでフロントエンドサーバーを起動
echo [2/2] フロントエンドサーバーを起動中...
start "貿易DX フロントエンドサーバー" cmd /k "cd frontend && start_frontend.bat"

echo.
echo ====================================
echo 起動完了
echo ====================================
echo.
echo バックエンド: http://localhost:8000
echo フロントエンド: http://localhost:3000
echo API ドキュメント: http://localhost:8000/docs
echo.
echo 各サーバーは別ウィンドウで起動しました。
echo 停止するには各ウィンドウで Ctrl+C を押してください。
echo.
pause






