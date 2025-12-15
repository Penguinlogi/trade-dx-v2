# Phase 3: 案件管理API - 実装メモ

## 📅 実施日
- **開始日**: 2025-11-25
- **完了日**: 2025-11-25

## 📝 実装内容

### 1. バックエンド実装

#### 1.1 案件CRUD API (`backend/app/api/endpoints/cases.py`)

**実装済みエンドポイント:**
- `GET /api/cases` - 案件一覧取得（ページネーション、フィルター、検索対応）
- `GET /api/cases/{case_id}` - 案件詳細取得
- `POST /api/cases` - 案件作成
- `PUT /api/cases/{case_id}` - 案件更新
- `DELETE /api/cases/{case_id}` - 案件削除
- `GET /api/cases/stats/summary` - 統計情報取得

**主な機能:**
- フィルタリング（区分、ステータス、担当者）
- 検索（案件番号、顧客名、商品名）
- ページネーション
- リレーション（顧客、商品情報の取得）
- 自動計算（売上額、粗利額、粗利率）
- バリデーション（顧客・商品の存在確認、案件番号の重複確認）

#### 1.2 案件番号生成API (`backend/app/api/endpoints/case_numbers.py`)

**実装済みエンドポイント:**
- `POST /api/case-numbers/generate` - 案件番号生成
- `GET /api/case-numbers/current/{trade_type}` - 現在の連番取得

**案件番号形式:**
- `YYYY-EX-NNN` (輸出)
- `YYYY-IM-NNN` (輸入)

**特徴:**
- 年・区分ごとに独立した連番管理
- トランザクション制御（ロック機構）
- 連番上限チェック（999まで）

#### 1.3 データモデル

**案件モデル (`backend/app/models/case.py`):**
- 既存のモデルを使用
- `calculate_amounts()` メソッドで金額を自動計算

**案件番号管理モデル (`backend/app/models/case_number.py`):**
- 既存のモデルを使用
- 年・区分ごとの連番管理

#### 1.4 スキーマ (`backend/app/schemas/case.py`)

**実装済みスキーマ:**
- `CaseBase` - ベーススキーマ
- `CaseCreate` - 作成用
- `CaseUpdate` - 更新用
- `Case` - レスポンス用
- `CaseListItem` - 一覧用
- `CaseListResponse` - ページネーション付きレスポンス
- `CustomerInCase` - 顧客情報（埋め込み）
- `ProductInCase` - 商品情報（埋め込み）

**バリデーション:**
- 区分: 「輸出」「輸入」のみ許可
- ステータス: 「見積中」「受注済」「船積済」「完了」「キャンセル」のみ許可
- 数量: 1以上
- 単価: 0以上

### 2. フロントエンド実装

#### 2.1 案件一覧画面 (`frontend/src/pages/CasesPage.tsx`)

**実装機能:**
- 案件一覧表示
- 検索（キーワード）
- フィルター（区分、ステータス、担当者、日付範囲、ソート）
- ページネーション
- 案件の作成・編集・削除
- エラーハンドリング

**状態管理:**
- 案件一覧データ
- ページネーション情報
- 検索・フィルターパラメータ
- モーダル表示状態
- ローディング状態
- エラー状態

#### 2.2 案件テーブルコンポーネント (`frontend/src/components/Table/CaseTable.tsx`)

**表示項目:**
- 案件番号
- 区分（色分けチップ）
- 顧客名
- 商品名
- 数量・単位
- 売上額
- 粗利額
- 粗利率
- ステータス（色分けチップ）
- 担当者
- 船積予定日
- 操作ボタン（詳細、編集、削除）

**機能:**
- 金額のフォーマット（¥形式）
- 日付のフォーマット
- パーセンテージのフォーマット
- ステータスの色分け
- 空データ時のメッセージ表示

#### 2.3 案件フォームモーダル (`frontend/src/components/Modal/CaseFormModal.tsx`)

**モード:**
- 作成モード
- 編集モード

**入力フィールド:**
- 案件番号（任意、自動生成可能）
- 区分
- 顧客ID
- 仕入先名
- 商品ID
- 数量
- 単位
- 販売単価
- 仕入単価
- 船積予定日
- ステータス
- 担当者
- 備考

**機能:**
- 案件番号自動生成（⚡ボタン）
- フォームバリデーション
- エラー表示
- ローディング表示

#### 2.4 API クライアント

**案件API (`frontend/src/api/cases.ts`):**
- `getCases()` - 案件一覧取得
- `getCase()` - 案件詳細取得
- `createCase()` - 案件作成
- `updateCase()` - 案件更新
- `deleteCase()` - 案件削除

**案件番号API (`frontend/src/api/caseNumbers.ts`):**
- `generateCaseNumber()` - 案件番号生成
- `getCurrentSequence()` - 現在の連番取得

#### 2.5 型定義 (`frontend/src/types/case.ts`)

**定義済み型:**
- `Case` - 案件（詳細）
- `CaseListItem` - 案件一覧アイテム
- `CaseListResponse` - ページネーション付きレスポンス
- `CaseCreateRequest` - 作成リクエスト
- `CaseUpdateRequest` - 更新リクエスト
- `CaseSearchParams` - 検索パラメータ
- `CustomerInCase` - 顧客情報
- `ProductInCase` - 商品情報
- `TradeType` - 区分型
- `CaseStatus` - ステータス型

### 3. データベース

**既存のシードデータを活用:**
- ユーザー: 3件
- 顧客マスタ: 3件
- 商品マスタ: 4件
- 案件番号管理: 2件（輸出・輸入）

**テーブル:**
- `cases` - 案件データ
- `case_numbers` - 案件番号管理

### 4. 手動操作手順書

**作成済み:**
- `進捗管理/フェーズ進捗メモ/Phase3_手動操作手順書.md`

**含まれる内容:**
1. テストデータの作成方法
2. 実行前のデータ確認
3. アプリケーションの起動方法
4. 手動操作による動作確認手順
5. 実行後のデータ確認
6. 確認チェックリスト
7. トラブルシューティング
8. 次のステップ
9. 参考情報
10. 動作確認完了の報告

## ✅ 完了した項目

- [x] 案件CRUD APIの実装
- [x] フィルタリング・検索機能
- [x] ページネーション機能
- [x] 案件番号自動生成機能
- [x] 案件一覧画面の実装
- [x] データテーブルコンポーネント
- [x] 案件作成・編集モーダル
- [x] フォームバリデーション
- [x] エラーハンドリング
- [x] 統計情報API（オプション）
- [x] 手動操作手順書の作成
- [x] 全体進捗管理書の更新

## 📊 実装統計

**バックエンド:**
- 新規ファイル: 1件
  - `backend/app/api/endpoints/cases.py` (約370行)
- 既存ファイル使用: 4件
  - `backend/app/models/case.py`
  - `backend/app/schemas/case.py`
  - `backend/app/api/endpoints/case_numbers.py`
  - `backend/app/models/case_number.py`

**フロントエンド:**
- 既存ファイル使用: 7件
  - `frontend/src/pages/CasesPage.tsx` (約385行)
  - `frontend/src/components/Table/CaseTable.tsx` (約187行)
  - `frontend/src/components/Modal/CaseFormModal.tsx` (約474行)
  - `frontend/src/api/cases.ts` (約53行)
  - `frontend/src/api/caseNumbers.ts` (約40行)
  - `frontend/src/types/case.ts` (約162行)

**ドキュメント:**
- 新規ファイル: 2件
  - `進捗管理/フェーズ進捗メモ/Phase3_手動操作手順書.md` (約1200行)
  - `進捗管理/フェーズ進捗メモ/Phase3.md` (このファイル)

**合計行数:** 約2,900行

## 🎯 主な成果

1. **完全なCRUD機能**: 案件の作成・参照・更新・削除が可能
2. **高度な検索・フィルター**: 複数条件での案件検索が可能
3. **案件番号自動生成**: 年・区分ごとの連番管理
4. **リアルタイム計算**: 売上額、粗利額、粗利率の自動計算
5. **ユーザーフレンドリーなUI**: Material-UIを使用した洗練されたデザイン
6. **詳細な手順書**: 動作確認からトラブルシューティングまで網羅

## 🔍 技術的なポイント

### バックエンド

**SQLAlchemy のリレーション活用:**
```python
query = db.query(CaseModel).options(
    joinedload(CaseModel.customer),
    joinedload(CaseModel.product)
)
```
- N+1問題を回避するために `joinedload` を使用
- 案件取得時に関連する顧客・商品情報を効率的に取得

**動的フィルタリング:**
```python
filters = []
if search:
    search_filter = or_(
        CaseModel.case_number.ilike(f"%{search}%"),
        CustomerModel.customer_name.ilike(f"%{search}%"),
        ProductModel.product_name.ilike(f"%{search}%")
    )
    filters.append(search_filter)
if filters:
    query = query.filter(and_(*filters))
```
- 検索条件を動的に構築
- OR条件とAND条件の組み合わせ

**トランザクション制御（案件番号生成）:**
```python
case_number_record = db.query(CaseNumber).filter(...).with_for_update().first()
```
- `with_for_update()` で行ロックを取得
- 同時リクエストでの連番重複を防止

**自動計算:**
```python
def calculate_amounts(self):
    self.sales_amount = self.quantity * self.sales_unit_price
    total_cost = self.quantity * self.purchase_unit_price
    self.gross_profit = self.sales_amount - total_cost
    if self.sales_amount > 0:
        self.gross_profit_rate = (self.gross_profit / self.sales_amount) * 100
```
- モデルメソッドで金額を計算
- 作成・更新時に自動実行

### フロントエンド

**状態管理とURL同期:**
```typescript
const [searchParams, setSearchParams] = useState<CaseSearchParams>({
  page: 1,
  page_size: 20,
  sort_by: 'created_at',
  sort_order: 'desc',
});

useEffect(() => {
  fetchCases();
}, [searchParams]);
```
- 検索パラメータの変更を検知して自動再取得
- ページネーション、フィルター、ソートの連携

**フォームバリデーション:**
```typescript
const validate = (): boolean => {
  const newErrors: Partial<Record<keyof FormData, string>> = {};
  if (!formData.quantity || parseFloat(formData.quantity) <= 0) {
    newErrors.quantity = '数量は1以上である必要があります';
  }
  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```
- クライアント側でのバリデーション
- エラーメッセージの表示

**金額フォーマット:**
```typescript
const formatAmount = (amount?: number | null): string => {
  if (amount === undefined || amount === null) return '-';
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY',
  }).format(amount);
};
```
- 日本円形式での金額表示
- null/undefinedの適切な処理

## 🚀 パフォーマンス最適化

1. **バックエンド:**
   - JOINを使用したN+1問題の回避
   - インデックスの活用（案件番号、顧客ID、商品ID）
   - ページネーションによるデータ量の制限

2. **フロントエンド:**
   - 必要な時だけAPIリクエストを発行
   - ローディング状態の表示でUX向上
   - エラー時の適切なフィードバック

## 🔐 セキュリティ

1. **認証:**
   - すべてのAPIエンドポイントで認証が必要
   - JWTトークンによる認証

2. **バリデーション:**
   - 入力値の検証（フロントエンド・バックエンド両方）
   - SQLインジェクション対策（SQLAlchemyのパラメータバインディング）

3. **権限管理:**
   - `created_by`、`updated_by` で作成者・更新者を記録
   - 将来的な権限制御の準備

## 📈 今後の改善点

1. **マスタ連携:**
   - 顧客ID、商品IDを直接入力ではなく、選択式にする
   - オートコンプリート機能の追加

2. **詳細画面:**
   - 案件詳細を表示する専用画面の追加
   - 変更履歴の表示

3. **エクスポート:**
   - 案件一覧のCSV/Excelエクスポート機能

4. **統計情報:**
   - 統計情報の可視化（グラフ、チャート）

5. **通知:**
   - 案件作成・更新時の通知機能

## 🐛 既知の制限事項

1. **顧客・商品の選択:**
   - 現在はID入力方式
   - Phase 4でマスタ連携を実装予定

2. **案件詳細画面:**
   - 詳細表示機能は未実装
   - 編集モーダルで代用

3. **バリデーション:**
   - 一部のビジネスロジックのバリデーションが不足
   - 例: 船積予定日が過去の日付でも登録可能

## 💡 学んだこと

1. **FastAPIのパフォーマンス:**
   - SQLAlchemyの `joinedload` を使うことで、N+1問題を効果的に回避できる

2. **Reactの状態管理:**
   - 検索パラメータを状態として管理することで、フィルター・ページネーション・ソートの連携がスムーズになる

3. **Material-UIの活用:**
   - `Chip` コンポーネントで視覚的に分かりやすいステータス表示が可能
   - `Pagination` コンポーネントで簡単にページネーションを実装できる

4. **トランザクション制御:**
   - 案件番号の連番生成では、行ロックを使用することで同時実行時の競合を防げる

## 📝 次フェーズへの引き継ぎ事項

**Phase 4 (マスタ管理) への準備:**
1. 顧客マスタ・商品マスタの管理画面を実装
2. 案件フォームで顧客・商品を選択式にする
3. オートコンプリート機能の追加

**シードデータ:**
- 顧客マスタ: 3件（十分）
- 商品マスタ: 4件（十分）
- 必要に応じて追加データを作成

**API連携:**
- 顧客マスタAPI、商品マスタAPIの実装が必要
- 案件フォームで選択肢として使用

## 📚 参考資料

**公式ドキュメント:**
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- React: https://react.dev/
- Material-UI: https://mui.com/

**内部ドキュメント:**
- `docs/貿易DX_詳細設計書_v2.1_実運用強化版.docx`
- `進捗管理/全体進捗管理書.md`
- `進捗管理/フェーズ進捗メモ/Phase3_手動操作手順書.md`

---

**Phase 3 実装メモ - 終わり**
