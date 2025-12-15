# Phase 4: マスタ管理 - 手動操作手順書

## 📋 目次
1. [概要](#概要)
2. [事前準備](#事前準備)
3. [テストデータの作成方法](#テストデータの作成方法)
4. [実行前のデータ確認](#実行前のデータ確認)
5. [システムの起動方法](#システムの起動方法)
6. [機能の動作確認](#機能の動作確認)
7. [実行後のデータ確認](#実行後のデータ確認)
8. [確認チェックリスト](#確認チェックリスト)
9. [トラブルシューティング](#トラブルシューティング)

---

## 概要

Phase 4では、以下のマスタ管理機能を実装しました：

### 実装機能
- ✅ **顧客マスタ管理**: 顧客情報の一覧表示、検索、削除
- ✅ **商品マスタ管理**: 商品情報の一覧表示、検索、削除
- ✅ **オートコンプリート機能**: 案件フォームでの顧客・商品選択用API

### API エンドポイント
#### 顧客マスタ
- `GET /api/customers/` - 顧客一覧取得
- `GET /api/customers/{id}` - 顧客詳細取得
- `POST /api/customers/` - 顧客新規作成
- `PUT /api/customers/{id}` - 顧客更新
- `DELETE /api/customers/{id}` - 顧客削除（論理削除）
- `GET /api/customers/autocomplete/` - オートコンプリート

#### 商品マスタ
- `GET /api/products/` - 商品一覧取得
- `GET /api/products/{id}` - 商品詳細取得
- `POST /api/products/` - 商品新規作成
- `PUT /api/products/{id}` - 商品更新
- `DELETE /api/products/{id}` - 商品削除（論理削除）
- `GET /api/products/autocomplete/` - オートコンプリート
- `GET /api/products/categories/` - カテゴリ一覧取得

---

## 事前準備

### 必要な環境
- Python 3.11+ がインストールされていること
- Node.js 18+ がインストールされていること
- バックエンドの仮想環境がセットアップされていること
- フロントエンドの依存関係がインストールされていること

### ディレクトリ構造確認
```
貿易DX/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/
│   │   │   ├── customers.py      ← 新規作成
│   │   │   └── products.py       ← 新規作成
│   │   ├── schemas/
│   │   │   ├── customer.py       ← 新規作成
│   │   │   └── product.py        ← 新規作成
│   │   └── main.py                ← 更新
│   ├── scripts/
│   │   └── seed_data.py           ← 確認（既存）
│   └── trade_dx.db
├── frontend/
│   └── src/
│       ├── api/
│       │   ├── customers.ts       ← 新規作成
│       │   └── products.ts        ← 新規作成
│       ├── pages/
│       │   ├── CustomersPage.tsx  ← 新規作成
│       │   └── ProductsPage.tsx   ← 新規作成
│       └── types/
│           ├── customer.ts        ← 新規作成
│           └── product.ts         ← 新規作成
```

---

## テストデータの作成方法

### 方法1: シードスクリプトの実行（推奨）

Phase 1で作成済みのシードデータに、顧客・商品データが既に含まれています。

#### Windows
```cmd
cd backend
venv\Scripts\activate
python scripts/seed_data.py
```

#### Mac/Linux
```bash
cd backend
source venv/bin/activate
python scripts/seed_data.py
```

### 方法2: 簡易実行バッチファイル（Windows）
```cmd
cd backend\scripts
run_seed_simple.bat
```

### 期待される出力
```
============================================================
シードデータ投入スクリプト
============================================================
テーブルを作成中...
✓ テーブル作成完了

初期ユーザーを作成中...
  - admin (管理者)
  - yamada (山田太郎)
  - suzuki (鈴木花子)
✓ ユーザー作成完了

顧客マスタを作成中...
  - C001: ABC商事株式会社
  - C002: XYZ物産株式会社
  - C003: グローバル貿易株式会社
✓ 顧客マスタ作成完了

商品マスタを作成中...
  - P001: 電子部品A
  - P002: プラスチック原料B
  - P003: 金属パーツC
  - P004: 繊維製品D
✓ 商品マスタ作成完了

案件番号管理を初期化中...
  - 2025-EX: 連番初期化
  - 2025-IM: 連番初期化
✓ 案件番号管理初期化完了

============================================================
✓ すべてのシードデータ投入が完了しました
============================================================
```

---

## 実行前のデータ確認

### データベースの確認

#### 方法1: SQLiteコマンド（推奨）
```cmd
cd backend
sqlite3 trade_dx.db
```

```sql
-- 顧客マスタのデータ確認
SELECT * FROM customers;

-- 商品マスタのデータ確認
SELECT * FROM products;

-- 終了
.quit
```

#### 方法2: Pythonスクリプトで確認
```cmd
cd backend
venv\Scripts\activate
python scripts/check_database.py
```

### 期待される結果

#### 顧客マスタ
| id | customer_code | customer_name | customer_name_en | is_active |
|----|---------------|---------------|------------------|-----------|
| 1 | C001 | ABC商事株式会社 | ABC Trading Co., Ltd. | 1 |
| 2 | C002 | XYZ物産株式会社 | XYZ Corporation | 1 |
| 3 | C003 | グローバル貿易株式会社 | Global Trade Inc. | 1 |

#### 商品マスタ
| id | product_code | product_name | category | unit | standard_price | is_active |
|----|--------------|-------------|----------|------|----------------|-----------|
| 1 | P001 | 電子部品A | 電子部品 | pcs | 150.00 | 1 |
| 2 | P002 | プラスチック原料B | 化学製品 | kg | 250.00 | 1 |
| 3 | P003 | 金属パーツC | 金属製品 | pcs | 500.00 | 1 |
| 4 | P004 | 繊維製品D | 繊維 | m | 80.00 | 1 |

---

## システムの起動方法

### 方法1: 個別起動（推奨）

#### バックエンドの起動
```cmd
# Windowsの場合
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**確認**: `http://localhost:8000` にアクセスして、以下が表示されることを確認
```json
{
  "message": "貿易DX管理システム API",
  "version": "2.1.0",
  "status": "running"
}
```

**Swagger UI**: `http://localhost:8000/docs` にアクセスして、以下のエンドポイントが表示されることを確認
- `GET /api/customers/` - 顧客マスタ一覧取得
- `GET /api/products/` - 商品マスタ一覧取得

#### フロントエンドの起動
```cmd
# 別のターミナルで
cd frontend
npm run dev
```

**確認**: `http://localhost:3000` にアクセスして、ログイン画面が表示されることを確認

### 方法2: Docker Compose起動
```cmd
# プロジェクトルートで
docker-compose up -d
```

---

## 機能の動作確認

### 1. ログイン

1. ブラウザで `http://localhost:3000` にアクセス
2. ログイン画面で以下の認証情報を入力：
   - **ユーザー名**: `admin`
   - **パスワード**: `admin123`
3. 「ログイン」ボタンをクリック

**期待される結果**: ダッシュボード画面に遷移する

---

### 2. 顧客マスタ管理の確認

#### 2-1. 顧客一覧画面へのアクセス

1. ダッシュボードで「顧客マスタ」カードの「顧客一覧へ」ボタンをクリック
2. または、ブラウザで `http://localhost:3000/customers` に直接アクセス

**期待される結果**:
- 顧客一覧画面が表示される
- ページタイトル: 「顧客マスタ」
- 「新規顧客登録」ボタンが表示される
- テーブルに3件の顧客データが表示される

#### 2-2. 顧客一覧の確認

**表示される顧客データ**:

| 顧客コード | 顧客名 | 顧客名（英語） | 電話番号 | 担当者 | ステータス |
|-----------|--------|----------------|----------|--------|-----------|
| C001 | ABC商事株式会社 | ABC Trading Co., Ltd. | 03-1234-5678 | 田中一郎 | 有効 |
| C002 | XYZ物産株式会社 | XYZ Corporation | 06-9876-5432 | 佐藤花子 | 有効 |
| C003 | グローバル貿易株式会社 | Global Trade Inc. | 045-1111-2222 | 高橋次郎 | 有効 |

**確認ポイント**:
- ✅ 3件のデータが表示されている
- ✅ 各行に「編集」と「削除」アイコンボタンが表示されている
- ✅ ステータスが「有効」の緑色チップで表示されている
- ✅ テーブルヘッダーが正しく表示されている

#### 2-3. 検索機能の確認

1. 検索ボックスに「ABC」と入力
2. Enterキーを押すか、虫眼鏡アイコンをクリック

**期待される結果**:
- ABC商事株式会社のみが表示される
- 件数表示が「全 1 件」になる

3. 検索ボックスをクリアして再検索

**期待される結果**:
- 全3件が再表示される
- 件数表示が「全 3 件」に戻る

#### 2-4. フィルター機能の確認

1. 「ステータス」ドロップダウンで「全て」を選択
2. 「全 3 件」が表示されることを確認

#### 2-5. 削除機能の確認

⚠️ **注意**: 実際にデータを削除しないでください。以下は確認のみ行ってください。

1. いずれかの顧客の「削除」アイコン（ゴミ箱）をクリック
2. 確認ダイアログが表示されることを確認

**期待されるダイアログメッセージ**:
```
この顧客を削除しますか？
（論理削除されます）
```

3. 「キャンセル」をクリックして削除を中止

---

### 3. 商品マスタ管理の確認

#### 3-1. 商品一覧画面へのアクセス

1. ダッシュボードで「商品マスタ」カードの「商品一覧へ」ボタンをクリック
2. または、ブラウザで `http://localhost:3000/products` に直接アクセス

**期待される結果**:
- 商品一覧画面が表示される
- ページタイトル: 「商品マスタ」
- 「新規商品登録」ボタンが表示される
- テーブルに4件の商品データが表示される

#### 3-2. 商品一覧の確認

**表示される商品データ**:

| 商品コード | 商品名 | 商品名（英語） | カテゴリ | 標準単価 | 単位 | ステータス |
|-----------|--------|----------------|----------|----------|------|-----------|
| P001 | 電子部品A | Electronic Component A | 電子部品 | ¥150 | pcs | 有効 |
| P002 | プラスチック原料B | Plastic Material B | 化学製品 | ¥250 | kg | 有効 |
| P003 | 金属パーツC | Metal Parts C | 金属製品 | ¥500 | pcs | 有効 |
| P004 | 繊維製品D | Textile Product D | 繊維 | ¥80 | m | 有効 |

**確認ポイント**:
- ✅ 4件のデータが表示されている
- ✅ 各行に「編集」と「削除」アイコンボタンが表示されている
- ✅ ステータスが「有効」の緑色チップで表示されている
- ✅ 標準単価が日本円フォーマットで表示されている（¥マーク付き）
- ✅ テーブルヘッダーが正しく表示されている

#### 3-3. 検索機能の確認

1. 検索ボックスに「電子」と入力
2. Enterキーを押すか、虫眼鏡アイコンをクリック

**期待される結果**:
- 電子部品Aのみが表示される
- 件数表示が「全 1 件」になる

3. 検索ボックスをクリアして再検索

**期待される結果**:
- 全4件が再表示される
- 件数表示が「全 4 件」に戻る

#### 3-4. カテゴリフィルターの確認

1. 「カテゴリ」ドロップダウンをクリック

**期待される結果**:
- 以下のカテゴリが表示される:
  - 全て
  - 電子部品
  - 化学製品
  - 金属製品
  - 繊維

2. 「電子部品」を選択

**期待される結果**:
- P001: 電子部品A のみが表示される
- 件数表示が「全 1 件」になる

3. 「全て」を選択して元に戻す

#### 3-5. 削除機能の確認

⚠️ **注意**: 実際にデータを削除しないでください。以下は確認のみ行ってください。

1. いずれかの商品の「削除」アイコン（ゴミ箱）をクリック
2. 確認ダイアログが表示されることを確認

**期待されるダイアログメッセージ**:
```
この商品を削除しますか？
（論理削除されます）
```

3. 「キャンセル」をクリックして削除を中止

---

### 4. APIエンドポイントの確認（Swagger UI）

1. ブラウザで `http://localhost:8000/docs` にアクセス
2. Swagger UIが表示されることを確認

#### 顧客マスタAPIの確認

1. 「顧客マスタ」セクションを展開
2. 以下のエンドポイントが表示されることを確認:
   - `GET /api/customers/` - 顧客マスタ一覧取得
   - `POST /api/customers/` - 顧客マスタ新規作成
   - `GET /api/customers/autocomplete/` - オートコンプリート
   - `GET /api/customers/{customer_id}` - 顧客マスタ詳細取得
   - `PUT /api/customers/{customer_id}` - 顧客マスタ更新
   - `DELETE /api/customers/{customer_id}` - 顧客マスタ削除

3. `GET /api/customers/` をクリックして「Try it out」をクリック
4. 「Execute」をクリック

**期待される結果** (Response body):
```json
{
  "total": 3,
  "items": [
    {
      "id": 1,
      "customer_code": "C001",
      "customer_name": "ABC商事株式会社",
      "customer_name_en": "ABC Trading Co., Ltd.",
      "address": "東京都千代田区丸の内1-1-1",
      "address_en": "1-1-1 Marunouchi, Chiyoda-ku, Tokyo, Japan",
      "phone": "03-1234-5678",
      "contact_person": "田中一郎",
      "email": "tanaka@abc-trading.co.jp",
      "payment_terms": "月末締め翌月末払い",
      "notes": null,
      "is_active": 1,
      "created_at": "2025-11-25T...",
      "updated_at": "2025-11-25T..."
    },
    // ... 他の顧客データ
  ],
  "page": 1,
  "page_size": 50,
  "total_pages": 1
}
```

#### 商品マスタAPIの確認

1. 「商品マスタ」セクションを展開
2. 以下のエンドポイントが表示されることを確認:
   - `GET /api/products/` - 商品マスタ一覧取得
   - `POST /api/products/` - 商品マスタ新規作成
   - `GET /api/products/autocomplete/` - オートコンプリート
   - `GET /api/products/categories/` - カテゴリ一覧取得
   - `GET /api/products/{product_id}` - 商品マスタ詳細取得
   - `PUT /api/products/{product_id}` - 商品マスタ更新
   - `DELETE /api/products/{product_id}` - 商品マスタ削除

3. `GET /api/products/` をクリックして「Try it out」をクリック
4. 「Execute」をクリック

**期待される結果** (Response body):
```json
{
  "total": 4,
  "items": [
    {
      "id": 1,
      "product_code": "P001",
      "product_name": "電子部品A",
      "product_name_en": "Electronic Component A",
      "hs_code": "8542.31.000",
      "unit": "pcs",
      "standard_price": 150.00,
      "category": "電子部品",
      "specification": "サイズ: 10mm×10mm, 動作温度: -40～85℃",
      "notes": null,
      "is_active": 1,
      "created_at": "2025-11-25T...",
      "updated_at": "2025-11-25T..."
    },
    // ... 他の商品データ
  ],
  "page": 1,
  "page_size": 50,
  "total_pages": 1
}
```

#### オートコンプリートAPIの確認

1. `GET /api/customers/autocomplete/` をクリック
2. 「Try it out」をクリック
3. `q` パラメータに「ABC」と入力
4. 「Execute」をクリック

**期待される結果**:
```json
[
  {
    "id": 1,
    "customer_code": "C001",
    "customer_name": "ABC商事株式会社",
    // ... 他のフィールド
  }
]
```

5. `GET /api/products/autocomplete/` でも同様に確認
6. `q` パラメータに「電子」と入力

**期待される結果**:
```json
[
  {
    "id": 1,
    "product_code": "P001",
    "product_name": "電子部品A",
    // ... 他のフィールド
  }
]
```

---

## 実行後のデータ確認

### データベースの確認（削除操作を行った場合）

論理削除を実行した場合、`is_active` フラグが `0` に更新されていることを確認します。

```cmd
cd backend
sqlite3 trade_dx.db
```

```sql
-- 論理削除された顧客を確認
SELECT id, customer_code, customer_name, is_active FROM customers WHERE is_active = 0;

-- 論理削除された商品を確認
SELECT id, product_code, product_name, is_active FROM products WHERE is_active = 0;

-- 終了
.quit
```

### フロントエンドでの確認

1. 顧客一覧画面で「ステータス」フィルタを「無効」に変更
2. 論理削除された顧客が表示されることを確認
3. ステータスが「無効」の灰色チップで表示されることを確認

---

## 確認チェックリスト

### 環境確認
- [ ] バックエンドが起動している（`http://localhost:8000`）
- [ ] フロントエンドが起動している（`http://localhost:3000`）
- [ ] Swagger UIにアクセスできる（`http://localhost:8000/docs`）
- [ ] データベースにテストデータが存在する

### 顧客マスタ機能
- [ ] 顧客一覧画面にアクセスできる
- [ ] 3件の顧客データが表示される
- [ ] 検索機能が動作する
- [ ] ステータスフィルタが動作する
- [ ] 削除ボタンをクリックすると確認ダイアログが表示される
- [ ] テーブルのホバーエフェクトが動作する

### 商品マスタ機能
- [ ] 商品一覧画面にアクセスできる
- [ ] 4件の商品データが表示される
- [ ] 検索機能が動作する
- [ ] カテゴリフィルタが動作する（4つのカテゴリが表示される）
- [ ] ステータスフィルタが動作する
- [ ] 標準単価が日本円フォーマットで表示される
- [ ] 削除ボタンをクリックすると確認ダイアログが表示される

### API機能
- [ ] `GET /api/customers/` が200を返す
- [ ] `GET /api/products/` が200を返す
- [ ] `GET /api/customers/autocomplete/` が動作する
- [ ] `GET /api/products/autocomplete/` が動作する
- [ ] `GET /api/products/categories/` がカテゴリ一覧を返す

### UI/UX
- [ ] ダッシュボードから各マスタ画面に遷移できる
- [ ] ページネーションが表示される（データが多い場合）
- [ ] アイコンボタンにツールチップが表示される
- [ ] レスポンシブデザインが動作する（ブラウザサイズを変更して確認）

---

## トラブルシューティング

### 問題1: バックエンドが起動しない

#### 症状
```
ModuleNotFoundError: No module named 'app'
```

#### 原因
- 仮想環境が有効化されていない
- カレントディレクトリが間違っている

#### 解決方法
```cmd
# 仮想環境を有効化
cd backend
venv\Scripts\activate

# カレントディレクトリが backend であることを確認
# main.py があることを確認
dir app\main.py

# 起動コマンドを実行
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 問題2: フロントエンドが起動しない

#### 症状
```
Error: Cannot find module 'vite'
```

#### 原因
- 依存関係がインストールされていない

#### 解決方法
```cmd
cd frontend
npm install
npm run dev
```

---

### 問題3: 顧客・商品データが表示されない

#### 症状
- 一覧画面に「顧客が見つかりませんでした」と表示される
- 一覧画面に「商品が見つかりませんでした」と表示される

#### 原因
- データベースにシードデータが投入されていない

#### 解決方法
```cmd
cd backend
venv\Scripts\activate
python scripts/seed_data.py
```

---

### 問題4: 認証エラーが発生する

#### 症状
```
401 Unauthorized
Could not validate credentials
```

#### 原因
- トークンが期限切れ
- ログインしていない

#### 解決方法
1. ブラウザで `http://localhost:3000/login` にアクセス
2. 再度ログイン
   - ユーザー名: `admin`
   - パスワード: `admin123`

---

### 問題5: CORS エラーが発生する

#### 症状
```
Access to XMLHttpRequest at 'http://localhost:8000/api/customers/'
from origin 'http://localhost:3000' has been blocked by CORS policy
```

#### 原因
- バックエンドのCORS設定が正しくない

#### 解決方法
1. `backend/app/main.py` を確認
2. CORS設定が以下のようになっているか確認:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. `backend/app/core/config.py` を確認
4. `CORS_ORIGINS` に `http://localhost:3000` が含まれているか確認

---

### 問題6: 検索機能が動作しない

#### 症状
- 検索ボックスに入力しても結果が変わらない

#### 原因
- Enterキーを押していない
- 検索アイコンをクリックしていない

#### 解決方法
1. 検索ボックスに入力後、**Enterキーを押す**
2. または、**虫眼鏡アイコンをクリック**

---

### 問題7: カテゴリフィルタに選択肢が表示されない

#### 症状
- カテゴリドロップダウンに「全て」しか表示されない

#### 原因
- 商品データにカテゴリが設定されていない
- データベースにデータが投入されていない

#### 解決方法
```cmd
cd backend
venv\Scripts\activate
python scripts/seed_data.py
```

実行後、フロントエンドをリロードして確認。

---

### 問題8: Swagger UIで認証が必要なエンドポイントが実行できない

#### 症状
```
401 Unauthorized
```

#### 原因
- Swagger UIで認証していない

#### 解決方法
1. Swagger UI (`http://localhost:8000/docs`) にアクセス
2. 右上の「Authorize」ボタンをクリック
3. まず、`POST /api/auth/login` エンドポイントでトークンを取得:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
4. レスポンスの `access_token` をコピー
5. 「Authorize」ボタンをクリック
6. `Bearer <access_token>` の形式で入力（例: `Bearer eyJ0eXAiOiJKV1QiLCJhb...`）
7. 「Authorize」をクリック

---

### 問題9: 日本語が文字化けする

#### 症状
- 顧客名や商品名が文字化けして表示される

#### 原因
- データベースの文字コード設定が間違っている
- ブラウザの文字コード設定が間違っている

#### 解決方法
1. ブラウザの開発者ツール (F12) を開く
2. Console タブでエラーがないか確認
3. Network タブでレスポンスの文字コードを確認
4. データベースを削除して再作成:
   ```cmd
   cd backend
   del trade_dx.db
   python scripts/seed_data.py
   ```

---

### 問題10: ポート番号が既に使用されている

#### 症状（バックエンド）
```
ERROR:    [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000):
通常、各ソケット アドレスに対してプロトコル、ネットワーク アドレス、またはポートのどれか 1 つのみを使用できます。
```

#### 解決方法
```cmd
# 別のポート番号を指定して起動
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### 症状（フロントエンド）
```
Port 3000 is in use, trying another one...
```

#### 解決方法
- 別のポートが使用される場合があります
- 表示されたURLにアクセスしてください

---

## 補足情報

### 未実装機能

Phase 4では以下の機能は未実装です（将来のフェーズで実装予定）:

- 顧客の新規登録・編集モーダル（現在は "開発中" アラート）
- 商品の新規登録・編集モーダル（現在は "開発中" アラート）
- 案件フォームでのマスタ連携（オートコンプリート組み込み）
  - APIは実装済み、フロントエンドの統合は未実装

### パフォーマンス最適化

大量のデータがある場合は、以下の設定を調整してください：

**ページサイズの変更**:
- デフォルト: 20件/ページ
- 変更方法: `CustomersPage.tsx` / `ProductsPage.tsx` の `pageSize` を変更

### セキュリティ注意事項

- 本番環境では、論理削除ではなく物理削除が必要な場合もあります
- 顧客・商品データは機密情報を含む可能性があるため、適切なアクセス制御を実装してください
- 本番環境では、JWTトークンの有効期限を適切に設定してください

---

## 次のステップ

Phase 4の動作確認が完了したら、以下を実施してください：

1. ✅ 確認チェックリストをすべて完了する
2. ✅ 発見した問題をトラブルシューティングセクションで解決する
3. ✅ 必要に応じてテストデータを追加する
4. ✅ Phase 5（ダッシュボード・集計機能）の準備を開始する

---

## 問い合わせ

不明な点や問題が解決しない場合は、以下の情報を添えて問い合わせてください：

1. エラーメッセージの全文
2. 実行したコマンド
3. 環境情報（OS、Pythonバージョン、Node.jsバージョン）
4. ブラウザの開発者ツールのConsoleに表示されているエラー

---

---

## ✅ 実行確認完了記録

**実行確認完了日**: 2025-11-27
**実行者**: ユーザー
**結果**: 全ての確認項目を正常に完了

### 完了した確認項目
- ✅ バックエンドAPI起動確認
- ✅ フロントエンド起動確認
- ✅ Swagger UI動作確認
- ✅ ログイン機能確認
- ✅ 顧客マスタ一覧表示確認
- ✅ 顧客マスタ検索機能確認
- ✅ 商品マスタ一覧表示確認
- ✅ 商品マスタ検索機能確認
- ✅ 商品マスタカテゴリフィルタ確認
- ✅ オートコンプリートAPI確認（顧客・商品）

### 発生した問題と解決
1. **bcrypt互換性エラー**
   - 問題: bcrypt 5.0.0とpasslib 1.7.4の互換性問題
   - 解決: bcrypt 4.0.1にダウングレード

2. **文字エンコーディングエラー**
   - 問題: Windowsコマンドプロンプトでのcp932エンコーディング
   - 解決: `chcp 65001` でUTF-8に設定

3. **Swagger UI認証**
   - 問題: 401 Unauthorizedエラー
   - 解決: username/passwordで直接認証

### 備考
- シードデータが正常に投入され、全てのテストデータが確認できた
- フロントエンドのポート番号を5173から3000に修正
- 全てのAPI機能が正常に動作することを確認

---

**Phase 4 手動操作手順書 完了**

作成日: 2025-11-25
更新日: 2025-11-27
実行確認完了日: 2025-11-27
