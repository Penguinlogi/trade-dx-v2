@echo off
chcp 65001 >nul
echo ========================================
echo email-validator インストール
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [エラー] 仮想環境が見つかりません
    echo 仮想環境を作成してください: python -m venv venv
    pause
    exit /b 1
)

echo [実行中] email-validatorをインストールしています...
echo.

venv\Scripts\python.exe -m pip install email-validator==2.1.0

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo [成功] email-validatorのインストールが完了しました
) else (
    echo [エラー] インストール中にエラーが発生しました
)
echo ========================================
pause




