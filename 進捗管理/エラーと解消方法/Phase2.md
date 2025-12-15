# Phase 2: 認証機能 - エラーと解消方法

## 発生したエラーと解消方法

Phase 2の開発中に発生したエラーと、その解消方法を記録します。

---

## エラー報告: なし ✅

Phase 2の開発では、特に大きなエラーは発生しませんでした。

### 開発がスムーズだった理由
1. ✅ Phase 1で適切な環境構築ができていた
2. ✅ requirements.txtに必要なパッケージが既に含まれていた
3. ✅ FastAPIの標準的な認証パターンを採用した
4. ✅ React Context APIを使った状態管理が適切だった

---

## よくある問題と解決方法

Phase 2の実装時や動作確認時に発生する可能性がある問題と、その解決方法をまとめます。

---

### 問題0-1: SyntaxError: (unicode error)

#### エラー内容
```
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
>>>
```

#### 原因
Pythonインタープリター（`>>>` プロンプト）で、コマンドプロンプトのコマンド（`cd`など）を実行しようとしている。

#### 症状
- プロンプトが `>>>` と表示されている
- `cd`、`pip`、`py -3 -m app.main` などのコマンドを実行するとSyntaxErrorが発生する
- 「unicode error」や「unicodeescape」というエラーメッセージが表示される

#### 解決方法

**ステップ1: Pythonインタープリターを終了する**
```python
>>> exit()
```

または、`Ctrl + Z` を押してから `Enter` を押す。

**ステップ2: コマンドプロンプトに戻ったことを確認**
プロンプトが `C:\Users\関伸>` のように表示されていればOK。

**ステップ3: コマンドを再度実行**
```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"
cd backend
py -3 -m app.main
```

#### プロンプトの見分け方
- ✅ **コマンドプロンプト（正しい）**: `C:\Users\関伸>` または `C:\...\backend>`
- ❌ **Pythonインタープリター（間違い）**: `>>>`

#### 予防策
- コマンドプロンプトを開いたら、`python` と単独で入力しない（これを実行するとPythonインタープリターが起動する）
- `>>>` プロンプトが表示されている場合は、必ず `exit()` で終了してからコマンドを実行する
- 手順書のコマンドは、すべてコマンドプロンプトで実行することを前提としている

---

### 問題0-2: 指定されたパスが見つかりません

#### エラー内容
```
C:\Users\関伸>cd backend
指定されたパスが見つかりません。
```

#### 原因
コマンドプロンプトを開いた場所（ホームディレクトリなど）から直接 `cd backend` を実行しようとしている。プロジェクトのルートディレクトリに移動していない。

#### 解決方法
```cmd
# まずプロジェクトのルートディレクトリに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# その後、backendに移動
cd backend
```

または一度に移動：
```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"
```

#### 現在のディレクトリを確認する方法
```cmd
cd
```

#### 予防策
- コマンドプロンプトを開いたら、**まず最初にプロジェクトのルートディレクトリに移動する習慣をつける**
- 手順書のコマンドは、プロジェクトルートからの相対パスで記載されている

---

### 問題1-1: Fatal error in launcher（日本語ユーザー名の問題）

#### エラー内容（パターン1: pipコマンド）
```
Fatal error in launcher: Unable to create process using '"C:\Users\??\AppData\Local\Programs\Python\Python314\python.exe"  "C:\Users\??\AppData\Local\Programs\Python\Python314\Scripts\pip.exe" install -r requirements.txt': ??????????????????
```

#### エラー内容（パターン2: Pythonスクリプト）
```
[ERROR] Failed to launch 'C:\Users\??\AppData\Local\Python\pythoncore-3.14-64\python.exe': the install path was not found (0x0002).
Try 'py install --repair <version>' to reinstall.
```

#### 原因
Windowsのユーザー名に日本語文字（「関伸」）が含まれているため、Pythonのランチャーがパスを正しく認識できず、「??」として表示される。これはPythonのランチャーが日本語を含むパスを適切に処理できないことが原因。

#### 症状
- `pip install` コマンドを実行すると「Fatal error in launcher」エラーが発生
- `python scripts\...` の形式でスクリプトを実行するとエラーが発生
- パスに「??」が表示される
- 文字化けしたエラーメッセージが表示される

#### 解決方法
**`py -3` コマンドを使用してPython 3を直接実行します。**

```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# パッケージをインストール
py -3 -m pip install -r requirements.txt

# スクリプトを実行
py -3 -m scripts.seed_data
py -3 -m scripts.check_database

# バックエンドを起動
py -3 -m app.main
```

**重要な変換ルール:**
- `python` → `py -3`（すべての場面で）
- `pip install` → `py -3 -m pip install`
- `python scripts\seed_data.py` → `py -3 -m scripts.seed_data`
- `python -m app.main` → `py -3 -m app.main`
- `scripts\` → `scripts.` に変更（バックスラッシュをドットに）
- `.py` 拡張子は不要

**なぜ `py -3` を使うのか？**
- `python` コマンド：Pythonランチャーを経由して実行→日本語パスで失敗
- `py -3` コマンド：Python 3を直接実行→日本語パスでも動作
- `-3` オプションで、Python 3系を明示的に指定

#### 代替方法（上級者向け）
1. Pythonを「すべてのユーザー」向けにインストールし直す（C:\Program Files\Python にインストール）
2. 環境変数を手動で設定する

ただし、最も簡単で確実な方法は `py -3 -m pip` を使用することです。

#### 予防策
**今後、すべてのPythonコマンドは `py -3` で実行してください：**

| ❌ 間違い | ✅ 正しい |
|---------|---------|
| `python -m app.main` | `py -3 -m app.main` |
| `pip install パッケージ名` | `py -3 -m pip install パッケージ名` |
| `python scripts\seed_data.py` | `py -3 -m scripts.seed_data` |
| `python scripts\check_database.py` | `py -3 -m scripts.check_database` |
| `python -m scripts.seed_data` | `py -3 -m scripts.seed_data` |

**ポイント:**
- `python` → `py -3` にすべて置き換え
- `py -3` は、Pythonランチャーを経由せずにPython 3を直接実行

---

### 問題1-2: ModuleNotFoundError: No module named 'jose'

#### エラー内容
```
ModuleNotFoundError: No module named 'jose'
```

#### 原因
python-joseパッケージがインストールされていない

#### 解決方法
```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# パッケージをインストール
py -3 -m pip install python-jose[cryptography]
```

または

```cmd
py -3 -m pip install -r requirements.txt
```

---

### 問題0-3: sqlite3は認識されていません

#### エラー内容
```
'sqlite3' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

#### 原因
WindowsにはSQLite3コマンドがデフォルトでインストールされていない

#### 解決方法
Pythonスクリプトを使ってデータベースを確認してください：

```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# データベース確認スクリプトを実行
py -3 -m scripts.check_database
```

または、バッチファイルで簡単に実行：
```cmd
scripts\check_db.bat
```

#### メリット
- SQLite3をインストールする必要がない
- Pythonスクリプトの方が見やすく整形されて表示される
- テーブルごとにきれいに分類して表示される

---

### 問題2: ログインできない（401 Unauthorized）

#### エラー内容
```json
{
  "detail": "ユーザー名またはパスワードが正しくありません"
}
```

#### 原因1: シードデータが投入されていない

**解決方法:**
```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# シードデータを投入
py -3 -m scripts.seed_data
```

#### 原因2: パスワードが間違っている

**解決方法:**
正しいパスワードを使用してください：
- admin: admin123
- yamada: yamada123
- suzuki: suzuki123

#### 原因3: データベースファイルが破損している

**解決方法:**
```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# データベースを削除
del trade_dx.db

# シードデータを再投入
py -3 -m scripts.seed_data
```

---

### 問題3: CORS Error

#### エラー内容
```
Access to XMLHttpRequest at 'http://localhost:8000/api/auth/login'
from origin 'http://localhost:3000' has been blocked by CORS policy
```

#### 原因
バックエンドのCORS設定が正しくない、またはバックエンドが起動していない

#### 解決方法1: バックエンドが起動しているか確認
ブラウザで http://localhost:8000/health にアクセスして確認

または、コマンドプロンプトで：
```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"
py -3 -m app.main
```

#### 解決方法2: CORS設定を確認
`backend/app/core/config.py` を確認:
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:3000",  # ← これがあることを確認
]
```

---

### 問題4: フロントエンドからバックエンドに接続できない

#### エラー内容
```
Network Error
```

#### 原因
環境変数が設定されていない、またはバックエンドのURLが間違っている

#### 解決方法1: .envファイルを作成
```bash
cd frontend

# .envファイルを作成
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# フロントエンドを再起動
npm run dev
```

#### 解決方法2: バックエンドのポートを確認
バックエンドが8000番ポートで起動していることを確認:
```bash
# Windowsの場合
netstat -ano | findstr :8000

# macOS/Linuxの場合
lsof -i :8000
```

---

### 問題5: トークンが保存されない

#### 症状
ログイン後すぐにログイン画面に戻る

#### 原因1: ブラウザのプライベートモード

**解決方法:**
通常モードでブラウザを開く

#### 原因2: LocalStorageがブロックされている

**解決方法:**
ブラウザの設定で「Cookieとサイトデータ」を許可

#### 原因3: ブラウザのキャッシュが残っている

**解決方法:**
1. ブラウザの開発者ツールを開く（F12）
2. Application → Storage → Clear site data
3. ブラウザを再起動

---

### 問題6: ポート8000が既に使用中

#### エラー内容
```
ERROR:    [Errno 48] Address already in use
```

#### 原因
ポート8000が既に使用されている

#### 解決方法1: 既存のプロセスを終了
```bash
# Windowsの場合
netstat -ano | findstr :8000
taskkill /PID [プロセスID] /F

# macOS/Linuxの場合
lsof -ti:8000 | xargs kill -9
```

#### 解決方法2: 別のポートを使用
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

その場合、フロントエンドの `.env` も更新:
```
VITE_API_BASE_URL=http://localhost:8001
```

---

### 問題7: 「セッションの期限が切れました」と表示される

#### 症状
30分後に自動ログアウトされる

#### 原因
これは仕様です（正常な動作）

#### 説明
- JWTトークンの有効期限は30分に設定されています
- 25分後に警告メッセージが表示されます
- 30分後に自動的にログアウトされます

#### 解決方法
再度ログインしてください。

#### 有効期限を変更したい場合
`backend/app/core/config.py` を編集:
```python
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # ← この値を変更
```

---

### 問題8: Swagger UIで認証できない

#### 症状
「Authorize」ボタンをクリックしても認証されない

#### 解決方法
1. まず「POST /api/auth/login」でログインしてトークンを取得
2. レスポンスから `access_token` の値をコピー（`eyJ...` の部分）
3. 右上の「Authorize」ボタンをクリック
4. `Bearer` を含めずにトークンのみを貼り付け
5. 「Authorize」→「Close」をクリック
6. 再度APIを実行

---

### 問題9: パスワードが間違っていないのにログインできない

#### 原因
パスワードのハッシュ化の問題、またはデータベースの問題

#### 解決方法1: データベースを再作成
```cmd
cd backend
del trade_dx.db
py -3 -m scripts.seed_data
```

#### 解決方法2: パスワードハッシュを確認
```bash
cd backend
sqlite3 trade_dx.db

# ユーザーのハッシュパスワードを確認
SELECT username, hashed_password FROM users WHERE username='admin';

# 終了
.exit
```

ハッシュパスワードが `$2b$` で始まっていればbcryptで正しくハッシュ化されています。

---

### 問題10: TypeScript エラー（フロントエンド）

#### エラー内容
```
Property 'user' does not exist on type 'AuthContextType | undefined'
```

#### 原因
useAuthフックを使用していない、または正しくインポートされていない

#### 解決方法
```typescript
import { useAuth } from '../context/AuthContext';

// コンポーネント内で使用
const { user, isAuthenticated, login, logout } = useAuth();
```

---

## 予防策

### 開発時のベストプラクティス

1. **環境変数を必ず設定する**
   - フロントエンドの `.env` ファイルを作成
   - バックエンドのポートを確認

2. **シードデータを投入する**
   - 開発開始時に必ず実行: `py -3 -m scripts.seed_data`

3. **ブラウザの開発者ツールを活用**
   - Network タブでAPIリクエストを確認
   - Console タブでエラーを確認
   - Application タブでトークンを確認

4. **Swagger UIを活用**
   - APIが正しく動作しているか確認
   - リクエスト・レスポンスの形式を確認

5. **定期的にデータベースを確認**
   - SQLiteデータベースを直接確認
   - データが正しく保存されているか確認

---

## デバッグのヒント

### バックエンドのデバッグ

#### ログを確認
```bash
cd backend
py -3 -m app.main
# コンソールにログが表示される
```

#### データベースを確認
```bash
cd backend
sqlite3 trade_dx.db

# ユーザー一覧を確認
SELECT * FROM users;

# 終了
.exit
```

### フロントエンドのデバッグ

#### ブラウザの開発者ツール（F12）
1. **Console タブ**: JavaScriptエラーを確認
2. **Network タブ**: APIリクエストを確認
3. **Application タブ**: LocalStorageを確認

#### トークンの確認
```javascript
// ブラウザのコンソールで実行
console.log(localStorage.getItem('access_token'));
console.log(JSON.parse(localStorage.getItem('user')));
```

---

## まとめ

Phase 2の開発は非常にスムーズでした。上記の問題は、主に環境設定やデータ投入に関するもので、コード自体には大きな問題はありませんでした。

### 重要なポイント
✅ シードデータの投入を忘れない
✅ 環境変数を正しく設定する
✅ バックエンドとフロントエンドの両方を起動する
✅ ブラウザの開発者ツールを活用する
✅ Swagger UIでAPIを確認する

---

**作成日**: 2025-11-25
**Phase**: 2
**ステータス**: 完了
