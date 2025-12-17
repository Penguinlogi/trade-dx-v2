# バックエンドサーバー起動手順（詳細版）

## 📋 前提条件

- Python 3.11以上がインストールされていること
- プロジェクトの `backend` ディレクトリに移動していること

---

## 🚀 起動方法

### 方法1: バッチファイルを使用（最も簡単・推奨）

1. **コマンドプロンプトまたはPowerShellを開く**

2. **backendディレクトリに移動**
   ```batch
   cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"
   ```

3. **起動スクリプトを実行**
   ```batch
   start_server.bat
   ```

   または、ファイルエクスプローラーで `backend` フォルダを開き、`start_server.bat` をダブルクリック

---

### 方法2: 手動で起動（トラブルシューティング用）

#### ステップ1: 仮想環境の確認とアクティベート

```batch
cd backend

REM 仮想環境が存在するか確認
dir venv
```

仮想環境が存在しない場合：
```batch
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

仮想環境が存在する場合：
```batch
venv\Scripts\activate.bat
```

**確認方法:**
- プロンプトの先頭に `(venv)` が表示されればOK

#### ステップ2: 必要なライブラリの確認

```batch
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"
```

エラーが出る場合：
```batch
pip install -r requirements.txt
```

#### ステップ3: サーバー起動

```batch
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**成功時の表示:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## ✅ 起動確認

### 1. ブラウザで確認

以下のURLにアクセスして確認：

- **API ドキュメント（Swagger UI）**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **ヘルスチェック**: http://localhost:8000/api/health（存在する場合）

### 2. コマンドで確認

別のコマンドプロンプトで：
```batch
curl http://localhost:8000/docs
```

または、PowerShellで：
```powershell
Invoke-WebRequest -Uri http://localhost:8000/docs
```

---

## ❌ よくあるエラーと解決方法

### エラー1: `ModuleNotFoundError: No module named 'fastapi'`

**原因:** 仮想環境がアクティベートされていない、またはライブラリがインストールされていない

**解決方法:**
```batch
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

### エラー2: `'venv' は、内部コマンドまたは外部コマンド、操作可能なプログラムまたはバッチ ファイルとして認識されていません。`

**原因:** 仮想環境が存在しない

**解決方法:**
```batch
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

### エラー3: `Address already in use` または `ポートが既に使用されています`

**原因:** ポート8000が既に使用されている

**解決方法1: 既存のサーバーを停止**
- 既に起動しているサーバーのウィンドウで `Ctrl+C` を押す

**解決方法2: ポートを使用しているプロセスを確認**
```batch
netstat -ano | findstr :8000
```
表示されたPIDを確認し、タスクマネージャーで終了

**解決方法3: 別のポートを使用（一時的）**
```batch
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

---

### エラー4: `ImportError: cannot import name 'xxx' from 'app.xxx'`

**原因:** モジュールのインポートエラー

**解決方法:**
1. `backend/app` ディレクトリに `__init__.py` が存在するか確認
2. サーバーを再起動
3. エラーメッセージの全文を確認

---

### エラー5: `sqlite3.OperationalError: no such table: xxx`

**原因:** データベースが初期化されていない

**解決方法:**
```batch
cd backend
venv\Scripts\activate.bat
python -m alembic stamp head
```

または、データベースを再作成：
```batch
del trade_dx.db
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

### エラー6: `SyntaxError` または `IndentationError`

**原因:** コードの構文エラー

**解決方法:**
1. エラーメッセージに表示されているファイルと行番号を確認
2. そのファイルを開いて構文エラーを修正
3. サーバーを再起動

---

## 🔍 デバッグ方法

### 1. 詳細なログを表示

```batch
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### 2. エラーメッセージの全文を確認

サーバー起動時に表示されるエラーメッセージの全文をコピーして保存

### 3. データベースの状態を確認

```batch
cd backend
venv\Scripts\activate.bat
python scripts/check_database.py
```

---

## 📝 チェックリスト

起動前に以下を確認：

- [ ] Python 3.11以上がインストールされている
- [ ] `backend` ディレクトリに移動している
- [ ] 仮想環境（`venv`）が存在する
- [ ] 仮想環境がアクティベートされている（プロンプトに `(venv)` が表示される）
- [ ] 必要なライブラリがインストールされている（`pip list | findstr fastapi`）
- [ ] ポート8000が使用可能である
- [ ] データベースファイル（`trade_dx.db`）が存在する（または作成可能）

---

## 🆘 それでも解決しない場合

1. **エラーメッセージの全文をコピー**
2. **以下の情報を確認:**
   - Pythonのバージョン: `python --version`
   - 仮想環境の状態: `pip list`
   - ポートの使用状況: `netstat -ano | findstr :8000`
3. **エラーメッセージと上記の情報を共有してください**

---

## 📞 次のステップ

サーバーが正常に起動したら：

1. ブラウザで http://localhost:8000/docs にアクセス
2. Swagger UIが表示されれば成功
3. フロントエンドサーバーを起動（別ウィンドウ）
4. ブラウザで http://localhost:3000 にアクセス

---

**最終更新:** 2025-11-28








