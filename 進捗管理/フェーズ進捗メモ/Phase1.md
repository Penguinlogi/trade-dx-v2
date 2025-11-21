# Phase 1: 環境構築とデータベース設計 - 進捗メモ

## 開始日: 2025-11-21
## 予定完了日: 2025-11-24 (3日)

---

## Day 1: プロジェクト初期化 (2025-11-21)

### 作業ログ

#### 10:00 - ディレクトリ構造作成
- ✅ 既存プログラムを`legacy/`フォルダに移動完了
- ✅ 新規プロジェクトのディレクトリ構造作成完了
  - backend/app/(api, core, models, schemas, services)
  - frontend/src/(api, components, pages, hooks, context, types, utils)
  - 進捗管理/(フェーズ進捗メモ, エラーと解消方法)

#### 進行中の作業
- バックエンド初期化
- フロントエンド初期化
- Docker環境構築

### 成果物
- [x] ディレクトリ構造
- [ ] requirements.txt
- [ ] package.json
- [ ] docker-compose.yml
- [ ] README.md

---

## Day 2: データベース設計 (予定)

### 予定作業
- ER図の作成
- テーブル定義
- SQLAlchemyモデル作成
- Alembicマイグレーション設定

---

## Day 3: データベース実装とマイグレーション (予定)

### 予定作業
- 初期マイグレーション実行
- シードデータ作成
- テストデータ投入

---

## メモ
- 既存のPhase 0-4のコードは無駄にならず、バックエンドのサービス層で再利用予定
- 案件番号生成ロジック: legacy/scripts/phase2/case_number_server.py → backend/app/services/case_number.py
- バックアップロジック: legacy/scripts/phase3/ → backend/app/services/backup.py


