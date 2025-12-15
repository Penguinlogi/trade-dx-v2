# 貿易DX管理システム V2.1 Webアプリケーション版

## プロジェクト概要
貿易業務（輸出入案件管理）を効率化するためのWebアプリケーションシステムです。
既存のExcelベースシステムをWebアプリケーション化し、複数ユーザーでの同時利用、リアルタイム同期、データの一元管理を実現します。

## 技術スタック

### フロントエンド
- React 18 + TypeScript
- Vite
- Material-UI (MUI)
- React Query
- React Hook Form + Zod
- Axios

### バックエンド
- FastAPI (Python 3.11+)
- SQLAlchemy 2.0
- PostgreSQL 15+ / SQLite (開発用)
- Pydantic V2
- JWT認証
- Alembic (マイグレーション)

### インフラ
- Docker Compose
- Nginx (オプション)

## プロジェクト構造

```
貿易DX/
├── backend/                    # バックエンドAPI
│   ├── app/
│   │   ├── api/               # APIエンドポイント
│   │   ├── core/              # 設定、データベース接続
│   │   ├── models/            # SQLAlchemyモデル
│   │   ├── schemas/           # Pydanticスキーマ
│   │   ├── services/          # ビジネスロジック
│   │   └── main.py           # FastAPIアプリケーション
│   ├── alembic/              # マイグレーション
│   ├── scripts/              # データベーススクリプト
│   ├── tests/                # テストコード
│   ├── requirements.txt      # Python依存関係
│   └── Dockerfile
│
├── frontend/                  # フロントエンドUI
│   ├── src/
│   │   ├── api/              # APIクライアント
│   │   ├── components/       # Reactコンポーネント
│   │   ├── context/          # Contextプロバイダー
│   │   ├── hooks/            # カスタムフック
│   │   ├── pages/            # ページコンポーネント
│   │   ├── types/            # TypeScript型定義
│   │   └── utils/            # ユーティリティ関数
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml        # Docker Compose設定
├── README.md
└── 進捗管理/                  # プロジェクト進捗管理
```

## セットアップ手順

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd 貿易DX
```

### 2. バックエンドのセットアップ

#### 依存関係のインストール
```bash
cd backend
pip install -r requirements.txt
```

#### データベースの初期化
```bash
# シードデータ（マスタデータ）の投入
python scripts/seed_data.py

# テストデータの投入（オプション）
python scripts/test_data.py
```

または、一括実行スクリプトを使用：
```bash
# Windowsの場合
scripts\run_seed.bat

# macOS/Linuxの場合
chmod +x scripts/run_seed.sh
./scripts/run_seed.sh
```

#### サーバーの起動

**⚠️ 重要:** フロントエンドより先にバックエンドを起動してください！

```bash
# Windowsの場合
py -3 -m uvicorn app.main:app --reload

# macOS/Linuxの場合
uvicorn app.main:app --reload
```

サーバーが起動したら、以下のURLでアクセスできます：
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. フロントエンドのセットアップ

**⚠️ 重要:** バックエンドを起動してからフロントエンドを起動してください！

**新しいターミナルを開いて：**

```bash
cd frontend
npm install
npm run dev
```

フロントエンドは **http://localhost:3000** で起動します（5173ではありません）。

### 4. Dockerを使用する場合

```bash
docker-compose up --build
```

以下のサービスが起動します：
- PostgreSQL: localhost:5432
- Backend API: localhost:8000
- Frontend: localhost:3000

## データベーススキーマ

### 主要テーブル
- **users**: ユーザー認証情報
- **customers**: 顧客マスタ
- **products**: 商品マスタ
- **cases**: 案件データ（輸出入案件）
- **change_history**: 変更履歴
- **case_numbers**: 案件番号管理（自動採番）
- **backups**: バックアップ履歴

詳細は `backend/app/models/` のモデル定義を参照してください。

## 初期ユーザー（開発環境）

シードデータで以下のユーザーが作成されます：

| ユーザー名 | パスワード | 権限 | 氏名 |
|----------|---------|------|------|
| admin | admin123 | 管理者 | 管理者 |
| yamada | yamada123 | 一般 | 山田太郎 |
| suzuki | suzuki123 | 一般 | 鈴木花子 |

## 開発進捗

### Phase 1: 環境構築とデータベース設計 ✅ 完了
- [x] プロジェクト初期化
- [x] バックエンド環境構築
- [x] フロントエンド環境構築
- [x] Docker環境構築
- [x] データベース設計とモデル作成
- [x] マイグレーション設定
- [x] シードデータ・テストデータスクリプト

### Phase 2: 認証機能 ✅ 完了
- [x] JWT認証の実装
- [x] ログイン画面の作成
- [x] 認証状態管理

### Phase 3: 案件管理API ✅ 完了
- [x] 案件CRUD API
- [x] 案件一覧画面
- [x] 案件登録・編集フォーム
- [x] 案件番号自動生成機能
- [x] 検索・フィルター機能

### Phase 4: マスタ管理 ✅ 完了
- [x] 顧客マスタ管理
- [x] 商品マスタ管理
- [x] マスタ連携機能

### Phase 5: ダッシュボード・集計機能 ✅ 完了
- [x] 集計API
- [x] ダッシュボード画面
- [x] 統計グラフ表示

### Phase 6: ドキュメント生成機能 ✅ 完了
- [x] Invoice生成
- [x] Packing List生成
- [x] ドキュメント履歴管理

### Phase 7: 変更履歴・バックアップ ✅ 完了
- [x] 変更履歴記録・表示
- [x] バックアップ・復元機能

### Phase 8: リアルタイム同期・通知 ✅ 完了
- [x] WebSocket通信
- [x] リアルタイム更新機能

### Phase 9: テストとデバッグ ✅ 完了
- [x] バックエンドテスト（65テスト、78%カバレッジ）
- [x] フロントエンドテスト（Vitest、E2E）
- [x] テストカバレッジレポート

**🎉 全フェーズ完了！システム開発は100%完了しました。**

詳細は `進捗管理/全体進捗管理書.md` を参照してください。

## ドキュメント

### 🚀 開発者向け
- [🚀 クイックスタートガイド](QUICKSTART.md) ← **最初にこれを読む！**
- [全体進捗管理書](進捗管理/全体進捗管理書.md)
- [Phase 1 手動操作手順書](進捗管理/フェーズ進捗メモ/Phase1_手動操作手順書.md)
- [Phase 2 手動操作手順書](進捗管理/フェーズ進捗メモ/Phase2_手動操作手順書.md)
- [Phase 3 手動操作手順書](進捗管理/フェーズ進捗メモ/Phase3_手動操作手順書.md)
- [Phase 9 手動操作手順書](進捗管理/フェーズ進捗メモ/Phase9_手動操作手順書.md)

### 📋 本番運用向け
- [📘 本番運用開始ガイド](docs/本番運用開始ガイド.md) ← **本番環境への展開前に必読！**
- [👥 ユーザーマニュアル（簡易版）](docs/ユーザーマニュアル_簡易版.md) ← **ユーザー向け**
- [Webアプリ開発計画](Webアプリ開発計画.md)

## 🚀 クイックスタート（最速で起動）

詳細な手順は `QUICKSTART.md` を参照してください。

```batch
# 1. シードデータ投入（初回のみ）
cd backend
scripts\run_seed_simple.bat

# 2. バックエンド起動（ターミナル1）
cd backend
py -3 -m uvicorn app.main:app --reload

# 3. フロントエンド起動（ターミナル2 - 新しいターミナルを開く）
cd frontend
npm run dev

# 4. ブラウザで http://localhost:3000 にアクセス
# ログイン: admin / admin123
```

## トラブルシューティング

### 問題: フロントエンドが真っ白（最も多い問題）

**原因:** バックエンドが起動していない

**解決策:**
1. バックエンドを先に起動する
2. http://localhost:8000/health にアクセスして確認
3. フロントエンドをリロード（F5）

### 問題: バッチファイルが文字化け

**解決策:** シンプル版を使用
```batch
cd backend
scripts\run_seed_simple.bat
```

### 問題: ポート番号が違う

- **フロントエンド:** 3000番ポート（5173ではない）
- **バックエンド:** 8000番ポート

`vite.config.ts` でポートが3000に設定されています。

### 問題: Pythonモジュールが見つからない
```bash
cd backend
pip install -r requirements.txt
```

### 問題: データベースの初期化に失敗する
既存のデータベースファイルを削除して再実行：
```bash
cd backend
del trade_dx.db  # Windowsの場合
# rm trade_dx.db  # macOS/Linuxの場合
py -3 -m scripts.seed_data
```

### 問題: Dockerコンテナが起動しない
```bash
docker-compose down -v
docker-compose up --build
```

## ライセンス
本プロジェクトはペンギンロジスティクス株式会社の内部プロジェクトです。

## 問い合わせ
開発チーム: AI事業部門

---

**最終更新**: 2025-12-01
**バージョン**: V2.1 Web
**ステータス**: ✅ 開発完了 (100% - 9/9 フェーズ完了)

## 🎯 次のステップ

システム開発は完了しました。本番環境での運用を開始するには、以下のガイドを参照してください：

1. **[本番運用開始ガイド](docs/本番運用開始ガイド.md)** - 本番環境への展開手順、データ移行、運用体制の構築方法
2. **[ユーザーマニュアル](docs/ユーザーマニュアル_簡易版.md)** - エンドユーザー向けの操作マニュアル

### 主な作業項目
- [ ] 本番サーバーのセットアップ
- [ ] セキュリティ設定（パスワード、HTTPS等）
- [ ] データ移行（既存Excelデータからの移行）
- [ ] バックアップ戦略の確立
- [ ] ユーザー教育の実施
- [ ] 運用体制の構築
