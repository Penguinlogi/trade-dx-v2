# 貿易DX管理システム V2.1 - Webアプリケーション版

貿易業務を効率化するための統合管理システム（Webアプリ版）

## 🎯 プロジェクト概要

ExcelベースのシステムからWebアプリケーションへの完全移行プロジェクト

### 主な機能

- 📦 案件管理（輸出/輸入/中継/国内）
- 👥 顧客マスタ管理
- 📦 商品マスタ管理
- 📊 ダッシュボード・集計機能
- 📄 ドキュメント生成（Invoice、Packing List）
- 🔒 ユーザー認証・権限管理
- 📝 変更履歴・監査ログ
- 💾 自動バックアップ

## 🏗️ 技術スタック

### フロントエンド
- **React** 18.2 + TypeScript
- **Vite** 5.0
- **Material-UI (MUI)** 5.14
- **React Query** 5.8
- **React Hook Form** + Zod
- **TanStack Table** 8.10

### バックエンド
- **FastAPI** 0.104 (Python 3.11+)
- **SQLAlchemy** 2.0
- **PostgreSQL** 15+ / SQLite (開発用)
- **JWT認証**
- **Pydantic V2**

### インフラ
- **Docker** + Docker Compose
- **Nginx** (オプション)

## 📁 プロジェクト構造

```
貿易DX/
├── backend/              # FastAPI バックエンド
│   ├── app/
│   │   ├── api/          # APIエンドポイント
│   │   ├── core/         # コア機能（設定、DB、セキュリティ）
│   │   ├── models/       # SQLAlchemyモデル
│   │   ├── schemas/      # Pydanticスキーマ
│   │   ├── services/     # ビジネスロジック
│   │   └── main.py       # メインアプリケーション
│   ├── tests/            # テスト
│   ├── requirements.txt  # Python依存関係
│   └── Dockerfile
│
├── frontend/             # React フロントエンド
│   ├── src/
│   │   ├── api/          # APIクライアント
│   │   ├── components/   # UIコンポーネント
│   │   ├── pages/        # ページ
│   │   ├── hooks/        # カスタムフック
│   │   ├── context/      # コンテキスト
│   │   └── types/        # 型定義
│   ├── package.json      # Node依存関係
│   └── Dockerfile
│
├── legacy/               # 既存のExcelベースシステム（保管用）
├── 進捗管理/              # プロジェクト進捗管理
│   ├── 全体進捗管理書.md
│   ├── フェーズ進捗メモ/
│   └── エラーと解消方法/
├── docker-compose.yml    # Docker構成
├── Webアプリ開発計画.md   # 詳細開発計画
└── README.md             # このファイル
```

## 🚀 クイックスタート

### 前提条件

- Python 3.11+
- Node.js 18+
- Docker Desktop（推奨）

### Docker を使用する場合（推奨）

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd 貿易DX

# 2. Docker Compose でサービスを起動
docker-compose up -d

# 3. ブラウザでアクセス
# フロントエンド: http://localhost:3000
# バックエンドAPI: http://localhost:8000
# API ドキュメント: http://localhost:8000/docs
```

### Docker を使用しない場合

#### バックエンド

```bash
cd backend

# 仮想環境の作成と有効化
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 依存関係のインストール
pip install -r requirements.txt

# サーバーの起動
uvicorn app.main:app --reload
```

#### フロントエンド

```bash
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

## 📚 ドキュメント

- [Webアプリ開発計画](./Webアプリ開発計画.md) - 詳細な開発計画（20日間）
- [全体進捗管理書](./進捗管理/全体進捗管理書.md) - プロジェクト進捗状況
- [バックエンドREADME](./backend/README.md) - バックエンド詳細
- [フロントエンドREADME](./frontend/README.md) - フロントエンド詳細

## 🗓️ 開発スケジュール

| Week | フェーズ | 内容 |
|------|---------|------|
| Week 1 | Phase 1-2 | 環境構築、データベース設計、認証機能 |
| Week 2 | Phase 3-4 | 案件管理API、マスタ管理 |
| Week 3 | Phase 5-7 | ダッシュボード、ドキュメント生成、履歴管理 |
| Week 4 | Phase 8-9 | リアルタイム機能、テスト |

**開始日**: 2025-11-21  
**予定完了日**: 2025-12-20

## 📝 開発状況

- ✅ Phase 0: プロジェクト初期化完了（2025-11-21）
- 🔄 Phase 1: 環境構築中
- ⬜ Phase 2-9: 未着手

詳細は [全体進捗管理書](./進捗管理/全体進捗管理書.md) を参照

## 🔧 開発ツール

### コードフォーマット

```bash
# バックエンド
cd backend
black app/
flake8 app/

# フロントエンド
cd frontend
npm run lint
```

### テスト

```bash
# バックエンド
cd backend
pytest

# フロントエンド
cd frontend
npm test
```

## 🌐 API ドキュメント

サーバー起動後、以下のURLでAPIドキュメントにアクセス可能：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📦 既存資産の活用

以下の既存ロジックをWebアプリに移植予定：

| 既存資産 | 移行先 |
|---------|-------|
| 案件番号生成ロジック | backend/app/services/case_number.py |
| バックアップロジック | backend/app/services/backup.py |
| 競合解決ロジック | backend/app/services/merge.py |
| 設定管理 | backend/app/core/config.py |

既存のExcelベースシステムは `legacy/` フォルダに保管済み

## 🔐 セキュリティ

- JWT認証によるユーザー認証
- パスワードのbcryptハッシュ化
- CORS設定
- 環境変数による機密情報管理

## 🤝 貢献

プロジェクトへの貢献を歓迎します！

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 ライセンス

社内プロジェクト - ペンギンロジスティクス株式会社

## 👥 プロジェクトチーム

- **プロジェクトオーナー**: AI事業部門
- **開発**: AI事業部門 + AI Assistant
- **期間**: 2025-11-21 ~ 2025-12-20

## 📞 サポート

問題や質問がある場合は、以下を参照：

1. [エラーと解消方法](./進捗管理/エラーと解消方法/) - 既知の問題と解決策
2. [フェーズ進捗メモ](./進捗管理/フェーズ進捗メモ/) - 各フェーズの詳細記録
3. プロジェクトチームへの問い合わせ

---

**プロジェクト開始日**: 2025-11-21  
**最終更新**: 2025-11-21  
**バージョン**: 2.1.0

