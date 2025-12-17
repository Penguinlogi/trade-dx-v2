# Render.com デプロイ手順書

## 📋 目次
1. [概要](#概要)
2. [前提条件](#前提条件)
3. [バックエンド（Web Service）のデプロイ](#バックエンドweb-serviceのデプロイ)
4. [フロントエンド（Static Site）のデプロイ](#フロントエンドstatic-siteのデプロイ)
5. [データベースマイグレーション](#データベースマイグレーション)
6. [環境変数の設定](#環境変数の設定)
7. [動作確認](#動作確認)
8. [トラブルシューティング](#トラブルシューティング)

---

## 概要

本ドキュメントでは、Render.comの無料プランを使用して貿易DX管理システムをデプロイする手順を説明します。

### デプロイ構成
- **バックエンド**: Render Web Service（FastAPI + Gunicorn）
- **フロントエンド**: Render Static Site（React + Vite）
- **データベース**: Render PostgreSQL（既存のPostgreSQLを使用）

### 予想されるURL
- バックエンド: `https://trade-dx-v2.onrender.com`
- フロントエンド: `https://trade-dx-frontend.onrender.com`

---

## 前提条件

1. **Render.comアカウント**
   - [Render.com](https://render.com)でアカウントを作成
   - GitHubアカウントと連携

2. **GitHubリポジトリ**
   - リポジトリURL: `https://github.com/Penguinlogi/trade-dx-v2.git`
   - ブランチ: `master`

3. **必要な情報**
   - データベース接続情報（既に提供済み）
   - 環境変数の値（既に提供済み）

---

## バックエンド（Web Service）のデプロイ

### ステップ1: Web Serviceの作成

1. Renderダッシュボードにログイン
2. 「New +」ボタンをクリック
3. 「Web Service」を選択
4. GitHubリポジトリを接続（初回のみ）
   - 「Connect account」をクリック
   - GitHubアカウントを認証
   - リポジトリ `Penguinlogi/trade-dx-v2` を選択

### ステップ2: 基本設定

以下の設定を入力：

| 項目 | 値 |
|------|-----|
| **Name** | `trade-dx-v2` |
| **Region** | `Singapore`（または最寄りのリージョン） |
| **Branch** | `master` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |

### ステップ3: 環境変数の設定

「Environment」セクションで以下の環境変数を追加：

| 変数名 | 値 |
|--------|-----|
| `DATABASE_URL` | `postgresql://trade_dx_user:eWTIvR3Vw2999cXZ5vukx2uDeTp93Lwr@dpg-d4vql1re5dus73akhge0-a/trade_dx` |
| `SECRET_KEY` | `unjyLKd_BdeRoiAQdozo1_k402fEDqPSP8QqxLD1nI4` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `480` |
| `CORS_ORIGINS` | `https://trade-dx-frontend.onrender.com` |
| `LOG_LEVEL` | `INFO` |
| `DEBUG` | `False` |

**重要**: フロントエンドのURLが確定するまで、`CORS_ORIGINS`は後で更新する必要があります。

### ステップ4: デプロイの開始

1. 「Create Web Service」をクリック
2. デプロイが開始されます（初回は5-10分かかります）
3. デプロイ完了後、URLが表示されます（例: `https://trade-dx-v2.onrender.com`）

### ステップ5: 動作確認

デプロイ完了後、以下のURLで動作確認：

- ヘルスチェック: `https://trade-dx-v2.onrender.com/health`
- APIルート: `https://trade-dx-v2.onrender.com/`

期待されるレスポンス:
```json
{
  "status": "healthy",
  "app_name": "貿易DX管理システム",
  "version": "2.1.0"
}
```

---

## フロントエンド（Static Site）のデプロイ

### ステップ1: Static Siteの作成

1. Renderダッシュボードで「New +」をクリック
2. 「Static Site」を選択
3. GitHubリポジトリを選択（既に接続済みの場合は選択）

### ステップ2: 基本設定

以下の設定を入力：

| 項目 | 値 |
|------|-----|
| **Name** | `trade-dx-frontend` |
| **Branch** | `master` |
| **Root Directory** | `frontend` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `dist` |

### ステップ3: 環境変数の設定

「Environment Variables」セクションで以下を追加：

| 変数名 | 値 |
|--------|-----|
| `VITE_API_BASE_URL` | `https://trade-dx-v2.onrender.com` |

**重要**: バックエンドのURLが確定してから設定してください。

### ステップ4: デプロイの開始

1. 「Create Static Site」をクリック
2. デプロイが開始されます（初回は3-5分かかります）
3. デプロイ完了後、URLが表示されます（例: `https://trade-dx-frontend.onrender.com`）

### ステップ5: バックエンドのCORS設定を更新

フロントエンドのURLが確定したら、バックエンドの環境変数を更新：

1. バックエンドのWeb Service設定を開く
2. 「Environment」セクションで `CORS_ORIGINS` を更新
   - 値: `https://trade-dx-frontend.onrender.com`（実際のURLに置き換え）
3. 「Save Changes」をクリック
4. 自動的に再デプロイが開始されます

---

## データベースマイグレーション

### ステップ1: ローカル環境での確認

本番環境にデプロイする前に、マイグレーションファイルが最新であることを確認：

```bash
cd backend
alembic current
alembic heads
```

### ステップ2: Render Shellでのマイグレーション実行

1. RenderダッシュボードでバックエンドのWeb Serviceを開く
2. 「Shell」タブをクリック
3. 以下のコマンドを実行：

```bash
cd backend
alembic upgrade head
```

### 代替方法: デプロイ時に自動実行

Renderの「Build Command」を以下のように変更することで、デプロイ時に自動的にマイグレーションを実行できます：

```bash
pip install -r requirements.txt && cd backend && alembic upgrade head
```

**注意**: この方法は、マイグレーションエラー時にデプロイが失敗するため、慎重に使用してください。

---

## 環境変数の設定

### バックエンド環境変数一覧

| 変数名 | 説明 | デフォルト値 | 本番値 |
|--------|------|-------------|--------|
| `DATABASE_URL` | PostgreSQL接続文字列 | `sqlite:///./trade_dx.db` | 提供済み |
| `SECRET_KEY` | JWT署名用秘密鍵 | `your-secret-key-here...` | 提供済み |
| `ALGORITHM` | JWTアルゴリズム | `HS256` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | トークン有効期限（分） | `30` | `480` |
| `CORS_ORIGINS` | CORS許可オリジン | `*` | フロントエンドURL |
| `LOG_LEVEL` | ログレベル | `INFO` | `INFO` |
| `DEBUG` | デバッグモード | `True` | `False` |

### フロントエンド環境変数一覧

| 変数名 | 説明 | 本番値 |
|--------|------|--------|
| `VITE_API_BASE_URL` | バックエンドAPIのベースURL | `https://trade-dx-v2.onrender.com` |

**注意**: Viteの環境変数は `VITE_` プレフィックスが必要です。

---

## 動作確認

### 1. バックエンドの確認

#### ヘルスチェック
```bash
curl https://trade-dx-v2.onrender.com/health
```

期待されるレスポンス:
```json
{
  "status": "healthy",
  "app_name": "貿易DX管理システム",
  "version": "2.1.0"
}
```

#### APIエンドポイント確認
```bash
curl https://trade-dx-v2.onrender.com/
```

### 2. フロントエンドの確認

1. ブラウザで `https://trade-dx-frontend.onrender.com` にアクセス
2. ログインページが表示されることを確認
3. テストユーザーでログインを試行

### 3. 統合確認

1. フロントエンドからログイン
2. 各種機能（案件一覧、顧客マスタなど）が正常に動作することを確認
3. ブラウザの開発者ツールでネットワークエラーがないか確認

---

## トラブルシューティング

### 問題1: デプロイが失敗する

**原因と対処法**:
- **Buildエラー**: `requirements.txt`の依存関係を確認
- **Startエラー**: Start Commandが正しいか確認
- **環境変数エラー**: 必須環境変数が設定されているか確認

**確認方法**:
1. Renderダッシュボードの「Logs」タブでエラーログを確認
2. ローカル環境で同じコマンドを実行して再現する

### 問題2: データベース接続エラー

**原因と対処法**:
- `DATABASE_URL`が正しく設定されているか確認
- PostgreSQLが起動しているか確認（Render PostgreSQLの場合）
- 接続文字列の形式を確認（`postgresql://`で始まる必要がある）

**確認方法**:
```bash
# Render Shellで実行
cd backend
python -c "from app.core.database import engine; print(engine.url)"
```

### 問題3: CORSエラー

**原因と対処法**:
- バックエンドの `CORS_ORIGINS` にフロントエンドのURLが含まれているか確認
- フロントエンドの `VITE_API_BASE_URL` が正しいか確認

**確認方法**:
1. ブラウザの開発者ツールでコンソールエラーを確認
2. ネットワークタブでリクエストヘッダーを確認

### 問題4: スリープ後の初回アクセスが遅い

**原因**: Render無料プランは、一定時間アイドル状態になるとスリープします。

**対処法**:
- 有料プランにアップグレード（常時起動）
- 外部のpingサービスを使用して定期的にアクセス（無料プランでも可能）

### 問題5: 環境変数が反映されない

**原因と対処法**:
- 環境変数を追加・変更した後、再デプロイが必要
- フロントエンドの環境変数はビルド時に埋め込まれるため、変更後は再ビルドが必要

**確認方法**:
1. Renderダッシュボードで環境変数が正しく設定されているか確認
2. 再デプロイを実行

---

## デプロイ後のメンテナンス

### 定期的な確認項目

1. **ログの確認**
   - Renderダッシュボードの「Logs」タブでエラーがないか確認
   - 定期的にログを確認して異常を早期発見

2. **データベースのバックアップ**
   - Render PostgreSQLのバックアップ設定を確認
   - 必要に応じて手動バックアップを実行

3. **パフォーマンス監視**
   - Renderダッシュボードでリソース使用状況を確認
   - 必要に応じてプランアップグレードを検討

4. **セキュリティ**
   - 環境変数（特に `SECRET_KEY`）が漏洩していないか確認
   - 定期的に `SECRET_KEY` を更新

### アップデート手順

1. ローカル環境で変更をコミット・プッシュ
2. Renderが自動的にデプロイを開始
3. デプロイ完了後、動作確認
4. 問題があれば、前のバージョンにロールバック

---

## 参考リンク

- [Render公式ドキュメント](https://render.com/docs)
- [FastAPIデプロイガイド](https://fastapi.tiangolo.com/deployment/)
- [Vite環境変数](https://vitejs.dev/guide/env-and-mode.html)

---

## サポート

問題が発生した場合:
1. 本ドキュメントのトラブルシューティングを確認
2. Renderダッシュボードのログを確認
3. 必要に応じて開発チームに連絡
