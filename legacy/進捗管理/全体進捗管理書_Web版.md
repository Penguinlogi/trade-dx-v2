# 貿易DX V2.1 - Webアプリケーション開発 全体進捗管理書

## プロジェクト概要
- **プロジェクト名**: 貿易DX管理システム V2.1 (Webアプリ版)
- **アーキテクチャ**: React + TypeScript + FastAPI + PostgreSQL
- **開始日**: 2025-11-21
- **目標完了日**: 2025-12-19 (4週間)
- **現在ステータス**: Phase 1 開始

## 進捗サマリー
- **現在フェーズ**: Phase 1 (環境構築) - 準備中
- **全体進捗**: 0% (0/9 フェーズ完了)
- **最終更新**: 2025-11-21

---

## Phase 1: 環境構築とデータベース設計 (3日)
**ステータス**: ⬜ 未着手  
**開始日**: 2025-11-21  
**完了日**: -

### Day 1: プロジェクト初期化
- [ ] ディレクトリ構造の作成
- [ ] バックエンド初期化
  - [ ] FastAPI プロジェクト作成
  - [ ] requirements.txt 作成
  - [ ] main.py 作成
  - [ ] config.py 作成
  - [ ] __init__.py 各階層に作成
- [ ] フロントエンド初期化
  - [ ] React + Vite プロジェクト作成
  - [ ] package.json 設定
  - [ ] TypeScript 設定
  - [ ] ESLint/Prettier 設定
  - [ ] vite.config.ts 設定
- [ ] Docker環境構築
  - [ ] docker-compose.yml 作成
  - [ ] Dockerfile (backend)
  - [ ] Dockerfile (frontend)
  - [ ] .dockerignore 作成
- [ ] 環境変数設定
  - [ ] .env.example 作成
  - [ ] .gitignore 更新

### Day 2: データベース設計
- [ ] ER図の作成
- [ ] テーブル定義書の作成
- [ ] SQLAlchemy モデル作成
  - [ ] Base モデル
  - [ ] User モデル
  - [ ] Customer モデル
  - [ ] Product モデル
  - [ ] Case モデル
  - [ ] ChangeHistory モデル
  - [ ] CaseNumber モデル
- [ ] Alembic セットアップ
  - [ ] alembic init
  - [ ] env.py 設定
  - [ ] alembic.ini 設定

### Day 3: データベース実装とマイグレーション
- [ ] 初期マイグレーションファイル生成
- [ ] マイグレーション実行確認
- [ ] シードデータスクリプト作成
  - [ ] ユーザーデータ
  - [ ] 顧客マスタデータ
  - [ ] 商品マスタデータ
  - [ ] サンプル案件データ
- [ ] データベース接続テスト
- [ ] CRUD操作の基本テスト

### 成果物
- [ ] backend/ ディレクトリ (FastAPI)
- [ ] frontend/ ディレクトリ (React)
- [ ] docker-compose.yml
- [ ] requirements.txt
- [ ] package.json
- [ ] ER図
- [ ] テーブル定義書
- [ ] マイグレーションファイル

### Git管理
- [ ] git add .
- [ ] git commit -m "Phase 1: 環境構築とDB設計完了"
- [ ] git tag web-phase1-complete

---

## Phase 2: 認証機能 (2日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### Day 1: バックエンド認証
- [ ] JWT認証実装
  - [ ] app/core/security.py 作成
  - [ ] パスワードハッシュ化 (bcrypt)
  - [ ] トークン生成関数
  - [ ] トークン検証関数
- [ ] 認証エンドポイント実装
  - [ ] POST /api/auth/login
  - [ ] POST /api/auth/logout
  - [ ] GET /api/auth/me
  - [ ] POST /api/auth/refresh
- [ ] 認証依存関係
  - [ ] app/api/deps.py 作成
  - [ ] get_current_user() 関数
  - [ ] get_current_active_user() 関数
- [ ] Pydanticスキーマ
  - [ ] TokenSchema
  - [ ] UserSchema

### Day 2: フロントエンド認証
- [ ] ログイン画面作成
  - [ ] pages/Login/index.tsx
  - [ ] フォームコンポーネント
  - [ ] バリデーション
- [ ] 認証Context
  - [ ] context/AuthContext.tsx
  - [ ] useAuth フック
- [ ] PrivateRoute コンポーネント
- [ ] API クライアント
  - [ ] api/auth.ts
  - [ ] axios インスタンス設定
  - [ ] インターセプター設定
- [ ] トークン管理
  - [ ] localStorage/sessionStorage
  - [ ] 自動ログアウト機能

### 成果物
- [ ] app/core/security.py
- [ ] app/api/endpoints/auth.py
- [ ] app/api/deps.py
- [ ] pages/Login/
- [ ] context/AuthContext.tsx
- [ ] 認証機能テストケース

### Git管理
- [ ] git commit -m "Phase 2: 認証機能完了"
- [ ] git tag web-phase2-complete

---

## Phase 3: 案件管理API (4日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### Day 1: 案件CRUD - バックエンド
- [ ] 案件モデル拡張
- [ ] 案件スキーマ作成
  - [ ] CaseCreate
  - [ ] CaseUpdate
  - [ ] CaseResponse
  - [ ] CaseListResponse
- [ ] 案件エンドポイント実装
  - [ ] GET /api/cases (一覧取得)
  - [ ] GET /api/cases/{id} (詳細取得)
  - [ ] POST /api/cases (新規作成)
  - [ ] PUT /api/cases/{id} (更新)
  - [ ] DELETE /api/cases/{id} (削除)
- [ ] フィルタリング機能
  - [ ] 区分フィルター
  - [ ] ステータスフィルター
  - [ ] 日付範囲フィルター
- [ ] 検索機能
  - [ ] 案件番号検索
  - [ ] 顧客名検索
  - [ ] 商品名検索

### Day 2: 案件CRUD - フロントエンド
- [ ] 案件一覧画面
  - [ ] pages/Cases/index.tsx
  - [ ] DataTable コンポーネント
  - [ ] ページネーション
  - [ ] ソート機能
- [ ] フィルター・検索UI
  - [ ] SearchBar コンポーネント
  - [ ] FilterPanel コンポーネント
- [ ] API連携
  - [ ] api/cases.ts
  - [ ] React Query セットアップ
  - [ ] hooks/useCases.ts

### Day 3: 案件フォーム
- [ ] 新規作成モーダル
  - [ ] components/CaseFormModal.tsx
  - [ ] React Hook Form セットアップ
  - [ ] Zodバリデーション
- [ ] 編集モーダル
- [ ] フォームフィールド
  - [ ] 基本情報
  - [ ] 顧客選択
  - [ ] 商品選択
  - [ ] 金額・数量
  - [ ] 日付
- [ ] エラーハンドリング
- [ ] 成功/エラートースト

### Day 4: 案件番号自動生成
- [ ] 案件番号生成サービス
  - [ ] app/services/case_number.py (legacy移植)
  - [ ] POST /api/case-numbers/generate
  - [ ] 案件種別ごとの採番
- [ ] CaseNumberモデル
- [ ] トランザクション制御
- [ ] スレッドセーフ実装
- [ ] テストケース

### 成果物
- [ ] app/api/endpoints/cases.py
- [ ] app/services/case_number.py
- [ ] pages/Cases/
- [ ] components/CaseFormModal.tsx
- [ ] hooks/useCases.ts

### Git管理
- [ ] git commit -m "Phase 3: 案件管理API完了"
- [ ] git tag web-phase3-complete

---

## Phase 4: マスタ管理 (3日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### Day 1: 顧客マスタ
- [ ] 顧客マスタAPI
  - [ ] GET /api/customers
  - [ ] POST /api/customers
  - [ ] PUT /api/customers/{id}
  - [ ] DELETE /api/customers/{id}
- [ ] 顧客マスタスキーマ
- [ ] 顧客マスタ画面
  - [ ] pages/Customers/
  - [ ] 一覧表示
  - [ ] 登録・編集フォーム
  - [ ] 検索・フィルター

### Day 2: 商品マスタ
- [ ] 商品マスタAPI
  - [ ] GET /api/products
  - [ ] POST /api/products
  - [ ] PUT /api/products/{id}
  - [ ] DELETE /api/products/{id}
- [ ] 商品マスタスキーマ
- [ ] 商品マスタ画面
  - [ ] pages/Products/
  - [ ] 一覧表示
  - [ ] 登録・編集フォーム
  - [ ] 検索・フィルター

### Day 3: マスタ連携
- [ ] 案件フォームでの顧客選択UI
- [ ] 案件フォームでの商品選択UI
- [ ] オートコンプリートコンポーネント
- [ ] マスタデータキャッシュ
- [ ] 統合テスト

### 成果物
- [ ] app/api/endpoints/customers.py
- [ ] app/api/endpoints/products.py
- [ ] pages/Customers/
- [ ] pages/Products/
- [ ] components/AutoComplete/

### Git管理
- [ ] git commit -m "Phase 4: マスタ管理完了"
- [ ] git tag web-phase4-complete

---

## Phase 5: ダッシュボード・集計機能 (2日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### Day 1: 集計API
- [ ] 集計サービス作成
  - [ ] app/services/analytics.py
- [ ] 集計エンドポイント
  - [ ] GET /api/analytics/summary
  - [ ] GET /api/analytics/trends
  - [ ] GET /api/analytics/by-customer
  - [ ] GET /api/analytics/by-status
- [ ] SQLAlchemy 集計クエリ
- [ ] キャッシュ機能 (Redis オプション)

### Day 2: ダッシュボード画面
- [ ] pages/Dashboard/index.tsx
- [ ] サマリーカード
  - [ ] 総売上
  - [ ] 総粗利
  - [ ] 平均粗利率
  - [ ] 案件数
- [ ] グラフコンポーネント
  - [ ] Recharts セットアップ
  - [ ] 月次トレンドグラフ
  - [ ] ステータス分布円グラフ
  - [ ] 顧客別売上棒グラフ
- [ ] リアルタイム更新

### 成果物
- [ ] app/services/analytics.py
- [ ] app/api/endpoints/analytics.py
- [ ] pages/Dashboard/
- [ ] components/Charts/

### Git管理
- [ ] git commit -m "Phase 5: ダッシュボード完了"
- [ ] git tag web-phase5-complete

---

## Phase 6: ドキュメント生成機能 (3日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### Day 1: Invoice生成
- [ ] ドキュメント生成サービス
  - [ ] app/services/document.py
  - [ ] openpyxl 統合
- [ ] Invoiceテンプレート管理
- [ ] Invoice生成API
  - [ ] POST /api/documents/invoice/{case_id}
- [ ] PDFエクスポート (オプション)

### Day 2: Packing List生成
- [ ] Packing Listテンプレート
- [ ] Packing List生成API
  - [ ] POST /api/documents/packing-list/{case_id}
- [ ] ドキュメント履歴管理
  - [ ] Document モデル
  - [ ] GET /api/documents/history/{case_id}

### Day 3: フロントエンド統合
- [ ] ドキュメント生成ボタン
- [ ] プレビュー機能
- [ ] ダウンロード機能
- [ ] 生成履歴表示
- [ ] エラーハンドリング

### 成果物
- [ ] app/services/document.py
- [ ] app/api/endpoints/documents.py
- [ ] templates/ (Excelテンプレート)
- [ ] components/DocumentGenerator/

### Git管理
- [ ] git commit -m "Phase 6: ドキュメント生成完了"
- [ ] git tag web-phase6-complete

---

## Phase 7: 変更履歴・バックアップ (2日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### Day 1: 変更履歴機能
- [ ] 変更履歴記録ミドルウェア
  - [ ] app/middleware/audit.py
  - [ ] 自動記録機能
- [ ] 変更履歴API
  - [ ] GET /api/change-history
  - [ ] GET /api/change-history/{entity}/{id}
- [ ] 変更履歴画面
  - [ ] pages/ChangeHistory/
  - [ ] 差分表示コンポーネント

### Day 2: バックアップ機能
- [ ] バックアップサービス
  - [ ] app/services/backup.py (legacy移植)
  - [ ] データベースバックアップ
- [ ] バックアップAPI
  - [ ] POST /api/backups/create
  - [ ] GET /api/backups
  - [ ] POST /api/backups/restore/{id}
- [ ] スケジューラ統合
  - [ ] APScheduler セットアップ
  - [ ] 自動バックアップ (日次)
- [ ] バックアップ管理画面

### 成果物
- [ ] app/middleware/audit.py
- [ ] app/services/backup.py
- [ ] app/api/endpoints/change_history.py
- [ ] app/api/endpoints/backups.py
- [ ] pages/ChangeHistory/

### Git管理
- [ ] git commit -m "Phase 7: 履歴・バックアップ完了"
- [ ] git tag web-phase7-complete

---

## Phase 8: リアルタイム同期・通知 (1日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### タスクリスト
- [ ] WebSocket セットアップ
  - [ ] FastAPI WebSocketエンドポイント
  - [ ] WS /api/ws
- [ ] フロントエンドWebSocket
  - [ ] hooks/useWebSocket.ts
- [ ] リアルタイム更新通知
  - [ ] 案件更新通知
  - [ ] 新規案件通知
- [ ] サーバー状態表示
  - [ ] 接続状態インジケーター
  - [ ] 最終同期時刻表示
- [ ] オンラインユーザー表示 (オプション)

### 成果物
- [ ] app/api/endpoints/websocket.py
- [ ] hooks/useWebSocket.ts
- [ ] components/ConnectionStatus/

### Git管理
- [ ] git commit -m "Phase 8: リアルタイム機能完了"
- [ ] git tag web-phase8-complete

---

## Phase 9: テストとデバッグ (2日)
**ステータス**: ⬜ 未着手  
**開始日**: -  
**完了日**: -

### Day 1: バックエンドテスト
- [ ] pytest セットアップ
- [ ] 単体テスト
  - [ ] モデルテスト
  - [ ] サービステスト
  - [ ] APIテスト
- [ ] 統合テスト
  - [ ] エンドツーエンドフロー
- [ ] テストカバレッジ確認
  - [ ] pytest-cov
  - [ ] 80%以上を目標

### Day 2: フロントエンドテスト
- [ ] Vitest セットアップ
- [ ] コンポーネントテスト
  - [ ] React Testing Library
- [ ] E2Eテスト
  - [ ] Playwright セットアップ
  - [ ] 主要フロー確認
- [ ] エラーハンドリング確認
- [ ] パフォーマンステスト

### 成果物
- [ ] backend/tests/ (全テストケース)
- [ ] frontend/src/**/*.test.tsx
- [ ] e2e/ (E2Eテスト)
- [ ] テスト結果レポート
- [ ] カバレッジレポート

### Git管理
- [ ] git commit -m "Phase 9: テスト完了"
- [ ] git tag v2.1-web-complete

---

## 全体進捗
- Phase 1: ⬜ 0% (環境構築)
- Phase 2: ⬜ 0% (認証)
- Phase 3: ⬜ 0% (案件管理)
- Phase 4: ⬜ 0% (マスタ管理)
- Phase 5: ⬜ 0% (ダッシュボード)
- Phase 6: ⬜ 0% (ドキュメント生成)
- Phase 7: ⬜ 0% (履歴・バックアップ)
- Phase 8: ⬜ 0% (リアルタイム)
- Phase 9: ⬜ 0% (テスト)

**合計進捗: 0/9 (0%)**

---

## 技術スタック詳細

### バックエンド
- **Python**: 3.11+
- **FastAPI**: 0.104+
- **SQLAlchemy**: 2.0+
- **Alembic**: 1.12+
- **Pydantic**: 2.0+
- **python-jose**: JWT
- **bcrypt**: パスワードハッシュ
- **pytest**: テスト

### フロントエンド
- **React**: 18
- **TypeScript**: 5.0+
- **Vite**: 5.0+
- **Material-UI**: 5.14+ または Ant Design
- **React Query**: 5.0+
- **React Hook Form**: 7.47+
- **Zod**: 3.22+
- **Axios**: 1.6+
- **Recharts**: グラフ
- **Vitest**: テスト

### データベース
- **PostgreSQL**: 15+
- **SQLite**: 開発用オプション

### インフラ
- **Docker**: コンテナ化
- **Docker Compose**: 開発環境
- **Nginx**: リバースプロキシ (本番)

---

## 既存資産活用マップ

| Legacy資産 | 移行先 | 優先度 |
|-----------|-------|--------|
| phase1/common.py | backend/app/core/config.py | 高 |
| phase1/file_handler.py | backend/app/services/backup.py | 中 |
| phase2/case_number_server.py | backend/app/services/case_number.py | 高 |
| phase3/incremental_sync.py | backend/app/services/backup.py | 中 |
| phase4/integrate_data.py | backend/app/services/merge.py | 低 |
| master/*.xlsx | データベース移行 | 高 |

---

## 次のアクション
1. ✅ プロジェクト構造作成
2. ✅ 進捗管理ドキュメント作成
3. ⏭️ Phase 1-Day 1: バックエンド初期化開始

---

## 備考
- Legacy Excel版は `legacy_excel_system/` に保存済み
- 本開発計画は `Webアプリ開発計画.md` を参照
- Git履歴は継続（新しいタグ体系を使用）
- 開発完了後、Excelファイルからデータベースへの移行ツールを作成予定


