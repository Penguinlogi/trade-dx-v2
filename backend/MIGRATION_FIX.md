# マイグレーションエラー修正手順

## エラー: "Target database is not up to date"

このエラーは、データベースが最新のマイグレーション状態にないことを示しています。

## 解決方法

### 方法1: 既存のマイグレーションを適用（推奨）

```bash
cd backend
venv\Scripts\activate.bat
python -m alembic upgrade head
```

または、バッチファイルを使用：

```bash
cd backend
fix_migration.bat
```

### 方法2: データベースを最新状態としてマーク

既存のデータベースが既に正しいスキーマを持っている場合：

```bash
cd backend
venv\Scripts\activate.bat
python -m alembic stamp head
```

これで、データベースを最新のマイグレーション状態としてマークします。

### 方法3: マイグレーションなしで動作確認

SQLiteでは外部キー制約がデフォルトで無効のため、マイグレーションなしでも動作する可能性があります。

1. バックエンドサーバーを再起動
2. 案件を削除して動作確認
3. 変更履歴ページで削除履歴が1件のみ表示されることを確認

## 注意事項

- **重要**: マイグレーションを実行する前に、データベースのバックアップを取ってください
- 既存のデータベースで `case_id` が `nullable=False` の場合、削除処理は正常に動作するはずです（SQLiteでは外部キー制約が無効のため）






