# 貿易DX管理システム - バックエンド

FastAPIを使用したバックエンドAPIサーバー

## 技術スタック

- **Python**: 3.11+
- **フレームワーク**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0
- **データベース**: PostgreSQL 15+ / SQLite (開発用)
- **認証**: JWT (JSON Web Tokens)

## セットアップ

### 1. 仮想環境の作成と有効化

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、必要な設定を行う

```bash
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

### 4. データベースマイグレーション

```bash
alembic upgrade head
```

### 5. サーバーの起動

```bash
# 開発モード（ホットリロード有効）
uvicorn app.main:app --reload

# または
python -m app.main
```

サーバーは `http://localhost:8000` で起動します。

## API ドキュメント

サーバー起動後、以下のURLでAPIドキュメントにアクセスできます：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ディレクトリ構造

```
backend/
├── app/
│   ├── api/              # APIエンドポイント
│   │   ├── endpoints/    # 個別エンドポイント
│   │   └── deps.py       # 依存性注入
│   ├── core/             # コア機能
│   │   ├── config.py     # 設定管理
│   │   ├── database.py   # DB接続
│   │   └── security.py   # セキュリティ
│   ├── models/           # SQLAlchemyモデル
│   ├── schemas/          # Pydanticスキーマ
│   ├── services/         # ビジネスロジック
│   └── main.py           # メインアプリケーション
├── alembic/              # DBマイグレーション
├── tests/                # テスト
├── requirements.txt      # 依存パッケージ
├── .env.example          # 環境変数テンプレート
└── README.md
```

## テスト

```bash
pytest
```

## 開発

### コードフォーマット

```bash
black app/
```

### リンター

```bash
flake8 app/
```

### 型チェック

```bash
mypy app/
```

