@echo off
chcp 65001 >nul
echo ========================================
echo 統合テスト実行（デバッグモード）
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [エラー] 仮想環境が見つかりません
    echo 仮想環境を作成してください: python -m venv venv
    pause
    exit /b 1
)

echo [実行中] 統合テストを実行しています...
echo.

venv\Scripts\python.exe -m pytest tests/test_integration.py::TestIntegration::test_case_workflow -v -s

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo [成功] テストが正常に完了しました
) else (
    echo [エラー] テストの実行中にエラーが発生しました
)
echo ========================================
pause




