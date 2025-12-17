# Render.com Static Site SPA設定

## 問題

React Routerなどのクライアントサイドルーティングを使用しているSPA（Single Page Application）をRender.comのStatic Siteとしてデプロイする場合、`/login`や`/cases`などのパスに直接アクセスすると404エラーが発生します。

これは、サーバーがこれらのパスに対応するファイルを探すが、実際には`index.html`にリダイレクトする必要があるためです。

## 解決方法

Render.comのStatic Siteでは、以下の方法でリダイレクトを設定できます。

### 方法1: Render.comダッシュボードで設定（推奨）

1. **Render.comダッシュボードにログイン**
   - https://dashboard.render.com/ にアクセス

2. **フロントエンドサービスを開く**
   - 「Static Sites」→ `trade-dx-frontend` をクリック

3. **Settingsタブを開く**

4. **「Redirects/Rewrites」セクションを探す**
   - もしこのセクションが見つからない場合は、「Environment」セクションの下にあります

5. **リダイレクトルールを追加**
   - 「Add Redirect/Rewrite」ボタンをクリック
   - 以下の設定を入力：
     - **Source Path**: `/*`
     - **Destination Path**: `/index.html`
     - **Type**: `Rewrite` または `Redirect (200)`
   - 「Save」をクリック

6. **再デプロイ**
   - 設定を保存すると、自動的に再デプロイが開始されます
   - または、「Manual Deploy」から「Deploy latest commit」をクリック

### 方法2: render.yamlファイルを使用

プロジェクトのルートに`render.yaml`ファイルを作成：

```yaml
services:
  - type: web
    name: trade-dx-v2
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        sync: false
      # ... 他の環境変数

static_sites:
  - name: trade-dx-frontend
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    headers:
      - path: /*
        name: X-Frame-Options
        value: DENY
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

### 方法3: _redirectsファイルを使用（Netlify形式）

`frontend/public/_redirects`ファイルを作成（既に作成済み）：

```
/*    /index.html   200
```

**注意**: Render.comでは、`_redirects`ファイルが自動的に認識されない場合があります。この場合は、方法1（ダッシュボード設定）を使用してください。

---

## 設定後の確認

1. **設定を保存後、数分待つ**（再デプロイが完了するまで）

2. **ブラウザのキャッシュをクリア**
   - Ctrl+Shift+Delete（Windows/Linux）
   - Cmd+Shift+Delete（Mac）

3. **直接`/login`パスにアクセス**
   ```
   https://trade-dx-frontend.onrender.com/login
   ```
   - 404エラーが表示されず、ログインページが表示されることを確認

4. **ブラウザの開発者ツールで確認**
   - F12キーで開発者ツールを開く
   - Networkタブで404エラーが解消されているか確認

---

## トラブルシューティング

### 設定が反映されない場合

1. **再デプロイを実行**
   - Render.comダッシュボードで「Manual Deploy」→「Deploy latest commit」

2. **ブラウザのキャッシュを完全にクリア**
   - シークレットモードで試す

3. **別のブラウザで試す**

### リダイレクトルールが正しく動作しない場合

- **Source Path**: `/*` と設定（すべてのパスを対象）
- **Destination Path**: `/index.html` と設定（必ずスラッシュで始まる）
- **Type**: `Rewrite` または `Redirect (200)` を選択（301や302ではなく）

---

**最終更新**: 2025-12-01

