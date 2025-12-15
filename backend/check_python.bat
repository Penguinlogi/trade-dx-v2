@echo off
REM Python環境の確認スクリプト
chcp 65001 > nul
echo ====================================
echo Python環境の確認
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

echo.
echo [2/3] Pythonのパスを確認中...
echo.
where python
echo.
python --version
echo.

echo [3/3] FastAPIのインストール状況を確認中...
echo.
python -c "import sys; print('Pythonパス:', sys.executable)"
python -c "import fastapi; print('FastAPIバージョン:', fastapi.__version__)"
python -c "import uvicorn; print('Uvicorn OK')"
echo.

echo ====================================
echo 確認完了
echo ====================================
pause






