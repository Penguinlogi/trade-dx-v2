# Render.com デプロイ チェックリスト

## 📋 デプロイ前の確認事項

### バックエンド（Web Service）

- [ ] `requirements.txt`に`gunicorn`が含まれている
- [ ] `backend/app/main.py`が正しく設定されている
- [ ] 環境変数の値が準備されている
  - [ ] `DATABASE_URL`
  - [ ] `SECRET_KEY`
  - [ ] `ALGORITHM`
  - [ ] `ACCESS_TOKEN_EXPIRE_MINUTES`
  - [ ] `CORS_ORIGINS`（フロントエンドURL確定後に設定）
  - [ ] `LOG_LEVEL`
  - [ ] `DEBUG=False`

### フロントエンド（Static Site）

- [ ] `package.json`のビルドスクリプトが正しい
- [ ] `vite.config.ts`が正しく設定されている
- [ ] 環境変数の値が準備されている
  - [ ] `VITE_API_BASE_URL`（バックエンドURL確定後に設定）

### データベース

- [ ] PostgreSQL接続情報が正しい
- [ ] マイグレーションファイルが最新である
- [ ] 本番環境用のデータベースが準備されている

### Gitリポジトリ

- [ ] 最新のコードが`master`ブランチにプッシュされている
- [ ] コミットメッセージが適切である

---

## 🚀 デプロイ手順

### ステップ1: バックエンドのデプロイ

1. [ ] Renderダッシュボードで「New +」→「Web Service」を選択
2. [ ] GitHubリポジトリを接続（`Penguinlogi/trade-dx-v2`）
3. [ ] 基本設定を入力
   - [ ] Name: `trade-dx-v2`
   - [ ] Branch: `master`
   - [ ] Root Directory: `backend`
   - [ ] Build Command: `pip install -r requirements.txt`
   - [ ] Start Command: `gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
4. [ ] 環境変数を設定（上記の環境変数一覧を参照）
5. [ ] 「Create Web Service」をクリック
6. [ ] デプロイ完了を待つ（5-10分）
7. [ ] バックエンドURLを確認（例: `https://trade-dx-v2.onrender.com`）
8. [ ] ヘルスチェックを実行: `https://trade-dx-v2.onrender.com/health`

### ステップ2: データベースマイグレーション

1. [ ] Render Shellでバックエンドに接続
2. [ ] マイグレーションを実行: `cd backend && alembic upgrade head`
3. [ ] マイグレーション成功を確認

### ステップ3: フロントエンドのデプロイ

1. [ ] Renderダッシュボードで「New +」→「Static Site」を選択
2. [ ] GitHubリポジトリを選択（`Penguinlogi/trade-dx-v2`）
3. [ ] 基本設定を入力
   - [ ] Name: `trade-dx-frontend`
   - [ ] Branch: `master`
   - [ ] Root Directory: `frontend`
   - [ ] Build Command: `npm install && npm run build`
   - [ ] Publish Directory: `dist`
4. [ ] 環境変数を設定
   - [ ] `VITE_API_BASE_URL`: バックエンドURL（ステップ1で取得）
5. [ ] 「Create Static Site」をクリック
6. [ ] デプロイ完了を待つ（3-5分）
7. [ ] フロントエンドURLを確認（例: `https://trade-dx-frontend.onrender.com`）

### ステップ4: CORS設定の更新

1. [ ] バックエンドのWeb Service設定を開く
2. [ ] 「Environment」セクションで`CORS_ORIGINS`を更新
   - [ ] 値: フロントエンドURL（ステップ3で取得）
3. [ ] 「Save Changes」をクリック
4. [ ] 自動再デプロイの完了を待つ

---

## ✅ 動作確認

### バックエンド

- [ ] ヘルスチェック: `https://trade-dx-v2.onrender.com/health`
  - 期待されるレスポンス: `{"status": "healthy", ...}`
- [ ] APIルート: `https://trade-dx-v2.onrender.com/`
  - 期待されるレスポンス: `{"message": "貿易DX管理システム API", ...}`

### フロントエンド

- [ ] フロントエンドURLにアクセス
- [ ] ログインページが表示される
- [ ] テストユーザーでログインできる
- [ ] 各種機能が正常に動作する
  - [ ] 案件一覧の表示
  - [ ] 顧客マスタの表示
  - [ ] 商品マスタの表示
  - [ ] 分析・集計機能
  - [ ] ドキュメント生成

### 統合確認

- [ ] ブラウザの開発者ツールでネットワークエラーがない
- [ ] CORSエラーがない
- [ ] WebSocket接続が正常に動作する（該当する場合）

---

## 🔧 トラブルシューティング

### デプロイが失敗する場合

1. [ ] Renderダッシュボードの「Logs」タブでエラーログを確認
2. [ ] ローカル環境で同じコマンドを実行して再現する
3. [ ] 環境変数が正しく設定されているか確認

### データベース接続エラーの場合

1. [ ] `DATABASE_URL`が正しいか確認
2. [ ] PostgreSQLが起動しているか確認
3. [ ] 接続文字列の形式を確認

### CORSエラーの場合

1. [ ] バックエンドの`CORS_ORIGINS`にフロントエンドURLが含まれているか確認
2. [ ] フロントエンドの`VITE_API_BASE_URL`が正しいか確認
3. [ ] 環境変数変更後に再デプロイが完了しているか確認

### スリープ後の初回アクセスが遅い場合

- [ ] これはRender無料プランの正常な動作です
- [ ] 有料プランにアップグレードするか、外部pingサービスを使用

---

## 📝 デプロイ後のメンテナンス

### 定期的な確認

- [ ] ログの確認（週1回）
- [ ] データベースのバックアップ確認（週1回）
- [ ] パフォーマンス監視（月1回）
- [ ] セキュリティ確認（月1回）

### アップデート手順

1. [ ] ローカル環境で変更をコミット・プッシュ
2. [ ] Renderが自動的にデプロイを開始
3. [ ] デプロイ完了後、動作確認
4. [ ] 問題があれば、前のバージョンにロールバック

---

## 📞 サポート

問題が発生した場合:
1. [ ] 本チェックリストを確認
2. [ ] `RENDER_DEPLOYMENT_GUIDE.md`のトラブルシューティングを確認
3. [ ] Renderダッシュボードのログを確認
4. [ ] 必要に応じて開発チームに連絡
