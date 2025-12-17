@echo off
chcp 65001 >nul
echo ========================================
echo フロントエンドカバレッジレポート生成
echo ========================================
echo.

cd /d "%~dp0"

echo [実行中] カバレッジレポートを生成しています...
echo この処理には数秒かかる場合があります...
echo.

npm run test:coverage

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo [成功] カバレッジレポートが生成されました
    echo ========================================
    echo.
    echo カバレッジレポートは coverage/index.html で確認できます
    echo.
    if exist "coverage\index.html" (
        echo [確認] HTMLレポートファイルが存在します
        echo ブラウザで開くには以下のコマンドを実行してください:
        echo   start coverage\index.html
    ) else (
        echo [警告] HTMLレポートファイルが見つかりません
        echo coverage ディレクトリの内容を確認してください
    )
) else (
    echo.
    echo [エラー] カバレッジレポートの生成中にエラーが発生しました
)

echo.
pause






