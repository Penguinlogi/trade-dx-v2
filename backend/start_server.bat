@echo off
REM バックエンドサーバー起動スクリプト
chcp 65001 > nul
echo ====================================
echo 貿易DX バックエンドサーバー起動
echo ====================================
echo.

REM 仮想環境のアクティベート
if exist "venv\Scripts\activate.bat" (
    echo [1/4] 仮想環境をアクティベート中...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [エラー] 仮想環境のアクティベートに失敗しました。
        pause
        exit /b 1
    )
    echo [完了] 仮想環境がアクティベートされました。
) else (
    echo [エラー] 仮想環境が見つかりません。
    echo.
    echo 以下のコマンドで仮想環境を作成してください:
    echo   python -m venv venv
    echo   venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    echo.
    echo 仮想環境を作成しますか？ (Y/N)
    set /p create_venv=
    if /i "%create_venv%"=="Y" (
        echo [作成中] 仮想環境を作成しています...
        python -m venv venv
        if errorlevel 1 (
            echo [エラー] 仮想環境の作成に失敗しました。
            pause
            exit /b 1
        )
        call venv\Scripts\activate.bat
        echo [インストール中] 必要なライブラリをインストールしています...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo [エラー] ライブラリのインストールに失敗しました。
            pause
            exit /b 1
        )
        echo [完了] 仮想環境の作成とライブラリのインストールが完了しました。
    ) else (
        pause
        exit /b 1
    )
)

REM Pythonのバージョン確認
echo [2/4] Pythonのバージョンを確認中...
venv\Scripts\python.exe --version
if errorlevel 1 (
    echo [エラー] Pythonが見つかりません。
    pause
    exit /b 1
)

REM 必要なライブラリの確認
echo [3/4] 必要なライブラリを確認中...
venv\Scripts\python.exe -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [警告] FastAPIがインストールされていません。
    echo [インストール中] 必要なライブラリをインストールしています...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [エラー] ライブラリのインストールに失敗しました。
        echo.
        echo 手動でインストールしてください:
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo [完了] ライブラリのインストールが完了しました。
) else (
    echo [完了] 必要なライブラリはインストール済みです。
)

REM ポートの確認
echo [4/4] ポート8000の使用状況を確認中...
netstat -ano | findstr :8000 >nul 2>&1
if not errorlevel 1 (
    echo [警告] ポート8000は既に使用されています。
    echo 既存のサーバーを停止するか、別のポートを使用してください。
    echo.
    echo ポートを使用しているプロセスを確認:
    netstat -ano | findstr :8000
    echo.
    echo 続行しますか？ (Y/N)
    set /p continue=
    if /i not "%continue%"=="Y" (
        pause
        exit /b 1
    )
)

REM 仮想環境のPythonが使用されているか確認
echo [確認] 仮想環境のPythonを確認中...
venv\Scripts\python.exe -c "import sys; print('Python:', sys.executable)" 2>nul
if errorlevel 1 (
    echo [警告] Pythonの確認に失敗しました。
)

REM サーバー起動
echo.
echo ====================================
echo サーバーを起動中...
echo ====================================
echo.
echo サーバーURL: http://localhost:8000
echo API ドキュメント: http://localhost:8000/docs
echo.
echo 停止するには Ctrl+C を押してください
echo.
echo ====================================
echo.

REM 仮想環境のPythonを直接使用
venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

if errorlevel 1 (
    echo.
    echo [エラー] サーバーの起動に失敗しました。
    echo エラーメッセージを確認してください。
    echo.
    pause
)
