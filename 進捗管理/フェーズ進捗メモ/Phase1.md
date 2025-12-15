# Phase 1: 環境構築とデータベース設計 - 進捗メモ

## 完了日
2025-11-21

## 実施内容

### 1. プロジェクト初期化（Day 1）
- ✅ ディレクトリ構造の作成
- ✅ バックエンド初期化
  - FastAPIプロジェクト作成
  - requirements.txt作成（Pydantic 2.10.0, FastAPI 0.115.0使用）
  - main.py、config.py、database.py作成
- ✅ フロントエンド初期化
  - React + Vite プロジェクト設定
  - TypeScript設定（tsconfig.json）
  - package.json設定
- ✅ Docker環境構築
  - docker-compose.yml作成（PostgreSQL、Backend、Frontend）
  - Dockerfileの作成（backend, frontend）

### 2. データベース設計（Day 2）
- ✅ SQLAlchemyモデル作成
  - `models/user.py`: ユーザー認証用テーブル
  - `models/customer.py`: 顧客マスタ
  - `models/product.py`: 商品マスタ
  - `models/case.py`: 案件テーブル（リレーション、金額計算ロジック含む）
  - `models/change_history.py`: 変更履歴テーブル
  - `models/case_number.py`: 案件番号管理テーブル
  - `models/backup.py`: バックアップ履歴テーブル

- ✅ Alembicマイグレーション設定
  - alembic.ini作成
  - alembic/env.py設定
  - script.py.mako テンプレート作成

### 3. データベース実装（Day 3）
- ✅ 初期マイグレーションファイル作成
  - `alembic/versions/001_initial_migration.py`: すべてのテーブル定義
  
- ✅ シードデータスクリプト作成
  - `scripts/seed_data.py`: 初期ユーザー、顧客マスタ、商品マスタ、案件番号管理
  - `scripts/test_data.py`: テスト用案件データ
  - `scripts/run_seed.bat` / `run_seed.sh`: 一括実行スクリプト

## 技術的な決定事項

### 依存関係の調整
- **問題**: psycopg2-binaryとpydantic-coreのコンパイルエラー
- **解決策**:
  - PostgreSQLドライバー（psycopg2-binary）を開発環境ではコメントアウト
  - PydanticとFastAPIをより新しいバージョンに更新
    - pydantic: 2.5.0 → 2.10.0
    - pydantic-settings: 2.1.0 → 2.6.0
    - fastapi: 0.104.1 → 0.115.0
    - uvicorn: 0.24.0 → 0.32.0

### データベース設計の特徴
1. **SQLiteを開発環境で使用**: PostgreSQLは本番環境用
2. **リレーション**: Customer ← Case → Product の多対多
3. **金額自動計算**: Case.calculate_amounts()メソッドで売上額、粗利額、粗利率を計算
4. **変更履歴**: JSON形式で変更詳細を保存可能
5. **案件番号**: 年度・区分別の連番管理（例: 2025-EX-001）

## 次のステップ（Phase 2）
- JWT認証の実装
- ログイン画面の作成
- 認証状態管理

## 注意事項
- 本番環境でPostgreSQLを使用する場合は、requirements.txtのpsycopg2-binaryのコメントを外す必要があります
- マイグレーション実行前に、Pythonの依存関係が正しくインストールされていることを確認してください

## 成果物リスト
1. **バックエンド**
   - SQLAlchemyモデル（7テーブル）
   - Alembicマイグレーション設定
   - 初期マイグレーションファイル
   - シードデータスクリプト
   
2. **フロントエンド**
   - React + Vite + TypeScript基本設定
   - MUI（Material-UI）依存関係
   
3. **インフラ**
   - Docker Compose設定
   - Dockerfile（backend, frontend）
   
4. **ドキュメント**
   - 進捗管理書の更新
   - 手動操作手順書（別ファイル）
