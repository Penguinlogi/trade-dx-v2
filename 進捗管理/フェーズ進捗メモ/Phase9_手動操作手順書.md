# Phase 9: テストとデバッグ - 手動操作手順書

## 📋 目次
1. [概要](#概要)
2. [実行前の準備](#実行前の準備)
3. [バックエンドテストの実行](#バックエンドテストの実行)
4. [フロントエンドテストの実行](#フロントエンドテストの実行)
5. [E2Eテストの実行](#e2eテストの実行)
6. [テストカバレッジの確認](#テストカバレッジの確認)
7. [確認チェックリスト](#確認チェックリスト)
8. [トラブルシューティング](#トラブルシューティング)

---

## 概要

Phase 9では、以下のテスト機能が実装されました：
- **バックエンドテスト**: pytestを使用したAPI単体テスト・統合テスト
- **フロントエンドテスト**: Vitestを使用したコンポーネントテスト
- **E2Eテスト**: Playwrightを使用したエンドツーエンドテスト
- **カバレッジレポート**: テストカバレッジの可視化

---

## 実行前の準備

### 1. 依存関係のインストール

#### バックエンド依存関係のインストール

**方法1: バッチファイルでインストール（Windows・推奨）**

```batch
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**方法2: コマンドプロンプトから手動でインストール**

```batch
cd backend
venv\Scripts\activate.bat
pip install pytest pytest-asyncio pytest-cov httpx
```

**方法3: PowerShellからインストール**

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### フロントエンド依存関係のインストール

```bash
cd frontend
npm install
```

**注意**: Playwrightのブラウザをインストールする必要があります：

```bash
cd frontend
npx playwright install
```

### 2. サーバー起動（E2Eテスト用）

E2Eテストを実行する場合は、バックエンドとフロントエンドのサーバーを起動する必要があります。

#### バックエンドサーバー起動

```batch
cd backend
venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### フロントエンドサーバー起動

```bash
cd frontend
npm run dev
```

**注意**: Playwrightの設定では、E2Eテスト実行時に自動的にフロントエンドサーバーを起動します。

---

## バックエンドテストの実行

### 方法1: バッチファイルで実行（Windows・推奨）

```batch
cd backend
run_tests.bat
```

このスクリプトは以下を実行します：
- 仮想環境のアクティベート
- pytestの実行（カバレッジ付き）
- HTMLカバレッジレポートの生成

### 方法2: コマンドプロンプトから手動で実行

```batch
cd backend
venv\Scripts\activate.bat
pytest tests/ -v
```

### 方法3: カバレッジ付きで実行

```batch
cd backend
venv\Scripts\activate.bat
pytest tests/ -v --cov=app --cov-report=html --cov-report=term
```

### 方法4: 特定のテストファイルのみ実行

```batch
cd backend
venv\Scripts\activate.bat
pytest tests/test_auth.py -v
```

### 方法5: 特定のテストクラスまたは関数のみ実行

```batch
cd backend
venv\Scripts\activate.bat
pytest tests/test_auth.py::TestAuth::test_login_success -v
```

### 実行結果の確認

#### ターミナル出力

テスト実行後、以下のような出力が表示されます：

```
tests/test_auth.py::TestAuth::test_login_success PASSED
tests/test_auth.py::TestAuth::test_login_invalid_username PASSED
tests/test_cases.py::TestCases::test_create_case PASSED
...
========================= X passed in Y.YYs =========================
```

#### カバレッジレポート（HTML）

カバレッジ付きで実行した場合、`backend/htmlcov/index.html` が生成されます。
ブラウザでこのファイルを開くと、カバレッジレポートを確認できます。

---

## フロントエンドテストの実行

### 方法1: npmコマンドで実行

```bash
cd frontend
npm test
```

### 方法2: UIモードで実行（推奨）

```bash
cd frontend
npm run test:ui
```

ブラウザが自動的に開き、テスト結果を視覚的に確認できます。

### 方法3: カバレッジ付きで実行

```bash
cd frontend
npm run test:coverage
```

### 方法4: ウォッチモードで実行

```bash
cd frontend
npm test -- --watch
```

ファイル変更を監視し、自動的にテストを再実行します。

### 実行結果の確認

#### ターミナル出力

テスト実行後、以下のような出力が表示されます：

```
✓ src/components/__tests__/PrivateRoute.test.tsx (3)
  ✓ PrivateRoute (3)
    ✓ 認証済みユーザーは子コンポーネントを表示する
    ✓ 未認証ユーザーはログインページにリダイレクトされる
    ✓ ローディング中はローディングインジケーターを表示する

Test Files  1 passed (1)
     Tests  3 passed (3)
```

#### カバレッジレポート

カバレッジ付きで実行した場合、`frontend/coverage/` ディレクトリにレポートが生成されます。

---

## E2Eテストの実行

### 前提条件

E2Eテストを実行する前に、以下を確認してください：
1. バックエンドサーバーが起動している（http://localhost:8000）
2. フロントエンドサーバーが起動している（http://localhost:3000）
   - または、Playwrightの設定で自動起動される

### 方法1: npmコマンドで実行

```bash
cd frontend
npm run test:e2e
```

### 方法2: UIモードで実行（推奨）

```bash
cd frontend
npm run test:e2e:ui
```

PlaywrightのUIモードが起動し、テストを視覚的に確認しながら実行できます。

### 方法3: 特定のブラウザのみで実行

```bash
cd frontend
npx playwright test --project=chromium
```

### 方法4: 特定のテストファイルのみ実行

```bash
cd frontend
npx playwright test e2e/login.spec.ts
```

### 実行結果の確認

#### ターミナル出力

テスト実行後、以下のような出力が表示されます：

```
Running 3 tests using 1 worker

  ✓ e2e/login.spec.ts:5:3 › ログインページ › ログインフォームが表示される (2.1s)
  ✓ e2e/navigation.spec.ts:5:3 › ナビゲーション › 未認証ユーザーはログインページにリダイレクトされる (1.8s)

  3 passed (5.2s)
```

#### HTMLレポート

テスト実行後、以下のコマンドでHTMLレポートを表示できます：

```bash
cd frontend
npx playwright show-report
```

---

## テストカバレッジの確認

### バックエンドカバレッジ

#### HTMLレポートの確認

1. バックエンドテストをカバレッジ付きで実行：
   ```batch
   cd backend
   venv\Scripts\activate.bat
   pytest tests/ -v --cov=app --cov-report=html
   ```

2. `backend/htmlcov/index.html` をブラウザで開く

3. 各モジュールのカバレッジを確認：
   - ファイルごとのカバレッジ率
   - カバーされていない行のハイライト
   - 全体のカバレッジ率

#### ターミナル出力での確認

```batch
cd backend
venv\Scripts\activate.bat
pytest tests/ --cov=app --cov-report=term
```

ターミナルに以下のような出力が表示されます：

```
---------- coverage: platform win32, python 3.13 -----------
Name                    Stmts   Miss  Cover
--------------------------------------------
app/__init__.py             0      0   100%
app/api/endpoints/auth.py  45      2    96%
app/api/endpoints/cases.py 120     15    88%
...
--------------------------------------------
TOTAL                     500     50    90%
```

### フロントエンドカバレッジ

#### カバレッジレポートの確認

1. フロントエンドテストをカバレッジ付きで実行：
   ```bash
   cd frontend
   npm run test:coverage
   ```

2. `frontend/coverage/` ディレクトリ内のHTMLファイルをブラウザで開く

3. 各コンポーネント・モジュールのカバレッジを確認

---

## 確認チェックリスト

### バックエンドテスト

- [ ] 全テストが成功する
  ```batch
  cd backend
  venv\Scripts\activate.bat
  pytest tests/ -v
  ```
- [ ] 認証APIのテストが成功する
  ```batch
  pytest tests/test_auth.py -v
  ```
- [ ] 案件APIのテストが成功する
  ```batch
  pytest tests/test_cases.py -v
  ```
- [ ] 顧客APIのテストが成功する
  ```batch
  pytest tests/test_customers.py -v
  ```
- [ ] 商品APIのテストが成功する
  ```batch
  pytest tests/test_products.py -v
  ```
- [ ] 統合テストが成功する
  ```batch
  pytest tests/test_integration.py -v
  ```
- [ ] ドキュメント生成APIのテストが成功する
  ```batch
  pytest tests/test_documents.py -v
  ```
- [ ] 変更履歴APIのテストが成功する
  ```batch
  pytest tests/test_change_history.py -v
  ```
- [ ] バックアップAPIのテストが成功する
  ```batch
  pytest tests/test_backups.py -v
  ```
- [ ] 集計・ダッシュボードAPIのテストが成功する
  ```batch
  pytest tests/test_analytics.py -v
  ```
- [ ] 案件番号生成APIのテストが成功する
  ```batch
  pytest tests/test_case_numbers.py -v
  ```
- [ ] カバレッジレポートが生成される
  ```batch
  pytest tests/ --cov=app --cov-report=html
  ```
- [ ] カバレッジ率が80%以上である（目標）

### フロントエンドテスト

- [ ] 全テストが成功する
  ```bash
  cd frontend
  npm test
  ```
- [ ] PrivateRouteコンポーネントのテストが成功する
- [ ] 認証APIのテストが成功する
- [ ] カバレッジレポートが生成される
  ```bash
  npm run test:coverage
  ```
- [ ] カバレッジ率が70%以上である（目標）

### E2Eテスト

- [ ] 全E2Eテストが成功する
  ```bash
  cd frontend
  npm run test:e2e
  ```
- [ ] ログインテストが成功する
- [ ] ナビゲーションテストが成功する
- [ ] 複数のブラウザでテストが成功する（chromium, firefox, webkit）

### エラーハンドリング確認

- [ ] 無効な認証情報でのログインが適切にエラーを返す
- [ ] 存在しないリソースへのアクセスが404を返す
- [ ] 認証なしでのアクセスが401を返す
- [ ] バリデーションエラーが適切に処理される

---

## トラブルシューティング

### バックエンドテスト

#### エラー: `ModuleNotFoundError: No module named 'pytest'`

**原因**: pytestがインストールされていない

**解決方法**:
```batch
cd backend
venv\Scripts\activate.bat
pip install pytest pytest-asyncio pytest-cov httpx
```

#### エラー: `ImportError: cannot import name 'TestClient' from 'fastapi.testclient'`

**原因**: FastAPIのバージョンが古い

**解決方法**:
```batch
cd backend
venv\Scripts\activate.bat
pip install --upgrade fastapi
```

#### エラー: データベース関連のエラー

**原因**: テスト用データベースの設定が正しくない

**解決方法**: `tests/conftest.py` の設定を確認してください。テストはインメモリSQLiteデータベースを使用します。

### フロントエンドテスト

#### エラー: `Cannot find module '@testing-library/react'`

**原因**: テストライブラリがインストールされていない

**解決方法**:
```bash
cd frontend
npm install
```

#### エラー: `ReferenceError: document is not defined`

**原因**: jsdom環境が正しく設定されていない

**解決方法**: `vite.config.ts` の `test.environment` が `'jsdom'` に設定されているか確認してください。

#### エラー: モックが動作しない

**原因**: モックの設定が正しくない

**解決方法**: `src/test/setup.ts` と各テストファイルのモック設定を確認してください。

### E2Eテスト

#### エラー: `browserType.launch: Executable doesn't exist`

**原因**: Playwrightのブラウザがインストールされていない

**解決方法**:
```bash
cd frontend
npx playwright install
```

#### エラー: `net::ERR_CONNECTION_REFUSED`

**原因**: バックエンドまたはフロントエンドサーバーが起動していない

**解決方法**:
1. バックエンドサーバーを起動: `cd backend && python -m uvicorn app.main:app --reload`
2. フロントエンドサーバーを起動: `cd frontend && npm run dev`
3. または、Playwrightの設定で自動起動を有効にする

#### エラー: タイムアウトエラー

**原因**: テストのタイムアウト時間が短すぎる

**解決方法**: `playwright.config.ts` の `timeout` 設定を増やすか、特定のテストで `test.setTimeout()` を使用する

### カバレッジレポート

#### カバレッジレポートが生成されない

**原因**: カバレッジツールが正しく設定されていない

**解決方法**:
- バックエンド: `pytest-cov` がインストールされているか確認
- フロントエンド: `@vitest/coverage-v8` がインストールされているか確認

#### カバレッジ率が低い

**原因**: テストが不足している

**解決方法**: カバレッジレポートでカバーされていない行を確認し、追加のテストを作成してください。

---

## 次のステップ

Phase 9のテストとデバッグが完了したら、以下を確認してください：

1. **全テストが成功する**: バックエンド・フロントエンド・E2Eすべてのテストが成功する
2. **カバレッジ目標を達成**: バックエンド80%以上、フロントエンド70%以上
3. **エラーハンドリングが適切**: すべてのエラーケースがテストされている
4. **ドキュメントが更新されている**: テスト実行方法が文書化されている

---

## 参考情報

### テストファイルの場所

- バックエンドテスト: `backend/tests/`
- フロントエンドテスト: `frontend/src/**/__tests__/` または `frontend/src/**/*.test.tsx`
- E2Eテスト: `frontend/e2e/`

### テスト実行コマンド一覧

#### バックエンド
```batch
# 全テスト実行
pytest tests/ -v

# カバレッジ付き
pytest tests/ --cov=app --cov-report=html

# 特定のテスト
pytest tests/test_auth.py -v
```

#### フロントエンド
```bash
# 全テスト実行
npm test

# UIモード
npm run test:ui

# カバレッジ付き
npm run test:coverage
```

#### E2E
```bash
# 全テスト実行
npm run test:e2e

# UIモード
npm run test:e2e:ui
```

---

**最終更新**: 2025-11-29

## 追加テスト（2025-11-29）

以下のテストファイルが追加されました：

### 追加されたテストファイル

1. **test_documents.py** - ドキュメント生成APIのテスト
   - Invoice生成
   - Packing List生成
   - ドキュメント一覧取得
   - ドキュメントダウンロード
   - フィルタリング機能

2. **test_change_history.py** - 変更履歴APIのテスト
   - 変更履歴一覧取得
   - 変更履歴詳細取得
   - フィルタリング（案件ID、変更タイプ）
   - ページネーション
   - 特定案件の変更履歴取得

3. **test_backups.py** - バックアップAPIのテスト
   - バックアップ作成
   - バックアップ一覧取得
   - バックアップ詳細取得
   - フィルタリング（タイプ、ステータス）
   - 権限チェック（スーパーユーザーのみの操作）

4. **test_analytics.py** - 集計・ダッシュボードAPIのテスト
   - 集計サマリー取得
   - 月次トレンド取得
   - 顧客別売上TOP取得
   - 日付範囲指定

5. **test_case_numbers.py** - 案件番号生成APIのテスト
   - 輸入案件番号生成
   - 輸出案件番号生成
   - 連続した案件番号生成
   - 現在の連番取得

### 追加テストの実行方法

全テストを実行：
```batch
cd backend
venv\Scripts\activate.bat
pytest tests/ -v
```

特定のテストファイルのみ実行：
```batch
pytest tests/test_documents.py -v
pytest tests/test_change_history.py -v
pytest tests/test_backups.py -v
pytest tests/test_analytics.py -v
pytest tests/test_case_numbers.py -v
```
