# Phase 1 - 手動操作手順書

## 目的
Phase 1で実装したデータベース環境とシードデータが正しく動作することを手動で確認します。

---

## 前提条件
- Python 3.11以上がインストールされていること
- プロジェクトのルートディレクトリにいること

---

## 手順1: Pythonの依存関係をインストール

### 方法A: pip を使用（推奨）
```bash
cd backend
pip install -r requirements.txt
```

**期待される結果**: すべての依存関係が正常にインストールされる

**注意**: 以下のパッケージがRustコンパイラを必要とする場合があります
- 開発環境ではSQLiteを使用するため、PostgreSQLドライバー（psycopg2-binary）はコメントアウトされています
- Rustコンパイラのエラーが出た場合は、requirements.txtのバージョンが正しいことを確認してください

---

## 手順2: データベーステーブルの作成

### 実行前の確認
- `backend/` ディレクトリにいることを確認
- `trade_dx.db` ファイルが存在しないことを確認（初回実行の場合）

### 実行コマンド
```bash
# Windowsの場合
cd backend
python scripts\seed_data.py

# macOS/Linuxの場合
cd backend
python scripts/seed_data.py
```

### 期待される出力
```
============================================================
シードデータ投入スクリプト
============================================================
テーブルを作成中...
✓ テーブル作成完了

初期ユーザーを作成中...
  - admin (管理者)
  - yamada (山田太郎)
  - suzuki (鈴木花子)
✓ ユーザー作成完了

顧客マスタを作成中...
  - C001: ABC商事株式会社
  - C002: XYZ物産株式会社
  - C003: グローバル貿易株式会社
✓ 顧客マスタ作成完了

商品マスタを作成中...
  - P001: 電子部品A
  - P002: プラスチック原料B
  - P003: 金属パーツC
  - P004: 繊維製品D
✓ 商品マスタ作成完了

案件番号管理を初期化中...
  - 2025-EX: 連番初期化
  - 2025-IM: 連番初期化
✓ 案件番号管理初期化完了

============================================================
✓ すべてのシードデータ投入が完了しました
============================================================
```

### トラブルシューティング
**エラー**: `ModuleNotFoundError: No module named 'passlib'`
**解決策**: requirements.txtの依存関係を再インストール
```bash
pip install -r requirements.txt
```

**エラー**: `sqlalchemy.exc.OperationalError`
**解決策**: データベースファイルのパーミッションを確認、または既存の`trade_dx.db`を削除して再実行

---

## 手順3: テストデータの投入

### 実行コマンド
```bash
# Windowsの場合
python scripts\test_data.py

# macOS/Linuxの場合
python scripts/test_data.py
```

### 期待される出力
```
============================================================
テストデータ投入スクリプト
============================================================
テスト用案件データを作成中...
  - 2025-EX-001: 見積中
  - 2025-EX-002: 受注済
  - 2025-IM-001: 船積済
  - 2025-EX-003: 完了
  - 2025-IM-002: 見積中
✓ テスト案件データ作成完了 (5件)

現在のデータ件数:
  - ユーザー: 3件
  - 顧客: 3件
  - 商品: 4件
  - 案件: 5件

============================================================
✓ テストデータ投入が完了しました
============================================================
```

---

## 手順4: データベースの確認

### 方法A: SQLiteブラウザを使用
1. [DB Browser for SQLite](https://sqlitebrowser.org/)をダウンロード・インストール
2. `backend/trade_dx.db` を開く
3. 以下のテーブルが存在することを確認：
   - users
   - customers
   - products
   - cases
   - change_history
   - case_numbers
   - backups

### 方法B: Pythonスクリプトで確認
```bash
cd backend
python -c "from app.core.database import SessionLocal; from app.models import User, Customer, Product, Case; db = SessionLocal(); print('Users:', db.query(User).count()); print('Customers:', db.query(Customer).count()); print('Products:', db.query(Product).count()); print('Cases:', db.query(Case).count())"
```

### 期待される出力
```
Users: 3
Customers: 3
Products: 4
Cases: 5
```

---

## 手順5: FastAPIサーバーの起動確認

### 実行コマンド
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 期待される出力
```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### ブラウザで確認
1. http://127.0.0.1:8000 にアクセス
2. 以下のようなJSONレスポンスが返ってくることを確認：
```json
{
  "message": "貿易DX管理システム API",
  "version": "2.1.0",
  "status": "running"
}
```

3. http://127.0.0.1:8000/docs にアクセス
4. Swagger UIが表示されることを確認

---

## 確認チェックリスト

### データベース
- [ ] trade_dx.db ファイルが作成されている
- [ ] 7つのテーブルがすべて作成されている
- [ ] usersテーブルに3件のレコードが存在
- [ ] customersテーブルに3件のレコードが存在
- [ ] productsテーブルに4件のレコードが存在
- [ ] casesテーブルに5件のレコードが存在
- [ ] case_numbersテーブルに2件のレコード（輸出・輸入）が存在

### FastAPIサーバー
- [ ] サーバーが正常に起動する
- [ ] http://127.0.0.1:8000 でルートエンドポイントにアクセスできる
- [ ] http://127.0.0.1:8000/health でヘルスチェックが成功する
- [ ] http://127.0.0.1:8000/docs でSwagger UIが表示される

### 環境構成
- [ ] backend/requirements.txt のすべての依存関係がインストールされている
- [ ] backend/app/models/ に7つのモデルファイルが存在
- [ ] backend/alembic/versions/ にマイグレーションファイルが存在
- [ ] backend/scripts/ にシードデータスクリプトが存在

---

## トラブルシューティング

### 問題1: Pythonモジュールが見つからない
**症状**: `ModuleNotFoundError`
**解決策**:
```bash
cd backend
pip install -r requirements.txt
```

### 問題2: データベースファイルが作成されない
**症状**: `No such file or directory: './trade_dx.db'`
**解決策**:
- backendディレクトリにいることを確認
- パーミッションを確認
- 手動でファイルを作成してから再実行

### 問題3: FastAPIサーバーが起動しない
**症状**: `ImportError` または `ModuleNotFoundError`
**解決策**:
1. Pythonパスを確認
```bash
cd backend
python -c "import sys; print(sys.path)"
```
2. app/__init__.pyが存在することを確認
3. 依存関係を再インストール

### 問題4: Rustコンパイラエラー
**症状**: `Cargo, the Rust package manager, is not installed`
**解決策**:
- pydanticとfastapiのバージョンを確認（requirements.txtで最新バージョンを使用）
- または、バイナリビルド済みのパッケージをインストール

---

## 一括実行スクリプト

### Windowsの場合
```bash
cd backend
scripts\run_seed.bat
```

### macOS/Linuxの場合
```bash
cd backend
chmod +x scripts/run_seed.sh
./scripts/run_seed.sh
```

このスクリプトは以下を順番に実行します：
1. シードデータの投入
2. テストデータの投入

---

## 次のステップ
Phase 1の動作確認が完了したら、Phase 2（認証機能）の開発に進みます。

## 参考資料
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [Alembic公式ドキュメント](https://alembic.sqlalchemy.org/)














