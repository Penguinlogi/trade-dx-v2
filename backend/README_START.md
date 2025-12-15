# バックエンドサーバー起動手順

## 問題: `ModuleNotFoundError: No module named 'fastapi'`

このエラーは、仮想環境がアクティベートされていない状態でサーバーを起動しようとした場合に発生します。

## 解決方法

### 方法1: バッチファイルを使用（推奨）

1. `backend` ディレクトリに移動
2. `start_server.bat` をダブルクリック、またはコマンドプロンプト/PowerShellで実行：

**コマンドプロンプト（cmd）を使用する場合**:
```batch
cd backend
start_server.bat
```

**PowerShellを使用する場合**:
```powershell
cd backend
.\start_server.bat
```

**注意**: PowerShellでは、現在のディレクトリのファイルを実行する際に `.\` を付ける必要があります。

このバッチファイルは以下を自動的に実行します：
- 仮想環境のアクティベート
- 必要なライブラリの確認・インストール
- サーバーの起動

### 方法2: 手動で仮想環境をアクティベート

#### コマンドプロンプト（cmd）を使用する場合

```batch
cd backend
venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### PowerShellを使用する場合

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**注意**: PowerShellで `Activate.ps1` を実行できない場合は、実行ポリシーを変更してください：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 方法3: ライブラリがインストールされていない場合

仮想環境をアクティベートした後、必要なライブラリをインストール：

```batch
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 確認方法

仮想環境が正しくアクティベートされているか確認：

```batch
python --version
pip list | findstr fastapi
```

`fastapi` が表示されれば、仮想環境が正しくアクティベートされています。

## サーバー起動確認

サーバーが起動すると、以下のメッセージが表示されます：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

ブラウザで以下にアクセスして確認：
- API ドキュメント: http://localhost:8000/docs
- ヘルスチェック: http://localhost:8000/health
