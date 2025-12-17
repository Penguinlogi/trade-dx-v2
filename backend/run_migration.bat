@echo off
REM マイグレーション実行スクリプト
chcp 65001 > nul
echo ====================================
echo データベースマイグレーション実行
echo ====================================
echo.

REM 仮想環境のアクティベート
if exist "venv\Scripts\activate.bat" (
    echo [1/2] 仮想環境をアクティベート中...
    call venv\Scripts\activate.bat
) else (
    echo [エラー] 仮想環境が見つかりません。
    pause
    exit /b 1
)

REM マイグレーション実行
echo [2/2] マイグレーションを実行中...
echo.
python -m alembic upgrade head

echo.
echo ====================================
echo マイグレーション完了
echo ====================================
pause








