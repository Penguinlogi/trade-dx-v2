@echo off
REM バックエンドテスト実行スクリプト
chcp 65001 > nul

echo ========================================
echo バックエンドテスト実行
echo ========================================
echo.

REM 仮想環境の確認
if not exist venv\Scripts\python.exe (
    echo [エラー] 仮想環境が見つかりません
    echo venv ディレクトリで仮想環境を作成してください
    echo.
    echo 以下のコマンドで仮想環境を作成してください:
    echo   python -m venv venv
    echo   venv\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [実行中] テストを実行しています...
echo.

REM pytest-covがインストールされているか確認
venv\Scripts\python.exe -c "import pytest_cov" 2>nul
if errorlevel 1 (
    echo [警告] pytest-covがインストールされていません
    echo [インストール中] pytest-covをインストールしています...
    venv\Scripts\python.exe -m pip install pytest-cov
    if errorlevel 1 (
        echo [エラー] pytest-covのインストールに失敗しました
        echo [実行] カバレッジなしでテストを実行します...
        echo.
        venv\Scripts\python.exe -m pytest tests/ -v
    ) else (
        echo [完了] pytest-covのインストールが完了しました
        echo.
        REM カバレッジ付きでテスト実行
        venv\Scripts\python.exe -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term
    )
) else (
    REM カバレッジ付きでテスト実行
    venv\Scripts\python.exe -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term
)

if errorlevel 1 (
    echo.
    echo [エラー] テストの実行中にエラーが発生しました
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo テスト完了
echo ========================================
echo.
echo カバレッジレポートは htmlcov/index.html で確認できます
echo.

pause
