# Phase 2: 認証機能 - README

## 📋 概要

Phase 2では、JWT（JSON Web Token）を使用したユーザー認証システムを実装しました。
これにより、ユーザーは安全にログイン・ログアウトでき、認証が必要なページへのアクセスが保護されます。

## ✨ 実装した機能

### バックエンド
- ✅ JWT認証システム（トークン生成・検証）
- ✅ パスワードハッシュ化（bcrypt）
- ✅ 認証APIエンドポイント
  - POST /api/auth/login - ログイン
  - POST /api/auth/logout - ログアウト
  - GET /api/auth/me - ユーザー情報取得
  - POST /api/auth/refresh - トークンリフレッシュ
- ✅ 認証ミドルウェア（依存性注入）

### フロントエンド
- ✅ ログイン画面（Material-UI）
- ✅ 認証コンテキスト（React Context API）
- ✅ プライベートルート（認証保護）
- ✅ トークン管理（LocalStorage）
- ✅ 自動ログアウト（30分）
- ✅ ダッシュボード画面

## 🚀 クイックスタート

### ⚠️ 重要事項

#### 1. コマンドプロンプトで実行してください

**すべてのコマンドは、Windowsのコマンドプロンプトで実行してください。**
- ❌ Pythonインタープリター（`>>>` プロンプト）では実行できません
- ✅ コマンドプロンプト（`C:\...>` プロンプト）で実行してください

**もし `>>>` が表示されている場合は、`exit()` と入力してPythonを終了してください。**

#### 2. プロジェクトのルートディレクトリに移動してください

まず、コマンドプロンプトでプロジェクトのルートディレクトリに移動してください：

```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"
```

### 1. バックエンドの起動

```cmd
cd backend
py -3 -m pip install -r requirements.txt
py -3 -m scripts.seed_data  # 初回のみ
py -3 -m app.main
```

バックエンドが http://localhost:8000 で起動します。

### 2. フロントエンドの起動

新しいコマンドプロンプトを開いて：

```cmd
# プロジェクトのルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"

# フロントエンドに移動
cd frontend
npm install  # 初回のみ
npm run dev
```

フロントエンドが http://localhost:3000 で起動します。

### 3. ログイン

ブラウザで http://localhost:3000 にアクセスし、以下のアカウントでログイン：

- **ユーザー名**: `admin`
- **パスワード**: `admin123`

## 🔐 テストアカウント

| ユーザー名 | パスワード | 権限 | フルネーム |
|-----------|----------|------|-----------|
| admin | admin123 | 管理者 | 管理者 |
| yamada | yamada123 | 一般 | 山田太郎 |
| suzuki | suzuki123 | 一般 | 鈴木花子 |

## 📡 APIエンドポイント

### 認証API

| メソッド | エンドポイント | 説明 | 認証 |
|---------|--------------|------|------|
| POST | /api/auth/login | ログイン | 不要 |
| POST | /api/auth/logout | ログアウト | 必要 |
| GET | /api/auth/me | 現在のユーザー情報取得 | 必要 |
| POST | /api/auth/refresh | トークンリフレッシュ | 必要 |

### Swagger UI

APIドキュメントは以下のURLで確認できます：
http://localhost:8000/docs

## 📂 ファイル構造

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── auth.py          # 認証エンドポイント
│   ├── core/
│   │   ├── security.py          # JWT認証・パスワードハッシュ化
│   │   └── deps.py              # 認証依存性注入
│   ├── schemas/
│   │   ├── user.py              # ユーザースキーマ
│   │   └── auth.py              # 認証スキーマ
│   └── main.py                  # メインアプリケーション

frontend/
├── src/
│   ├── api/
│   │   ├── axios.ts             # Axios設定
│   │   └── auth.ts              # 認証API
│   ├── components/
│   │   └── PrivateRoute.tsx     # プライベートルート
│   ├── context/
│   │   └── AuthContext.tsx      # 認証コンテキスト
│   ├── pages/
│   │   ├── LoginPage.tsx        # ログイン画面
│   │   └── DashboardPage.tsx    # ダッシュボード
│   ├── types/
│   │   └── auth.ts              # 認証型定義
│   └── App.tsx                  # メインアプリケーション
```

## 🔧 技術スタック

### バックエンド
- FastAPI
- SQLAlchemy
- python-jose（JWT）
- passlib + bcrypt（パスワードハッシュ化）

### フロントエンド
- React 18 + TypeScript
- React Router
- Material-UI (MUI)
- Axios
- React Context API

## 📝 使い方

### ログイン
1. http://localhost:3000 にアクセス
2. ユーザー名とパスワードを入力
3. 「ログイン」ボタンをクリック
4. ダッシュボードに遷移

### ログアウト
1. ダッシュボード右上のログアウトアイコン（🚪）をクリック
2. ログイン画面に遷移

### 認証保護
- 未認証状態でダッシュボードにアクセスしようとすると、自動的にログイン画面にリダイレクトされます
- トークンの有効期限は30分です
- 25分後に警告メッセージが表示されます
- 30分後に自動的にログアウトされます

## 🧪 動作確認

詳細な動作確認手順は以下のドキュメントを参照してください：

📖 [Phase2_手動操作手順書.md](./Phase2_手動操作手順書.md)

### 基本的な確認項目
- [ ] バックエンドが起動する
- [ ] フロントエンドが起動する
- [ ] ログインできる
- [ ] ダッシュボードが表示される
- [ ] ユーザー情報が正しく表示される
- [ ] ログアウトできる
- [ ] 未認証でアクセスできない

## 🐛 トラブルシューティング

### 「Fatal error in launcher」エラー

**症状1: pipコマンド実行時**
```
Fatal error in launcher: Unable to create process using '"C:\Users\??\AppData\Local\Programs\Python\Python314\python.exe"'
```

**症状2: Pythonスクリプト実行時**
```
[ERROR] Failed to launch 'C:\Users\??\AppData\Local\Python\pythoncore-3.14-64\python.exe': the install path was not found (0x0002).
```

**原因:**
ユーザー名に日本語が含まれているため、`python` コマンド自体がPythonランチャーを経由してエラーになる

**解決方法:**
**すべてのPythonコマンドで `py -3` を使用してください：**

```cmd
# 依存パッケージのインストール
py -3 -m pip install -r requirements.txt

# シードデータ投入
py -3 -m scripts.seed_data

# データベース確認
py -3 -m scripts.check_database

# バックエンド起動
py -3 -m app.main
```

**重要:** `python` ではなく `py -3` を使用することで、日本語パスの問題を完全に回避できます。

### 「SyntaxError: (unicode error)」エラー

**症状:**
```
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
>>>
```

**原因:**
Pythonインタープリター（`>>>` プロンプト）でコマンドを実行しようとしている

**解決方法:**
1. `exit()` と入力してPythonを終了
2. コマンドプロンプト（`C:\...>` プロンプト）に戻る
3. コマンドを再度実行

### 「指定されたパスが見つかりません」エラー

**症状:**
```
C:\Users\関伸>cd backend
指定されたパスが見つかりません。
```

**解決方法:**
まずプロジェクトのルートディレクトリに移動してください：
```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"
```

その後、`backend` に移動：
```cmd
cd backend
```

### 「sqlite3は認識されていません」エラー

**症状:**
```
'sqlite3' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

**解決方法:**
Pythonスクリプトを使ってデータベースを確認してください：
```cmd
cd backend
py -3 -m scripts.check_database
```

### バックエンドが起動しない

**解決方法:**
```cmd
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"
py -3 -m pip install -r requirements.txt
```

### フロントエンドからバックエンドに接続できない
1. バックエンドが起動していることを確認
2. `frontend/.env` を確認:
   ```
   VITE_API_BASE_URL=http://localhost:8000
   ```
3. フロントエンドを再起動

### ログインできない
1. シードデータが投入されていることを確認:

   ```cmd
   cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX\backend"
   py -3 -m scripts.seed_data
   ```

2. 正しいパスワードを使用（admin / admin123）

## 📚 関連ドキュメント

- [Phase2.md](./Phase2.md) - Phase 2の詳細な進捗メモ
- [Phase2_手動操作手順書.md](./Phase2_手動操作手順書.md) - 詳細な動作確認手順
- [全体進捗管理書.md](../全体進捗管理書.md) - プロジェクト全体の進捗

## 🎯 次のステップ

Phase 3: 案件管理API の開発に進みます。

### Phase 3の主要タスク
- 案件CRUD API の実装
- 案件一覧画面の作成
- 案件登録・編集フォームの作成
- 案件番号自動生成機能の移植

---

**作成日**: 2025-11-25
**Phase**: 2
**ステータス**: ✅ 完了
