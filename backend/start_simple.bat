@echo off
REM シンプルなバックエンドサーバー起動スクリプト
chcp 65001 > nul

echo ====================================
echo 貿易DX バックエンドサーバー起動（簡易版）
echo ====================================
echo.

REM 仮想環境のPythonを直接使用してサーバーを起動
if exist "venv\Scripts\python.exe" (
    echo 仮想環境のPythonを使用してサーバーを起動します...
    echo.
    echo サーバーURL: http://localhost:8000
    echo API ドキュメント: http://localhost:8000/docs
    echo.
    echo 停止するには Ctrl+C を押してください
    echo.
    echo ====================================
    echo.

    venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo [エラー] 仮想環境が見つかりません。
    echo.
    echo 以下のコマンドで仮想環境を作成してください:
    echo   python -m venv venv
    echo   venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
