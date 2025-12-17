# 貿易DX システム起動手順

## クイックスタート

### 全てのサーバーを同時に起動（推奨）

プロジェクトルートディレクトリで以下を実行：

```batch
start_all.bat
```

これで、バックエンドとフロントエンドの両方が別ウィンドウで起動します。

---

## 個別に起動する場合

### バックエンドサーバー

#### 方法1: バッチファイルを使用（推奨）

```batch
cd backend
start_server.bat
```

#### 方法2: 手動で起動

```batch
cd backend
venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**起動確認:**
- サーバーURL: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs

---

### フロントエンドサーバー

#### 方法1: バッチファイルを使用（推奨）

```batch
cd frontend
start_frontend.bat
```

#### 方法2: 手動で起動

```batch
cd frontend
npm run dev
```

**起動確認:**
- サーバーURL: http://localhost:3000

---

## よくあるエラーと解決方法

### エラー1: `ModuleNotFoundError: No module named 'fastapi'`

**原因:** 仮想環境がアクティベートされていない

**解決方法:**
```batch
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

### エラー2: `Could not read package.json`

**原因:** プロジェクトルートで `npm run dev` を実行している（`frontend`ディレクトリで実行する必要がある）

**解決方法:**
```batch
cd frontend
npm run dev
```

または

```batch
cd frontend
start_frontend.bat
```

---

### エラー3: `node_modules` が見つからない

**原因:** 依存関係がインストールされていない

**解決方法:**
```batch
cd frontend
npm install
```

---

### エラー4: ポートが既に使用されている

**原因:** 既にサーバーが起動している、または他のアプリがポートを使用している

**解決方法:**
1. 既存のサーバーを停止（Ctrl+C）
2. 別のポートを使用する（推奨しません）
3. ポートを使用しているプロセスを終了する

**ポート確認（Windows）:**
```batch
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

---

## サーバー起動の確認

### バックエンド

1. ブラウザで http://localhost:8000/docs にアクセス
2. Swagger UIが表示されればOK

### フロントエンド

1. ブラウザで http://localhost:3000 にアクセス
2. ログイン画面が表示されればOK

---

## 開発環境の構成

```
貿易DX/
├── backend/              # バックエンド（FastAPI）
│   ├── venv/            # Python仮想環境
│   ├── app/             # アプリケーションコード
│   ├── requirements.txt # Python依存関係
│   └── start_server.bat # 起動スクリプト
│
├── frontend/            # フロントエンド（React + Vite）
│   ├── node_modules/    # Node.js依存関係
│   ├── src/             # ソースコード
│   ├── package.json     # Node.js依存関係定義
│   └── start_frontend.bat # 起動スクリプト
│
└── start_all.bat        # 全体起動スクリプト
```

---

## 次のステップ

サーバーが起動したら：

1. ブラウザで http://localhost:3000 にアクセス
2. ログイン画面でログイン
   - デフォルトユーザー: `admin`
   - デフォルトパスワード: `admin`
3. ダッシュボードが表示されれば成功

---

**問題が解決しない場合は、エラーメッセージの全文を共有してください。**








