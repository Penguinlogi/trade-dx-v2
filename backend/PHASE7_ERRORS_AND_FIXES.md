# Phase 7: エラーと修正の記録

**記録期間**: 2025-11-27 ～ 2025-11-28
**最終更新**: 2025-11-28

## エラーと修正の一覧

### 1. バックエンドサーバー起動エラー

**発生日時**: 2025-11-28
**エラー内容**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**原因**:
- 仮想環境が正しくアクティベートされていない
- または、グローバルPythonを使用していた

**修正内容**:
- `backend/start_server.bat` を作成・改善
- 仮想環境のPythonを直接使用するように変更: `venv\Scripts\python.exe`
- 仮想環境の確認と自動作成機能を追加

**関連ファイル**:
- `backend/start_server.bat`

**状態**: ✅ 解決済み

---

### 2. フロントエンド起動エラー

**発生日時**: 2025-11-28
**エラー内容**:
```
npm error code ENOENT
npm error path .../package.json
```

**原因**:
- プロジェクトルートから `npm run dev` を実行していた
- `package.json` は `frontend` ディレクトリに存在

**修正内容**:
- `frontend/start_frontend.bat` を作成
- `start_all.bat` を作成（バックエンドとフロントエンドを同時起動）
- 手順書に正しいディレクトリを明記

**関連ファイル**:
- `frontend/start_frontend.bat`
- `start_all.bat`
- `README_START.md`

**状態**: ✅ 解決済み

---

### 3. Material-UIアイコンインポートエラー

**発生日時**: 2025-11-28
**エラー内容**:
```
Uncaught SyntaxError: The requested module does not provide an export named 'Cleanup'
```

**原因**:
- `@mui/icons-material` に `Cleanup` アイコンが存在しない

**修正内容**:
- `Cleanup` を `DeleteSweep` に変更
- 未使用の `CloudDownload` インポートを削除

**関連ファイル**:
- `frontend/src/pages/BackupsPage.tsx`

**状態**: ✅ 解決済み

---

### 4. React Router Future Flag警告

**発生日時**: 2025-11-28
**エラー内容**:
```
⚠️ React Router Future Flag Warning: v7_startTransition
⚠️ React Router Future Flag Warning: v7_relativeSplatPath
```

**原因**:
- React Router v7への移行準備のための警告

**修正内容**:
- `BrowserRouter` に `future` プロップを追加
- `v7_startTransition: true` と `v7_relativeSplatPath: true` を設定

**関連ファイル**:
- `frontend/src/App.tsx`

**状態**: ✅ 解決済み

---

### 5. 案件削除時に変更履歴も削除される問題

**発生日時**: 2025-11-28
**エラー内容**:
- 案件を削除すると、その変更履歴も削除されてしまう

**原因**:
- SQLAlchemyの `cascade="all, delete-orphan"` が設定されていた

**修正内容**:
- `Case` モデルの `change_histories` リレーションから `cascade` を削除
- `passive_deletes=True` を追加（SQLAlchemyに外部キーの処理を任せる）

**関連ファイル**:
- `backend/app/models/case.py`

**状態**: ✅ 解決済み

---

### 6. 案件削除失敗エラー（IntegrityError）

**発生日時**: 2025-11-28
**エラー内容**:
```
sqlite3.IntegrityError: NOT NULL constraint failed: change_history.case_id
```

**原因**:
- データベーススキーマで `case_id` が `NOT NULL` のまま
- SQLAlchemyが削除時に `case_id` を NULL に設定しようとしていた

**修正内容**:
- `case_id` を `nullable=False` のまま維持（既存DBとの互換性のため）
- `passive_deletes=True` でSQLAlchemyに外部キーの自動処理をさせない
- 削除前に変更履歴を記録し、別トランザクションでコミット
- `PRAGMA foreign_keys=ON` の設定をコメントアウト（既存DBとの互換性）

**関連ファイル**:
- `backend/app/models/case.py`
- `backend/app/models/change_history.py`
- `backend/app/api/endpoints/cases.py`
- `backend/app/core/database.py`

**状態**: ✅ 解決済み

---

### 7. UnicodeDecodeError（requirements.txt）

**発生日時**: 2025-11-28
**エラー内容**:
```
UnicodeDecodeError: 'cp932' codec can't decode byte 0x87
```

**原因**:
- `requirements.txt` が非UTF-8エンコーディングで保存されていた

**修正内容**:
- `requirements.txt` をUTF-8エンコーディングで再保存
- コメントを英語に変更（エンコーディング問題を回避）

**関連ファイル**:
- `backend/requirements.txt`

**状態**: ✅ 解決済み

---

### 8. 変更履歴のタイムスタンプがJSTで表示されない

**発生日時**: 2025-11-28
**エラー内容**:
- 変更履歴の変更日時がUTCで表示されていた

**修正内容**:
- `to_jst()` 関数を追加（UTCからJSTへの変換）
- `get_change_history()` と `get_change_history_detail()` でJST変換を適用

**関連ファイル**:
- `backend/app/api/endpoints/change_history.py`

**状態**: ✅ 解決済み

---

### 9. 新規作成・更新が変更履歴に反映されない

**発生日時**: 2025-11-28
**エラー内容**:
- 新規案件作成・更新時に変更履歴が記録されない
- 過去の案件番号が新しい案件で上書きされる

**修正内容**:
- `record_change_history()` で `case_number_snapshot` を保存
- `db.flush()` を `db.commit()` に変更（明示的なコミット）
- 各CRUD操作後に変更履歴を明示的にコミット
- `Case` モデルに `sqlite_autoincrement=True` を追加（ID再利用防止）
- 既存データ補正スクリプトを作成

**関連ファイル**:
- `backend/app/services/change_history_service.py`
- `backend/app/api/endpoints/cases.py`
- `backend/app/models/case.py`
- `backend/scripts/fix_change_history_case_number_snapshot.py`

**状態**: ✅ 解決済み

---

### 10. 削除履歴が反映されない

**発生日時**: 2025-11-28
**エラー内容**:
- 削除履歴が記録されない

**修正内容**:
- 削除履歴記録のログレベルを `warning` から `error` に変更
- 成功ログの改善
- 削除前の重複チェック追加

**関連ファイル**:
- `backend/app/api/endpoints/cases.py`

**状態**: ✅ 解決済み

---

### 11. 変更履歴画面の案件番号検索・ソート

**発生日時**: 2025-11-28
**要望内容**:
- 案件IDではなく案件番号で検索・ソートしたい
- 完全一致ではなく部分一致にしたい

**修正内容**:
- バックエンドAPIに `case_number` パラメータを追加（部分一致検索）
- ソート項目に「案件番号」を追加
- Python側でフィルタリング・ソート処理を実装

**関連ファイル**:
- `backend/app/api/endpoints/change_history.py`
- `frontend/src/pages/ChangeHistoryPage.tsx`
- `frontend/src/types/changeHistory.ts`

**状態**: ✅ 解決済み

---

### 12. _case_number_snapshotフィールドが表示される

**発生日時**: 2025-11-28
**要望内容**:
- 変更履歴の詳細表示で `_case_number_snapshot` フィールドが表示されてしまう

**修正内容**:
- `changes_json` の表示時に `_case_number_snapshot` フィールドを除外
- 表示用データのみを抽出するフィルタリング処理を追加

**関連ファイル**:
- `frontend/src/pages/ChangeHistoryPage.tsx`

**状態**: ✅ 解決済み

---

### 13. バックアップ復元後にステータスが更新されない

**発生日時**: 2025-11-28
**エラー内容**:
- バックアップ復元後、ステータスが「実行中」のまま変化しない

**修正内容**:
- 復元処理開始時にステータスを `"in_progress"` に更新
- 復元完了時にステータスを `"success"` に更新
- エラー時は `"failed"` に更新

**関連ファイル**:
- `backend/app/services/backup_service.py`

**状態**: ✅ 解決済み

---

### 14. バックアップの作成日時がJSTで表示されない

**発生日時**: 2025-11-28
**エラー内容**:
- バックアップ一覧の作成日時がUTCで表示されていた

**修正内容**:
- `to_jst()` 関数を追加（変更履歴と同様）
- `get_backups()` と `get_backup()` で作成日時をJSTに変換

**関連ファイル**:
- `backend/app/api/endpoints/backups.py`

**状態**: ✅ 解決済み

---

### 15. スケジュールバックアップAPIで「Not authenticated」エラー

**発生日時**: 2025-11-28
**エラー内容**:
- ブラウザで直接アクセスすると「Not authenticated」エラー

**説明**:
- これは正常な動作（認証が必要なAPI）

**修正内容**:
- 手順書に正しい実行方法を追加
  - 方法1: FastAPI Swagger UI を使用（推奨）
  - 方法2: ブラウザの開発者ツールから実行
  - 方法3: curlコマンドで実行
- トラブルシューティングセクションに説明を追加

**関連ファイル**:
- `進捗管理/フェーズ進捗メモ/Phase7_手動操作手順書.md`

**状態**: ✅ 解決済み（手順書改善）

---

## まとめ

### エラー・修正の統計
- **総エラー数**: 15件
- **解決済み**: 15件
- **未解決**: 0件

### 主な修正カテゴリ
1. **環境構築・起動関連**: 3件
2. **UI・表示関連**: 4件
3. **データベース・データ整合性**: 5件
4. **日時表示**: 2件
5. **ドキュメント**: 1件

### 重要な学習ポイント
1. SQLAlchemyの `cascade` と `passive_deletes` の使い分け
2. 変更履歴の永続化には `passive_deletes=True` が重要
3. 案件番号スナップショットによる履歴の正確性確保
4. 日本標準時変換の一貫した実装
5. バックアップ復元時のステータス管理

---

**最終更新**: 2025-11-28
**記録者**: 開発チーム
**Phase 7状態**: ✅ 完了・実行確認完了






