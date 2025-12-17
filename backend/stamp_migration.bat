@echo off
REM マイグレーション履歴を記録するスクリプト
chcp 65001 > nul
echo ====================================
echo データベースを最新のマイグレーション状態としてマーク
echo ====================================
echo.
echo 注意: このスクリプトは既存のデータベースに対して
echo マイグレーション履歴を記録するだけです。
echo テーブルの作成や変更は行いません。
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

echo [2/2] マイグレーション履歴を記録中...
echo.
python -m alembic stamp head

echo.
echo ====================================
echo 完了: データベースは最新のマイグレーション状態としてマークされました
echo ====================================
echo.
echo 次のステップ:
echo   1. バックエンドサーバーを再起動
echo   2. 案件を削除して動作確認
echo   3. 変更履歴ページで削除履歴が1件のみ表示されることを確認
echo.
pause








