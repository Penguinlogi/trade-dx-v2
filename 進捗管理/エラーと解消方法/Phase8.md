# Phase 8: リアルタイム同期・通知 - エラーと解消方法

## 記録日: 2025-11-29

---

## エラー記録

### なし

---

## 解消済みエラー

### エラー1: `ModuleNotFoundError: No module named 'fastapi'` (2025-11-29)

**症状**: バックエンドサーバー起動時にエラーが発生

**原因**: 仮想環境がアクティベートされていない状態でサーバーを起動しようとした

**解決方法**:
1. バッチファイル `start_server.bat` を使用（仮想環境のアクティベートが自動で行われる）
2. または、手動で仮想環境をアクティベート: `venv\Scripts\activate.bat`

**影響範囲**: 手順書の修正

**修正ファイル**:
- `進捗管理/フェーズ進捗メモ/Phase8_手動操作手順書.md`
- `backend/README_START.md`

---

### エラー2: `Identifier 'handleDelete' has already been declared` (2025-11-29)

**症状**: フロントエンドのコンパイルエラー

**原因**: `CasesPage.tsx`で`handleDelete`関数が重複定義されていた

**解決方法**: 重複定義を削除

**影響範囲**: フロントエンドのコンパイル

**修正ファイル**:
- `frontend/src/pages/CasesPage.tsx`

---

### エラー3: ログインできない (2025-11-29)

**症状**: ログイン画面でログインできない

**原因**: データベースにユーザーが存在しない

**解決方法**: シードデータを投入

**影響範囲**: 初期セットアップ

**修正ファイル**:
- `backend/scripts/run_seed_with_venv.bat` (新規作成)
- `進捗管理/フェーズ進捗メモ/Phase8_ログインエラー対処法.md` (新規作成)

---

### エラー4: WebSocket接続エラー（開発モード） (2025-11-29)

**症状**: コンソールにWebSocket接続エラーが表示される

**原因**: React StrictModeによる二重レンダリング

**解決方法**:
- 接続状態のチェックを改善
- 接続の遅延を100ms → 200msに延長
- 既に接続済みの場合は新しい接続を作成しない

**影響範囲**: WebSocket接続の安定性

**修正ファイル**:
- `frontend/src/hooks/useWebSocket.ts`

---

### エラー5: リアルタイム更新が動作しない (2025-11-29)

**症状**: 通知は表示されるが、案件一覧が自動更新されない

**原因**:
1. `fetchCases`が`useCallback`でメモ化されていない
2. `useEffect`の依存配列に`fetchCases`が含まれていない
3. `exclude_user_id`により操作したユーザーに通知が送信されていない

**解決方法**:
1. `fetchCases`を`useCallback`でメモ化
2. `useEffect`の依存配列に`fetchCases`を追加
3. `exclude_user_id`を`None`に変更（全ユーザーに通知を送信）
4. カスタムイベントリスナーも追加（二重の安全策）

**影響範囲**: リアルタイム更新機能

**修正ファイル**:
- `frontend/src/pages/CasesPage.tsx`
- `backend/app/api/endpoints/cases.py`

---

### エラー6: 接続・切断通知が表示されない (2025-11-29)

**症状**: ユーザーの接続・切断時に通知が表示されない

**原因**:
1. `useWebSocket.ts`で`user_connected`/`user_disconnected`のメッセージがカスタムイベントを発火していない
2. `RealtimeNotification.tsx`で直接メッセージ処理のリストに含まれていない

**解決方法**:
1. `useWebSocket.ts`で`user_connected`/`user_disconnected`のメッセージもカスタムイベントを発火
2. `RealtimeNotification.tsx`で直接メッセージ処理のリストに追加

**影響範囲**: 接続・切断通知機能

**修正ファイル**:
- `frontend/src/hooks/useWebSocket.ts`
- `frontend/src/components/RealtimeNotification.tsx`

---

### エラー7: 接続ユーザー数が実際より多く表示される (2025-11-29)

**症状**: 実際の接続ウィンドウ数よりも多く表示される

**原因**:
1. React StrictModeによる二重レンダリング
2. 同じユーザーの複数接続（複数タブ/ウィンドウ）
3. 接続数のカウント方法（全接続数を表示していた）

**解決方法**:
1. 接続ユーザー数（ユニークユーザー数）を表示するように変更
2. 全接続数も記録（デバッグ用、ツールチップに表示）
3. 接続の重複を防ぐ改善

**影響範囲**: サーバー状態表示

**修正ファイル**:
- `backend/app/api/endpoints/websocket.py`
- `frontend/src/hooks/useWebSocket.ts`
- `frontend/src/components/ServerStatus.tsx`

---

### エラー8: ネットワーク切断時にオフラインに切り替わらない (2025-11-29)

**症状**: ネットワークを切断しても「オンライン」のまま

**原因**:
1. WebSocketの`onerror`/`onclose`が即座に発火しない場合がある
2. 開発モードでのエラー無視ロジックが影響している
3. ネットワーク状態の監視が不足

**解決方法**:
1. `navigator.onLine` APIによるネットワーク状態監視を追加
2. WebSocket接続状態の定期チェック（10秒間隔）を追加
3. ハートビートのタイムアウト監視を改善（30秒）
4. `onerror`ハンドラーの改善（開発モードでも接続済みのエラーは無視しない）

**影響範囲**: ネットワーク切断検知

**修正ファイル**:
- `frontend/src/hooks/useWebSocket.ts`

---

## 注意事項・Tips

### 開発環境での注意点

1. **仮想環境のアクティベート**
   - バックエンドサーバー起動時は必ず仮想環境をアクティベート
   - バッチファイル `start_server.bat` を使用することを推奨

2. **PowerShellでの実行**
   - PowerShellでは `.\start_server.bat` のように `.\` を付ける必要がある

3. **React StrictMode**
   - 開発モードではコンポーネントが2回レンダリングされる
   - WebSocket接続も2回作成される可能性がある
   - 接続の重複を防ぐロジックが必要

4. **シードデータの投入**
   - 初回起動時は必ずシードデータを投入
   - `scripts\run_seed_with_venv.bat` を使用

### 本番環境での注意点

1. **WebSocket接続数の管理**
   - 接続ユーザー数と全接続数を区別して管理
   - 重複接続を考慮した設計

2. **ネットワーク切断の検知**
   - `navigator.onLine` APIとWebSocket接続状態の両方を監視
   - ハートビートのタイムアウト監視も重要

3. **通知の送信**
   - 操作したユーザーにも通知を送信する設計
   - 全ユーザーに通知を送信することで、リアルタイム更新が確実に動作する

---

**総エラー数**: 8件（全て解決済み）
