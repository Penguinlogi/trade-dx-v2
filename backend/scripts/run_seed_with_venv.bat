@echo off
REM シードデータ投入スクリプト（仮想環境使用版）
chcp 65001 > nul
echo ========================================
echo シードデータ投入スクリプト
echo ========================================
echo.

REM 現在のディレクトリを確認
cd /d %~dp0..

REM 仮想環境のアクティベート
if exist "venv\Scripts\activate.bat" (
    echo [1/3] 仮想環境をアクティベート中...
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
    pause
    exit /b 1
)

REM Pythonのバージョン確認
echo [2/3] Pythonのバージョンを確認中...
python --version
if errorlevel 1 (
    echo [エラー] Pythonが見つかりません。
    pause
    exit /b 1
)

REM シードデータ投入
echo [3/3] シードデータを投入中...
python scripts\seed_data.py
if errorlevel 1 (
    echo.
    echo [エラー] シードデータの投入に失敗しました。
    pause
    exit /b 1
)

echo.
echo ========================================
echo シードデータ投入が完了しました
echo ========================================
echo.
echo 以下のアカウントでログインできます:
echo   ユーザー名: admin / パスワード: admin123
echo   ユーザー名: yamada / パスワード: yamada123
echo   ユーザー名: suzuki / パスワード: suzuki123
echo.
pause





