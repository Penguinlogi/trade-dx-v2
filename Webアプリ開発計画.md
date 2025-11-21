# 貿易DX V2.1 - Webアプリケーション開発計画

## プロジェクト概要
ExcelベースからWebアプリケーションへの完全移行

## 技術スタック

### フロントエンド
- **フレームワーク**: React 18 (Vite)
- **UI コンポーネント**: Material-UI (MUI) / Ant Design
- **状態管理**: React Query + Context API
- **テーブル**: TanStack Table (React Table v8)
- **フォーム**: React Hook Form + Zod
- **HTTP クライアント**: Axios
- **言語**: TypeScript

### バックエンド
- **フレームワーク**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **バリデーション**: Pydantic V2
- **認証**: JWT (python-jose)
- **データベース**: PostgreSQL 15+ / SQLite (開発用)
- **非同期処理**: asyncio
- **API ドキュメント**: OpenAPI (Swagger UI)

### インフラ・DevOps
- **開発環境**: Docker Compose
- **本番環境**: Docker / Cloud (オプション)
- **リバースプロキシ**: Nginx (オプション)
- **環境変数管理**: python-dotenv

### 既存資産の活用
- Phase 1-4のPythonロジックをバックエンドに統合
- config.json → データベース設定
- 案件番号生成ロジック → APIエンドポイント化
- ファイル同期ロジック → バックアップ機能として活用

---

## 開発フェーズ（全20日間 = 4週間）

### Phase 1: 環境構築とデータベース設計 (3日)

#### Day 1: プロジェクト初期化
- [ ] ディレクトリ構造の作成
- [ ] バックエンド初期化
  - [ ] FastAPI プロジェクト作成
  - [ ] requirements.txt 作成
  - [ ] main.py 作成
  - [ ] config.py 作成
- [ ] フロントエンド初期化
  - [ ] React + Vite プロジェクト作成
  - [ ] package.json 設定
  - [ ] TypeScript 設定
  - [ ] ESLint/Prettier 設定
- [ ] Docker環境構築
  - [ ] docker-compose.yml 作成
  - [ ] Dockerfile (backend)
  - [ ] Dockerfile (frontend)

#### Day 2: データベース設計
- [ ] ER図の作成
- [ ] テーブル定義
  - [ ] users (ユーザー)
  - [ ] customers (顧客マスタ)
  - [ ] products (商品マスタ)
  - [ ] cases (案件)
  - [ ] change_history (変更履歴)
  - [ ] case_numbers (案件番号管理)
  - [ ] backups (バックアップ履歴)
- [ ] SQLAlchemy モデル作成
- [ ] Alembic マイグレーション設定

#### Day 3: データベース実装とマイグレーション
- [ ] 初期マイグレーションファイル作成
- [ ] マイグレーション実行
- [ ] シードデータ作成
- [ ] テストデータ投入スクリプト

---

### Phase 2: 認証機能 (2日)

#### Day 1: バックエンド認証
- [ ] JWT認証の実装
  - [ ] auth/jwt.py 作成
  - [ ] パスワードハッシュ化 (bcrypt)
  - [ ] トークン生成・検証
- [ ] 認証エンドポイント
  - [ ] POST /api/auth/login
  - [ ] POST /api/auth/logout
  - [ ] GET /api/auth/me
  - [ ] POST /api/auth/refresh
- [ ] 認証ミドルウェア

#### Day 2: フロントエンド認証
- [ ] ログイン画面の作成
- [ ] AuthContext 作成
- [ ] Private Route 作成
- [ ] トークンストレージ (localStorage/sessionStorage)
- [ ] 自動ログアウト機能
- [ ] 認証状態の管理

---

### Phase 3: 案件管理API (4日)

#### Day 1: 案件CRUD - バックエンド
- [ ] 案件モデルの実装
- [ ] 案件APIエンドポイント
  - [ ] GET /api/cases (一覧取得)
  - [ ] GET /api/cases/{id} (詳細取得)
  - [ ] POST /api/cases (新規作成)
  - [ ] PUT /api/cases/{id} (更新)
  - [ ] DELETE /api/cases/{id} (削除)
- [ ] フィルタリング機能
  - [ ] 区分（輸出/輸入/中継/国内）
  - [ ] ステータス（受注/見積/船積/完了）
  - [ ] 日付範囲
- [ ] 検索機能
  - [ ] 案件番号
  - [ ] 顧客名
  - [ ] 商品名

#### Day 2: 案件CRUD - フロントエンド
- [ ] 案件一覧画面
  - [ ] データテーブルコンポーネント
  - [ ] ページネーション
  - [ ] ソート機能
  - [ ] フィルター機能
  - [ ] 検索フォーム
- [ ] API連携
  - [ ] React Query セットアップ
  - [ ] useCases フック作成

#### Day 3: 案件フォーム
- [ ] 新規案件作成モーダル
- [ ] 案件編集モーダル
- [ ] フォームバリデーション
- [ ] エラーハンドリング
- [ ] 確認ダイアログ
- [ ] 成功/エラートースト

#### Day 4: 案件番号自動生成
- [ ] Phase 2の案件番号ロジック移植
- [ ] POST /api/case-numbers/generate
- [ ] 案件種別ごとの採番
- [ ] 連番管理テーブル
- [ ] トランザクション制御

---

### Phase 4: マスタ管理 (3日)

#### Day 1: 顧客マスタ
- [ ] 顧客マスタAPIエンドポイント
  - [ ] GET /api/customers
  - [ ] POST /api/customers
  - [ ] PUT /api/customers/{id}
  - [ ] DELETE /api/customers/{id}
- [ ] 顧客マスタ画面
  - [ ] 一覧表示
  - [ ] 登録・編集フォーム
  - [ ] 検索・フィルター

#### Day 2: 商品マスタ
- [ ] 商品マスタAPIエンドポイント
  - [ ] GET /api/products
  - [ ] POST /api/products
  - [ ] PUT /api/products/{id}
  - [ ] DELETE /api/products/{id}
- [ ] 商品マスタ画面
  - [ ] 一覧表示
  - [ ] 登録・編集フォーム
  - [ ] 検索・フィルター

#### Day 3: マスタ連携
- [ ] 案件フォームでの顧客選択
- [ ] 案件フォームでの商品選択
- [ ] オートコンプリート機能
- [ ] マスタデータのキャッシュ

---

### Phase 5: ダッシュボード・集計機能 (2日)

#### Day 1: 集計API
- [ ] GET /api/analytics/summary (サマリー取得)
  - [ ] 総売上
  - [ ] 総粗利
  - [ ] 平均粗利率
  - [ ] 案件数（ステータス別）
- [ ] GET /api/analytics/trends (トレンド取得)
- [ ] GET /api/analytics/by-customer (顧客別集計)

#### Day 2: ダッシュボード画面
- [ ] サマリーカード
  - [ ] 総売上
  - [ ] 総粗利
  - [ ] 平均粗利率
- [ ] 案件ステータス分布
- [ ] 月次トレンドグラフ
- [ ] 顧客別売上TOP10

---

### Phase 6: ドキュメント生成機能 (3日)

#### Day 1: Invoice生成
- [ ] POST /api/documents/invoice
- [ ] Excelテンプレート管理
- [ ] openpyxl によるExcel生成
- [ ] PDFエクスポート (オプション)

#### Day 2: Packing List生成
- [ ] POST /api/documents/packing-list
- [ ] テンプレート管理
- [ ] ドキュメント履歴管理

#### Day 3: フロントエンド統合
- [ ] ドキュメント生成ボタン
- [ ] プレビュー機能
- [ ] ダウンロード機能
- [ ] 生成履歴表示

---

### Phase 7: 変更履歴・バックアップ (2日)

#### Day 1: 変更履歴機能
- [ ] 変更履歴記録ミドルウェア
- [ ] GET /api/change-history
- [ ] 変更履歴画面
- [ ] 差分表示機能

#### Day 2: バックアップ機能
- [ ] POST /api/backups/create
- [ ] GET /api/backups
- [ ] バックアップ自動作成（スケジューラ）
- [ ] Phase 3のバックアップロジック移植
- [ ] バックアップからの復元機能

---

### Phase 8: リアルタイム同期・通知 (1日)

- [ ] WebSocket セットアップ
- [ ] リアルタイム更新通知
- [ ] サーバー状態表示
- [ ] 最終同期時刻表示
- [ ] オンラインユーザー表示

---

### Phase 9: テストとデバッグ (2日)

#### Day 1: バックエンドテスト
- [ ] pytest セットアップ
- [ ] API単体テスト
- [ ] 統合テスト
- [ ] カバレッジレポート

#### Day 2: フロントエンドテスト
- [ ] Vitest セットアップ
- [ ] コンポーネントテスト
- [ ] E2Eテスト (Playwright)
- [ ] エラーハンドリング確認

---

## ディレクトリ構造

```
貿易DX/
├── backend/
│   ├── alembic/              # DBマイグレーション
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/    # APIエンドポイント
│   │   │   │   ├── auth.py
│   │   │   │   ├── cases.py
│   │   │   │   ├── customers.py
│   │   │   │   ├── products.py
│   │   │   │   ├── documents.py
│   │   │   │   └── analytics.py
│   │   │   └── deps.py       # 依存性注入
│   │   ├── core/
│   │   │   ├── config.py     # 設定
│   │   │   ├── security.py   # セキュリティ
│   │   │   └── database.py   # DB接続
│   │   ├── models/           # SQLAlchemyモデル
│   │   │   ├── user.py
│   │   │   ├── case.py
│   │   │   ├── customer.py
│   │   │   └── product.py
│   │   ├── schemas/          # Pydanticスキーマ
│   │   │   ├── user.py
│   │   │   ├── case.py
│   │   │   └── token.py
│   │   ├── services/         # ビジネスロジック
│   │   │   ├── case_number.py  # Phase 2移植
│   │   │   ├── backup.py       # Phase 3移植
│   │   │   └── document.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/              # API クライアント
│   │   ├── components/       # 共通コンポーネント
│   │   │   ├── Layout/
│   │   │   ├── Table/
│   │   │   ├── Form/
│   │   │   └── Modal/
│   │   ├── pages/            # ページ
│   │   │   ├── Login/
│   │   │   ├── Cases/
│   │   │   ├── Customers/
│   │   │   ├── Products/
│   │   │   └── Settings/
│   │   ├── hooks/            # カスタムフック
│   │   ├── context/          # Context
│   │   ├── types/            # TypeScript型定義
│   │   ├── utils/            # ユーティリティ
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── Webアプリ開発計画.md (このファイル)
```

---

## 既存資産の移行マップ

| 既存資産 | 移行先 | 備考 |
|---------|-------|------|
| scripts/phase1/common.py | backend/app/core/config.py | 設定管理 |
| scripts/phase1/file_handler.py | backend/app/services/backup.py | バックアップ機能 |
| scripts/phase2/case_number_server.py | backend/app/services/case_number.py | 案件番号生成ロジック |
| scripts/phase3/incremental_sync.py | backend/app/services/backup.py | バックアップ機能として統合 |
| scripts/phase4/integrate_data.py | backend/app/services/merge.py | 競合解決ロジック |
| master/案件管理台帳_マスター.xlsx | PostgreSQL データベース | データ移行 |

---

## 開発環境セットアップ手順

### 必要なソフトウェア
- Python 3.11+
- Node.js 18+
- Docker Desktop (推奨)
- PostgreSQL 15+ (Dockerなしの場合)
- Git

### セットアップコマンド
```bash
# 1. バックエンド
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. フロントエンド
cd frontend
npm install

# 3. Docker (推奨)
docker-compose up -d
```

---

## マイルストーン

- **Week 1 (Day 1-5)**: Phase 1-2 完了（環境構築、認証）
- **Week 2 (Day 6-10)**: Phase 3-4 完了（案件管理、マスタ管理）
- **Week 3 (Day 11-15)**: Phase 5-7 完了（集計、ドキュメント、履歴）
- **Week 4 (Day 16-20)**: Phase 8-9 完了（リアルタイム、テスト）

---

## 次のアクション

1. ✅ この計画書の確認と承認
2. Phase 1-Day 1: プロジェクト初期化の開始
3. 既存Excelデータの移行準備

---

## 注意事項

- 既存のPhase 0-4のコードは`scripts/legacy/`に移動して保管
- Excelファイルはデータベース移行まで保持
- 移行期間中の並行運用は検討可能
- 本番環境への展開は別途計画


