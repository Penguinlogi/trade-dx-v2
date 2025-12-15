# データベースマイグレーション手順

## 問題: "Target database is not up to date"

このエラーは、データベースが最新のマイグレーション状態にないことを示しています。

## 解決方法

### ステップ1: 既存のマイグレーションを適用

```bash
cd backend
venv\Scripts\activate.bat
python -m alembic upgrade head
```

または、バッチファイルを使用：

```bash
cd backend
run_migration.bat
```

### ステップ2: データベースの状態を確認

```bash
python -m alembic current
```

これで、現在のマイグレーションバージョンが表示されます。

### ステップ3: 新しいマイグレーションを作成（必要に応じて）

既存のマイグレーションを適用した後：

```bash
python -m alembic revision --autogenerate -m "make_change_history_case_id_nullable"
python -m alembic upgrade head
```

## 注意事項

- **重要**: マイグレーションを実行する前に、データベースのバックアップを取ってください
- SQLiteでは外部キー制約がデフォルトで無効のため、マイグレーションなしでも動作する可能性があります
- 既存のデータベースで `case_id` が `nullable=False` の場合、マイグレーションが必要です

## トラブルシューティング

### エラー: "Can't locate revision identified by '001'"

データベースにマイグレーション履歴がない場合：

```bash
python -m alembic stamp head
```

これで、データベースを最新のマイグレーション状態としてマークします。

### エラー: "Multiple heads detected"

複数のマイグレーションヘッドがある場合：

```bash
python -m alembic heads
```

で確認し、必要に応じてマージします。






