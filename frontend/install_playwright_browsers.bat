@echo off
chcp 65001 >nul
echo ========================================
echo Playwrightブラウザのインストール
echo ========================================
echo.
echo セキュリティソフトがブラウザを検疫に移動した場合、
echo このスクリプトでブラウザを再インストールします。
echo.

cd /d "%~dp0"

echo [実行中] Playwrightブラウザをインストールしています...
echo.

npx playwright install

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo [成功] ブラウザのインストールが完了しました
    echo.
    echo 注意: セキュリティソフトの除外設定に以下を追加してください:
    echo   C:\Users\%USERNAME%\AppData\Local\ms-playwright\
) else (
    echo [エラー] ブラウザのインストール中にエラーが発生しました
)
echo ========================================
pause






