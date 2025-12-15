@echo off
REM バックエンドカバレッジレポート生成スクリプト
chcp 65001 > nul

echo ========================================
echo バックエンドカバレッジレポート生成
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

echo [実行中] カバレッジレポートを生成しています...
echo.

REM 仮想環境のPythonを使ってpytestを実行
venv\Scripts\python.exe -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term

if errorlevel 1 (
    echo.
    echo [エラー] カバレッジレポートの生成中にエラーが発生しました
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo カバレッジレポート生成完了
echo ========================================
echo.
echo カバレッジレポートは htmlcov/index.html で確認できます
echo ブラウザで開くには以下のコマンドを実行してください:
echo   start htmlcov/index.html
echo.

pause




