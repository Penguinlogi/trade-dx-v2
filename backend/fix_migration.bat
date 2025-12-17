@echo off
REM マイグレーション修正スクリプト
chcp 65001 > nul
echo ====================================
echo データベースマイグレーション修正
echo ====================================
echo.

REM 仮想環境のアクティベート
if exist "venv\Scripts\activate.bat" (
    echo [1/3] 仮想環境をアクティベート中...
    call venv\Scripts\activate.bat
) else (
    echo [エラー] 仮想環境が見つかりません。
    pause
    exit /b 1
)

echo [2/3] 現在のマイグレーション状態を確認中...
python -m alembic current

echo.
echo [3/3] マイグレーションを適用中...
echo.
python -m alembic upgrade head

echo.
echo ====================================
if errorlevel 1 (
    echo マイグレーション適用に失敗しました。
    echo.
    echo データベースが既に存在する場合、以下のコマンドで
    echo データベースを最新のマイグレーション状態としてマークできます:
    echo   python -m alembic stamp head
) else (
    echo マイグレーション適用完了
)
echo ====================================
pause








