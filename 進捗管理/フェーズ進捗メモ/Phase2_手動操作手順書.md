# Phase 2: 認証機能 - 手動操作手順書

## ⚠️ 重要な注意事項

### 1. コマンドプロンプトで実行してください

**すべてのコマンドは、Windowsのコマンドプロンプトで実行してください。**

#### コマンドプロンプトの開き方
1. `Win + R` を押す
2. `cmd` と入力してEnter

#### プロンプトの見分け方
- ✅ **コマンドプロンプト（正しい）**: `C:\Users\関伸>` のように表示される
- ❌ **Pythonインタープリター（間違い）**: `>>>` と表示される

**もし `>>>` が表示されている場合は、`exit()` と入力してPythonを終了してください。**

### 2. プロジェクトのルートディレクトリに移動してください

**コマンドプロンプトを開いたら、まず最初にプロジェクトのルートディレクトリに移動してください！**

```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"
```

このディレクトリから、`backend` や `frontend` に移動してください。

---

## 目次
1. [概要](#概要)
2. [前提条件](#前提条件)
3. [テストデータの確認](#テストデータの確認)
4. [バックエンドの起動](#バックエンドの起動)
5. [フロントエンドの起動](#フロントエンドの起動)
6. [認証機能の動作確認](#認証機能の動作確認)
7. [確認チェックリスト](#確認チェックリスト)
8. [トラブルシューティング](#トラブルシューティング)

---

## 概要

Phase 2では、JWT認証を使用したユーザー認証機能を実装しました。

### 実装した機能
- ✅ JWT認証システム（トークン生成・検証）
- ✅ パスワードハッシュ化（bcrypt）
- ✅ 認証API エンドポイント（login, logout, me, refresh）
- ✅ ログイン画面
- ✅ 認証コンテキスト（AuthContext）
- ✅ プライベートルート（認証が必要なページの保護）
- ✅ 自動ログアウト機能（30分）

---

## 前提条件

### 必須環境
- Python 3.11以上
- Node.js 18以上
- Phase 1が完了していること

### 確認コマンド
```bash
# Pythonバージョン確認
python --version

# Node.jsバージョン確認
node --version

# npmバージョン確認
npm --version
```

---

## テストデータの確認

### 1. シードデータの投入

Phase 1でシードデータを既に投入済みの場合は、このステップをスキップできます。

```cmd
# プロジェクトのルートディレクトリに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドディレクトリに移動
cd backend

# シードデータ投入
py -3 -m scripts.seed_data
```

または、一度に移動する場合：

```cmd
# バックエンドディレクトリに直接移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"

# シードデータ投入
py -3 -m scripts.seed_data
```

**注意**: コマンドプロンプトを開いたら、まず**プロジェクトのルートディレクトリに移動**してください。

### 2. テストユーザーの確認

以下のユーザーが作成されています：

| ユーザー名 | パスワード | 権限 | フルネーム |
|-----------|----------|------|-----------|
| admin | admin123 | 管理者 | 管理者 |
| yamada | yamada123 | 一般 | 山田太郎 |
| suzuki | suzuki123 | 一般 | 鈴木花子 |

### 3. データベースの確認（オプション）

```cmd
# バックエンドディレクトリに移動（まだ移動していない場合）
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"

# データベース確認スクリプトを実行
py -3 -m scripts.check_database
```

または、バッチファイルを使って簡単に実行：

```cmd
scripts\check_db.bat
```

**期待される結果:**
```
================================================================================
貿易DX データベース確認
================================================================================

テーブル一覧: users, customers, products, cases, case_numbers, change_history, backups

================================================================================
ユーザーテーブル (users)
================================================================================
ID    ユーザー名         メールアドレス                     フルネーム         アクティブ   管理者
--------------------------------------------------------------------------------
1     admin          admin@example.com              管理者            ○          ○
2     yamada         yamada@example.com             山田太郎          ○          ×
3     suzuki         suzuki@example.com             鈴木花子          ○          ×

合計: 3 件

================================================================================
顧客マスタ (customers)
================================================================================
ID    顧客コード      顧客名                            担当者
--------------------------------------------------------------------------------
1     C001        ABC商事株式会社                   田中一郎
2     C002        XYZ物産株式会社                   佐藤花子
3     C003        グローバル貿易株式会社              高橋次郎

合計: 3 件

（商品マスタ、案件番号管理も同様に表示されます）
```

---

## バックエンドの起動

### ⚠️ 重要: コマンドプロンプトで実行してください

以下のコマンドは、**Windowsのコマンドプロンプト**で実行してください。
- ❌ Pythonインタープリター（`>>>` プロンプト）では実行できません
- ✅ コマンドプロンプト（`C:\...>` プロンプト）で実行してください

**Pythonインタープリターが起動している場合は、`exit()` で終了してください。**

### 方法1: Pythonで直接起動（推奨）

```cmd
# プロジェクトのルートディレクトリに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# backendディレクトリに移動
cd backend

# 依存パッケージのインストール（初回のみ）
py -3 -m pip install -r requirements.txt

# サーバー起動
py -3 -m app.main
```

**注意**:
- `cd` などのコマンドは、すべてコマンドプロンプトで実行してください。
- **日本語ユーザー名の問題を回避するため、すべてのPythonコマンドは `py -3` で実行してください。**

または

```cmd
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 方法2: Dockerで起動

```bash
# プロジェクトルートで実行
docker-compose up -d backend
```

### 起動確認

ブラウザで以下のURLにアクセス:

1. **ヘルスチェック**
   http://localhost:8000/health

   **期待される結果:**
   ```json
   {
     "status": "healthy",
     "app_name": "貿易DX管理システム",
     "version": "2.1.0"
   }
   ```

2. **API ドキュメント（Swagger UI）**
   http://localhost:8000/docs

   ✅ API エンドポイント一覧が表示される
   ✅ 「認証」タグに4つのエンドポイントがある:
   - POST /api/auth/login
   - POST /api/auth/logout
   - GET /api/auth/me
   - POST /api/auth/refresh

---

## フロントエンドの起動

### 1. 依存パッケージのインストール

```cmd
# プロジェクトのルートディレクトリに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# frontendディレクトリに移動
cd frontend

# 依存パッケージのインストール（初回のみ）
npm install
```

### 2. 環境変数の設定

フロントエンドディレクトリに `.env` ファイルを作成します（既に作成済み）:

```cmd
# .env の内容を確認
type .env
```

**期待される内容:**
```
VITE_API_BASE_URL=http://localhost:8000
```

### 3. フロントエンドの起動

```cmd
# frontendディレクトリで実行
npm run dev
```

### 起動確認

ブラウザで以下のURLにアクセス:

http://localhost:3000

✅ ログイン画面が表示される

---

## 認証機能の動作確認

### テスト1: ログイン機能

#### 手順
1. ブラウザで http://localhost:3000 にアクセス
2. ログイン画面が表示されることを確認
3. 以下の情報でログイン:
   - **ユーザー名**: `admin`
   - **パスワード**: `admin123`
4. 「ログイン」ボタンをクリック

#### 期待される結果
✅ ダッシュボード画面に遷移
✅ ヘッダーに「管理者」と表示される
✅ ユーザー情報が正しく表示される:
  - ユーザーID: 1
  - ユーザー名: admin
  - メールアドレス: admin@example.com
  - 権限: 管理者

#### 確認ポイント
- [ ] ログイン画面が表示される
- [ ] ログイン処理が成功する
- [ ] ダッシュボードに遷移する
- [ ] ユーザー情報が正しく表示される

---

### テスト2: 認証トークンの確認

#### 手順
1. ログイン後、ブラウザの開発者ツールを開く（F12）
2. 「Application」タブ（Chromeの場合）または「ストレージ」タブ（Firefoxの場合）を開く
3. 「Local Storage」→「http://localhost:3000」を選択
4. `access_token` と `user` が保存されていることを確認

#### 期待される結果
✅ `access_token`: JWT形式のトークン（`eyJ...` で始まる長い文字列）
✅ `user`: ユーザー情報のJSON文字列

#### 確認ポイント
- [ ] access_tokenが保存されている
- [ ] userが保存されている
- [ ] トークンがJWT形式である

---

### テスト3: ログアウト機能

#### 手順
1. ダッシュボード画面右上のログアウトアイコン（🚪）をクリック
2. ログイン画面に遷移することを確認

#### 期待される結果
✅ ログイン画面に遷移
✅ Local Storageから`access_token`と`user`が削除される

#### 確認方法
開発者ツールで Local Storage を確認:
- `access_token`: 削除されている
- `user`: 削除されている

#### 確認ポイント
- [ ] ログアウトボタンをクリックできる
- [ ] ログイン画面に遷移する
- [ ] トークンが削除される

---

### テスト4: 認証保護（未認証アクセス）

#### 手順
1. ログアウトした状態で、ブラウザのアドレスバーに直接 http://localhost:3000/ を入力
2. Enterキーを押す

#### 期待される結果
✅ 自動的にログイン画面（http://localhost:3000/login）にリダイレクトされる

#### 確認ポイント
- [ ] ダッシュボードにアクセスできない
- [ ] ログイン画面にリダイレクトされる

---

### テスト5: 誤った認証情報でのログイン

#### 手順
1. ログイン画面で以下の情報を入力:
   - **ユーザー名**: `admin`
   - **パスワード**: `wrongpassword`
2. 「ログイン」ボタンをクリック

#### 期待される結果
✅ エラーメッセージが表示される:
「ユーザー名またはパスワードが正しくありません」

#### 確認ポイント
- [ ] ログインが失敗する
- [ ] エラーメッセージが表示される
- [ ] ログイン画面のままである

---

### テスト6: 異なるユーザーでのログイン

#### 手順
1. ログイン画面で以下の情報を入力:
   - **ユーザー名**: `yamada`
   - **パスワード**: `yamada123`
2. 「ログイン」ボタンをクリック

#### 期待される結果
✅ ダッシュボード画面に遷移
✅ ヘッダーに「山田太郎」と表示される
✅ ユーザー情報が正しく表示される:
  - ユーザーID: 2
  - ユーザー名: yamada
  - メールアドレス: yamada@example.com
  - 権限: 一般ユーザー

#### 確認ポイント
- [ ] ログインが成功する
- [ ] 正しいユーザー情報が表示される
- [ ] 一般ユーザーと表示される

---

### テスト7: APIエンドポイントの直接テスト（Swagger UI）

#### 手順
1. ブラウザで http://localhost:8000/docs にアクセス
2. 「POST /api/auth/login」エンドポイントを展開
3. 「Try it out」ボタンをクリック
4. 以下の情報を入力:
   - **username**: `admin`
   - **password**: `admin123`
5. 「Execute」ボタンをクリック

#### 期待される結果
✅ Response Code: 200
✅ Response Body:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "管理者",
    "is_active": true,
    "is_superuser": true,
    "created_at": "2025-11-21T...",
    "updated_at": "2025-11-21T..."
  }
}
```

#### 確認ポイント
- [ ] ステータスコード200が返る
- [ ] access_tokenが返される
- [ ] ユーザー情報が返される

---

### テスト8: 認証が必要なエンドポイント（GET /api/auth/me）

#### 手順
1. Swagger UI（http://localhost:8000/docs）で「GET /api/auth/me」を展開
2. 「Try it out」→「Execute」をクリック（トークンなし）

#### 期待される結果（トークンなし）
✅ Response Code: 401
✅ Response Body:
```json
{
  "detail": "Not authenticated"
}
```

#### 手順（トークンあり）
1. 「POST /api/auth/login」でログインしてトークンを取得
2. 右上の「Authorize」ボタンをクリック
3. 取得したトークンを入力（`Bearer` は不要）
4. 「Authorize」→「Close」
5. 「GET /api/auth/me」を再度実行

#### 期待される結果（トークンあり）
✅ Response Code: 200
✅ Response Body: ユーザー情報が返される

#### 確認ポイント
- [ ] トークンなしで401エラーになる
- [ ] トークンありで200が返る
- [ ] ユーザー情報が取得できる

---

## 確認チェックリスト

### バックエンド
- [ ] バックエンドが正常に起動する
- [ ] ヘルスチェックが成功する（/health）
- [ ] Swagger UIが表示される（/docs）
- [ ] 認証エンドポイントが4つある

### フロントエンド
- [ ] フロントエンドが正常に起動する
- [ ] ログイン画面が表示される
- [ ] ダッシュボード画面が表示される

### 認証機能
- [ ] 正しい認証情報でログインできる
- [ ] ログイン後、ダッシュボードに遷移する
- [ ] ユーザー情報が正しく表示される
- [ ] トークンがLocal Storageに保存される
- [ ] ログアウトできる
- [ ] ログアウト後、トークンが削除される
- [ ] 未認証でダッシュボードにアクセスできない
- [ ] 誤った認証情報でエラーが表示される
- [ ] 異なるユーザーでログインできる

### API
- [ ] POST /api/auth/login が動作する
- [ ] POST /api/auth/logout が動作する
- [ ] GET /api/auth/me が動作する
- [ ] POST /api/auth/refresh が動作する
- [ ] トークンなしで401エラーになる

---

## トラブルシューティング

### 問題0-1: 「指定されたパスが見つかりません」エラー

#### エラー内容
```
C:\Users\関伸>cd backend
指定されたパスが見つかりません。
```

#### 原因
プロジェクトのルートディレクトリ以外の場所から `cd backend` を実行している

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

---

### 問題0-2: 「sqlite3は認識されていません」エラー

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
# バックエンドディレクトリに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"

# データベース確認スクリプトを実行
py -3 -m scripts.check_database
```

または、バッチファイルで簡単に実行：
```cmd
scripts\check_db.bat
```

このスクリプトは、SQLite3コマンドよりも見やすくデータを表示します。

---

### 問題0-3: 「SyntaxError: (unicode error)」エラー

#### エラー内容
```
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
>>>
```

#### 原因
Pythonインタープリター（`>>>` プロンプト）でコマンドプロンプトのコマンドを実行しようとしている

#### 症状
- プロンプトが `>>>` と表示されている
- `cd`、`pip`、`py -3 -m app.main` などのコマンドを実行するとエラーになる

#### 解決方法

**1. Pythonインタープリターを終了する**
```python
>>> exit()
```

または、`Ctrl + Z` を押してから `Enter` を押す。

**2. コマンドプロンプトに戻ったことを確認**
プロンプトが `C:\Users\関伸>` のように表示されていればOK。

**3. コマンドを再度実行**
```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"
cd backend
py -3 -m app.main
```

#### 予防策
- コマンドプロンプトを開くときは、`python` と入力せずに直接コマンドを実行する
- `>>>` プロンプトが表示されている場合は、Pythonインタープリターなので `exit()` で終了する
- コマンドプロンプトのプロンプトは `C:\...>` の形式

---

### 問題1-1: Fatal error in launcher（日本語ユーザー名の問題）

#### エラー内容
```
Fatal error in launcher: Unable to create process using '"C:\Users\??\AppData\Local\Programs\Python\Python314\python.exe"'
```

#### 原因
ユーザー名に日本語（「関伸」）が含まれているため、Pythonのランチャーがパスを正しく認識できない

#### 解決方法
`pip` の代わりに `py -3 -m pip` を使用してください：

```cmd
py -3 -m pip install -r requirements.txt
```

このコマンドは、ランチャーをバイパスしてPythonモジュールとしてpipを直接実行します。

**重要**: 今後、すべての `pip` コマンドは `py -3 -m pip` に置き換えてください。

---

### 問題1-1-2: Pythonスクリプト実行時のランチャーエラー

#### エラー内容
```
[ERROR] Failed to launch 'C:\Users\??\AppData\Local\Python\pythoncore-3.14-64\python.exe': the install path was not found (0x0002).
Try 'py install --repair <version>' to reinstall.
```

#### 原因
`python scripts\seed_data.py` のような形式でスクリプトを実行すると、Pythonランチャーが日本語ユーザー名（「関伸」）を認識できない

#### 症状
- `python scripts\...` の形式でスクリプトを実行するとエラーが発生
- パスに「??」が表示される

#### 解決方法
`py -3 -m` を使ってモジュールとして実行してください：

```cmd
# ❌ 間違い
python scripts\seed_data.py

# ✅ 正しい
py -3 -m scripts.seed_data
```

同様に、他のコマンドも：
```cmd
# 依存パッケージのインストール
py -3 -m pip install -r requirements.txt

# データベース確認
py -3 -m scripts.check_database

# バックエンド起動
py -3 -m app.main
```

#### 注意
- **`py -3` を必ず使用してください**（`python` ではなく）
- `py -3` は、Python 3を直接実行します（ランチャーの問題を回避）
- `scripts\` → `scripts.` に変更（バックスラッシュをドットに）
- `.py` 拡張子は不要

#### なぜ `py -3` が必要なのか？
- `python` コマンド：Pythonランチャーを経由→日本語パスで失敗
- `py -3` コマンド：Python 3を直接実行→日本語パスでも動作

---

### 問題1-2: ModuleNotFoundError: No module named 'jose'

#### エラー内容
```
ModuleNotFoundError: No module named 'jose'
```

**原因:** 必要なパッケージがインストールされていない

**解決方法:**
```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# パッケージをインストール
py -3 -m pip install -r requirements.txt
```

---

### 問題1-3: ログインできない（エラー: 401）

#### エラー: 「ユーザー名またはパスワードが正しくありません」

**原因1:** シードデータが投入されていない

**解決方法:**
```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# シードデータを投入
py -3 -m scripts.seed_data
```

**原因2:** パスワードが間違っている

**解決方法:**
正しいパスワードを確認:
- admin: admin123
- yamada: yamada123
- suzuki: suzuki123

---

### 問題1-4: フロントエンドからバックエンドに接続できない

#### エラー: `Network Error` または `CORS Error`

**原因1:** バックエンドが起動していない

**解決方法:**
```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# バックエンドに移動
cd backend

# バックエンドを起動
py -3 -m app.main
```

**原因2:** 環境変数が設定されていない

**解決方法:**
```bash
cd frontend
# .envファイルを確認
cat .env

# なければ作成
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# フロントエンドを再起動
npm run dev
```

**原因3:** ポートが異なる

**解決方法:**
- バックエンド: http://localhost:8000
- フロントエンド: http://localhost:3000

上記のポートで起動していることを確認してください。

---

### 問題2-1: トークンが保存されない

#### 症状: ログイン後すぐにログイン画面に戻る

**原因:** Local Storageがブロックされている

**解決方法:**
1. ブラウザのプライベートモードを解除
2. ブラウザの設定でCookieとサイトデータを許可
3. ブラウザのキャッシュをクリア

---

### 問題2-2: 「セッションの期限が切れました」と表示される

#### 症状: 30分後に自動ログアウトされる

**原因:** これは正常な動作です（仕様）

**解決方法:**
再度ログインしてください。トークンの有効期限は30分に設定されています。

---

### 問題2-3: ポート8000が既に使用中

#### エラー: `Address already in use`

**解決方法1:** 既存のプロセスを終了
```bash
# Windowsの場合
netstat -ano | findstr :8000
taskkill /PID [プロセスID] /F

# macOS/Linuxの場合
lsof -ti:8000 | xargs kill -9
```

**解決方法2:** 別のポートを使用
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

その場合、フロントエンドの`.env`も更新:
```
VITE_API_BASE_URL=http://localhost:8001
```

---

### 問題2-4: Swagger UIで認証できない

#### 症状: 「Authorize」ボタンをクリックしても認証されない

**解決方法:**
1. まず「POST /api/auth/login」でログインしてトークンを取得
2. トークン（`eyJ...`の部分のみ）をコピー
3. 「Authorize」ボタンをクリック
4. `Bearer` を含めずにトークンのみを貼り付け
5. 「Authorize」→「Close」をクリック
6. 再度APIを実行

---

## Phase 2 完了の確認

すべてのチェックリストが完了したら、Phase 2は正常に動作しています。

次は **Phase 3: 案件管理API** の開発に進みます。

---

## 関連ファイル

### バックエンド
- `backend/app/core/security.py` - JWT認証とパスワードハッシュ化
- `backend/app/core/deps.py` - 認証依存性注入
- `backend/app/schemas/user.py` - ユーザースキーマ
- `backend/app/schemas/auth.py` - 認証スキーマ
- `backend/app/api/endpoints/auth.py` - 認証エンドポイント
- `backend/app/main.py` - FastAPIメインアプリケーション

### フロントエンド
- `frontend/src/types/auth.ts` - 認証型定義
- `frontend/src/api/axios.ts` - Axios設定
- `frontend/src/api/auth.ts` - 認証API
- `frontend/src/context/AuthContext.tsx` - 認証コンテキスト
- `frontend/src/components/PrivateRoute.tsx` - プライベートルート
- `frontend/src/pages/LoginPage.tsx` - ログイン画面
- `frontend/src/pages/DashboardPage.tsx` - ダッシュボード画面
- `frontend/src/App.tsx` - メインアプリケーション

---

**作成日**: 2025-11-25
**Phase**: 2
**ステータス**: 完了
