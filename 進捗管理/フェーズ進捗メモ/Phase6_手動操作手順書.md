# Phase 6: ドキュメント生成機能 - 手動操作手順書

## 📋 目次
1. [概要](#概要)
2. [事前準備](#事前準備)
3. [テストデータの作成](#テストデータの作成)
4. [実行前のデータ確認](#実行前のデータ確認)
5. [ドキュメント生成機能の実行](#ドキュメント生成機能の実行)
6. [実行後のデータ確認](#実行後のデータ確認)
7. [確認チェックリスト](#確認チェックリスト)
8. [トラブルシューティング](#トラブルシューティング)

---

## 概要

### Phase 6で実装した機能
- **Invoice（請求書）生成機能**
- **Packing List（梱包リスト）生成機能**
- **ドキュメント履歴管理機能**
- **ドキュメントダウンロード機能**

### 実装内容
#### バックエンド
- `backend/app/services/document_generator.py` - ドキュメント生成サービス
- `backend/app/api/endpoints/documents.py` - ドキュメント生成API
- `backend/templates/` - テンプレートディレクトリ
- `backend/generated_documents/` - 生成ドキュメント保存ディレクトリ

#### フロントエンド
- `frontend/src/api/documents.ts` - ドキュメントAPI
- `frontend/src/pages/DocumentsPage.tsx` - ドキュメント履歴ページ
- `frontend/src/components/Table/CaseTable.tsx` - ドキュメント生成ボタン追加
- `frontend/src/pages/DashboardPage.tsx` - ドキュメント履歴へのリンク追加

---

## 事前準備

### 1. 環境確認

```bash
# Windows環境の場合は、UTF-8エンコーディングを有効化（推奨）
chcp 65001

# プロジェクトルートに移動
cd "C:\Users\関伸\OneDrive - ペンギンロジスティクス株式会社\ドキュメント\ペンギンロジスティクス\e 営業部門\c AI事業部門\CURSOR\貿易DX"
```

### 2. 必要なライブラリの確認

```bash
# バックエンドディレクトリに移動
cd backend

# 仮想環境をアクティベート
.\venv\Scripts\activate

# openpyxlがインストールされているか確認
pip show openpyxl

# 未インストールの場合
pip install openpyxl==3.1.2
```

### 3. サーバーの起動

#### バックエンド
```bash
# backend ディレクトリで実行
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### フロントエンド
```bash
# frontend ディレクトリで実行（新しいターミナル）
cd frontend
npm run dev
```

### 4. ブラウザでアクセス
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs

---

## テストデータの作成

### 1. ログイン
1. ブラウザで http://localhost:3000 を開く
2. テストユーザーでログイン
   - ユーザー名: `testuser`
   - パスワード: `testpass123`

### 2. テスト用案件データの確認

#### 既存データの確認
1. ダッシュボード画面で「案件一覧へ」をクリック
2. 案件が登録されているか確認

#### 新規案件の作成（既存データが少ない場合）
1. 案件一覧ページで「新規作成」ボタンをクリック
2. 以下の情報を入力:
   - **案件番号**: 自動生成ボタンを使用
   - **区分**: 輸出 または 輸入
   - **顧客**: 既存顧客を選択
   - **商品**: 既存商品を選択
   - **数量**: 1000
   - **単位**: kg
   - **単価**: 500
   - **売上額**: 500000（自動計算）
   - **ステータス**: 受注済
   - **担当者**: テストユーザー
   - **船積予定日**: 任意の日付
3. 「作成」ボタンをクリック

---

## 実行前のデータ確認

### 1. 案件データの確認

```bash
# SQLiteデータベースに接続して確認
cd backend
sqlite3 trade_dx.db

# 案件データを確認
SELECT id, case_number, trade_type, customer_id, product_id, quantity, unit, sales_unit_price, sales_amount, status
FROM cases
LIMIT 5;

# 案件IDをメモしておく（例: 1, 2, 3など）
```

### 2. 顧客・商品データの確認

```sql
-- 顧客データを確認
SELECT id, customer_code, customer_name, address, contact_person FROM customers LIMIT 5;

-- 商品データを確認
SELECT id, product_code, product_name, unit, standard_price FROM products LIMIT 5;

-- SQLiteを終了
.exit
```

---

## ドキュメント生成機能の実行

### 方法1: フロントエンド（案件一覧画面）から生成

#### Invoice生成
1. ブラウザで http://localhost:3000/cases を開く
2. 案件一覧から任意の案件を選択
3. 行の右端にある「ドキュメント生成」ボタン（📄アイコン）をクリック
4. メニューから「Invoice 生成」を選択
5. 生成が完了すると自動的にダウンロードが開始される
6. ダウンロードされたExcelファイルを開いて内容を確認

#### Packing List生成
1. 案件一覧から任意の案件を選択
2. 行の右端にある「ドキュメント生成」ボタン（📄アイコン）をクリック
3. メニューから「Packing List 生成」を選択
4. 生成が完了すると自動的にダウンロードが開始される
5. ダウンロードされたExcelファイルを開いて内容を確認

### 方法2: APIから直接生成（開発者向け）

#### Invoice生成 API
```bash
# curlを使用（Windows PowerShell）
$token = "your_jwt_token_here"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}
$body = @{
    case_id = 1
    document_type = "invoice"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/documents/invoice" -Method POST -Headers $headers -Body $body
```

#### Packing List生成 API
```bash
# curlを使用（Windows PowerShell）
$body = @{
    case_id = 1
    document_type = "packing_list"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/documents/packing-list" -Method POST -Headers $headers -Body $body
```

### 方法3: ドキュメント履歴画面からダウンロード

1. ダッシュボード画面で「履歴を見る」をクリック
2. または http://localhost:3000/documents を直接開く
3. 生成済みドキュメントの一覧が表示される
4. ダウンロードしたいドキュメントの「ダウンロード」ボタン（⬇アイコン）をクリック

---

## 実行後のデータ確認

### 1. データベース確認

```bash
cd backend
sqlite3 trade_dx.db

# 生成されたドキュメントレコードを確認
SELECT
    id,
    case_id,
    document_type,
    file_name,
    template_name,
    generated_by,
    generated_at
FROM documents
ORDER BY generated_at DESC
LIMIT 10;

# 特定の案件のドキュメントを確認
SELECT * FROM documents WHERE case_id = 1;

.exit
```

### 2. 生成ファイルの確認

```bash
# 生成されたドキュメントファイルを確認
cd backend/generated_documents
dir

# ファイルが存在することを確認
# - invoice_案件番号_日時.xlsx
# - packing_list_案件番号_日時.xlsx
```

### 3. Excelファイルの内容確認

生成されたExcelファイルを開いて、以下を確認:

#### Invoice確認項目
- [ ] タイトル「INVOICE」が表示されている
- [ ] 発行者情報（会社名、住所、電話番号）が記載されている
- [ ] 請求先情報（顧客名、住所、連絡先）が表示されている
- [ ] Invoice番号（案件番号）が表示されている
- [ ] Invoice日付が表示されている
- [ ] 船積予定日が表示されている
- [ ] 明細行が表示されている
  - 商品コード
  - 商品名
  - 数量
  - 単位
  - 単価
  - 金額
- [ ] 合計金額が正しく計算されている
- [ ] 備考が表示されている（案件に備考がある場合）

#### Packing List確認項目
- [ ] タイトル「PACKING LIST」が表示されている
- [ ] 発行者情報が記載されている
- [ ] 送付先情報（顧客名、住所）が表示されている
- [ ] Packing List番号（案件番号）が表示されている
- [ ] Packing日付が表示されている
- [ ] 船積予定日が表示されている
- [ ] 明細行が表示されている
  - 商品コード
  - 商品名
  - 数量
  - 単位
  - 総重量
  - 正味重量
  - 梱包数
- [ ] 合計行が表示されている
- [ ] 備考が表示されている（案件に備考がある場合）

### 4. フロントエンド確認

#### ドキュメント履歴画面
1. http://localhost:3000/documents を開く
2. 生成したドキュメントが一覧に表示されていることを確認
3. フィルター機能を確認
   - ドキュメントタイプでフィルタ（Invoice / Packing List）
   - 案件IDでフィルタ
4. 表示項目を確認
   - ID
   - タイプ
   - 案件ID
   - ファイル名
   - テンプレート名
   - 生成日時
   - 備考

---

## 確認チェックリスト

### 基本機能
- [ ] バックエンドサーバーが正常に起動する
- [ ] フロントエンドサーバーが正常に起動する
- [ ] ログインができる
- [ ] ダッシュボードが表示される

### ドキュメント生成機能
- [ ] 案件一覧で「ドキュメント生成」ボタンが表示される
- [ ] ドキュメント生成メニューが開く
- [ ] Invoice生成ボタンをクリックできる
- [ ] Packing List生成ボタンをクリックできる
- [ ] 生成中はローディングアイコンが表示される
- [ ] 生成完了後、自動的にダウンロードが開始される
- [ ] 生成完了メッセージが表示される

### Invoice生成
- [ ] Invoiceファイルが生成される
- [ ] ファイル名が正しい形式（invoice_案件番号_日時.xlsx）
- [ ] Excelファイルが正常に開ける
- [ ] タイトルが「INVOICE」
- [ ] 案件情報が正しく表示される
- [ ] 顧客情報が正しく表示される
- [ ] 商品情報が正しく表示される
- [ ] 金額計算が正しい
- [ ] データベースにレコードが保存される

### Packing List生成
- [ ] Packing Listファイルが生成される
- [ ] ファイル名が正しい形式（packing_list_案件番号_日時.xlsx）
- [ ] Excelファイルが正常に開ける
- [ ] タイトルが「PACKING LIST」
- [ ] 案件情報が正しく表示される
- [ ] 顧客情報が正しく表示される
- [ ] 商品情報が正しく表示される
- [ ] 重量・梱包数が表示される
- [ ] データベースにレコードが保存される

### ドキュメント履歴画面
- [ ] /documents にアクセスできる
- [ ] ドキュメント一覧が表示される
- [ ] タイプでフィルタリングできる
- [ ] 案件IDでフィルタリングできる
- [ ] ダウンロードボタンが表示される
- [ ] ダウンロードボタンをクリックするとファイルがダウンロードされる
- [ ] 生成日時が正しく表示される

### エラーハンドリング
- [ ] 存在しない案件IDでエラーメッセージが表示される
- [ ] 認証なしでアクセスするとログイン画面にリダイレクトされる
- [ ] ネットワークエラー時に適切なエラーメッセージが表示される

### ナビゲーション
- [ ] ダッシュボードに「ドキュメント履歴」カードが表示される
- [ ] 「履歴を見る」ボタンでドキュメント履歴画面に遷移できる

---

## トラブルシューティング

### 問題1: 「openpyxl がインストールされていない」エラー

**症状:**
```
ModuleNotFoundError: No module named 'openpyxl'
```

**解決方法:**
```bash
cd backend
.\venv\Scripts\activate
pip install openpyxl==3.1.2
```

---

### 問題2: ドキュメント生成時に「Case ID not found」エラー

**症状:**
API呼び出し時に404エラーが返される

**解決方法:**
1. 案件IDが正しいか確認
```bash
cd backend
sqlite3 trade_dx.db
SELECT id, case_number FROM cases;
.exit
```

2. 存在する案件IDを使用して再試行

---

### 問題3: Excelファイルがダウンロードされない

**症状:**
生成ボタンをクリックしても何も起こらない

**解決方法:**
1. ブラウザのコンソールを開いて（F12キー）エラーを確認
2. ブラウザのポップアップブロッカーを確認
3. バックエンドログを確認
```bash
# バックエンドのターミナルでエラーログを確認
```

---

### 問題4: 生成されたExcelファイルが開けない

**症状:**
ダウンロードしたExcelファイルを開こうとするとエラーが出る

**解決方法:**
1. ファイルサイズを確認（0バイトでないか）
2. 拡張子が `.xlsx` か確認
3. backend/generated_documents/ に実際にファイルが生成されているか確認
```bash
cd backend/generated_documents
dir
```

---

### 問題5: ドキュメント履歴画面が空白

**症状:**
/documents にアクセスしても何も表示されない

**解決方法:**
1. ブラウザのコンソールでエラーを確認
2. バックエンドAPIが正常に応答しているか確認
```bash
# PowerShellで確認
$token = "your_jwt_token_here"
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-RestMethod -Uri "http://localhost:8000/api/documents" -Headers $headers
```

---

### 問題6: 文字化けが発生する

**症状:**
日本語が文字化けする

**解決方法:**
```bash
# Windows環境でUTF-8を有効化
chcp 65001
```

---

### 問題7: ファイル保存先が見つからない

**症状:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**解決方法:**
```bash
# ディレクトリを手動で作成
cd backend
mkdir templates
mkdir generated_documents
```

---

### 問題8: 権限エラー

**症状:**
```
PermissionError: [Errno 13] Permission denied
```

**解決方法:**
1. backend/generated_documents/ の書き込み権限を確認
2. 管理者権限でターミナルを開く
3. ウイルス対策ソフトのリアルタイム保護を一時的に無効化

---

## 動作確認の流れ（推奨）

### ステップ1: 基本確認（5分）
1. サーバー起動
2. ログイン
3. ダッシュボード表示確認

### ステップ2: Invoice生成（5分）
1. 案件一覧を開く
2. 任意の案件でInvoice生成
3. ダウンロードされたファイルを開いて確認
4. データベースにレコードが保存されているか確認

### ステップ3: Packing List生成（5分）
1. 案件一覧を開く
2. 任意の案件でPacking List生成
3. ダウンロードされたファイルを開いて確認
4. データベースにレコードが保存されているか確認

### ステップ4: ドキュメント履歴確認（5分）
1. ドキュメント履歴画面を開く
2. 生成したドキュメントが表示されているか確認
3. フィルター機能を試す
4. ダウンロード機能を試す

### ステップ5: エッジケース確認（5分）
1. 存在しない案件IDでエラーが出るか確認
2. 同じ案件で複数回生成できるか確認
3. 複数のドキュメントを連続で生成できるか確認

**合計所要時間: 約25分**

---

## 次のステップ

Phase 6の動作確認が完了したら、以下を実施してください:

1. **進捗管理書の更新**
   - `進捗管理/全体進捗管理書.md` のPhase 6を「実行確認完了」に更新

2. **Phase 7の準備**
   - Phase 7「変更履歴・バックアップ」の要件を確認
   - 必要なライブラリやツールの調査

3. **本番環境への展開準備**（最終フェーズ後）
   - 本番用設定ファイルの作成
   - デプロイ手順書の作成

---

## 参考情報

### API エンドポイント一覧
- POST /api/documents/invoice - Invoice生成
- POST /api/documents/packing-list - Packing List生成
- GET /api/documents - ドキュメント一覧取得
- GET /api/documents/{id}/download - ドキュメントダウンロード

### 実装ファイル一覧
#### バックエンド
- `backend/app/services/document_generator.py`
- `backend/app/api/endpoints/documents.py`
- `backend/app/models/document.py`
- `backend/app/schemas/document.py`

#### フロントエンド
- `frontend/src/api/documents.ts`
- `frontend/src/pages/DocumentsPage.tsx`
- `frontend/src/components/Table/CaseTable.tsx`
- `frontend/src/pages/DashboardPage.tsx`
- `frontend/src/App.tsx`

---

**作成日**: 2025-11-27
**最終更新**: 2025-11-27
**対象フェーズ**: Phase 6（ドキュメント生成機能）
