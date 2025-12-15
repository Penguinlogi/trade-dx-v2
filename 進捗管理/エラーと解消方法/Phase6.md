# Phase 6 エラーと解消方法

## エラー履歴

---

## [エラーID: 6-002] [2025-11-27]

### エラー発生箇所
- ファイル: `backend/app/services/document_generator.py`
- 行番号: 114, 115, 134, 111, 262

### エラー内容
```
Parse error: no such column: total_amount
```

### エラーの原因
- データベースのcasesテーブルには`total_amount`と`unit_price`カラムが存在しない
- 実際のカラム名は`sales_amount`と`sales_unit_price`
- また、productテーブルのカラム名は`name`ではなく`product_name`
- document_generator.pyで誤ったカラム名を参照していた

### 影響範囲
- 影響を受けるファイル: `backend/app/services/document_generator.py`
- 影響を受ける機能: Invoice生成、Packing List生成

### 解消方法

#### 修正箇所
```python
# 修正前
case.unit_price
case.total_amount
product.name

# 修正後
case.sales_unit_price
case.sales_amount
product.product_name
```

#### 実際の修正内容
```diff
# backend/app/services/document_generator.py

# Invoice生成の明細データ
- ws.cell(row=detail_row, column=6).value = case.unit_price
+ ws.cell(row=detail_row, column=6).value = case.sales_unit_price

- ws.cell(row=detail_row, column=7).value = case.total_amount
+ ws.cell(row=detail_row, column=7).value = case.sales_amount

# Invoice生成の合計
- ws.cell(row=total_row, column=7).value = case.total_amount
+ ws.cell(row=total_row, column=7).value = case.sales_amount

# 商品名（Invoice & Packing List）
- ws.cell(row=detail_row, column=3).value = product.name if product else ""
+ ws.cell(row=detail_row, column=3).value = product.product_name if product else ""
```

### 検証結果
- バックエンド再起動後、Invoice生成・Packing List生成が正常に動作
- Excelファイルに単価・金額・商品名が正しく表示される

### 再発防止策
1. **モデル定義を確認する**
   - 新しい機能を実装する前に、モデルファイル（`app/models/`）を確認
   - 実際のカラム名を確認してからコーディング

2. **型ヒントを活用する**
   - IDEの補完機能を使えば、存在しないカラムを参照するとエラーが表示される

3. **早期テスト**
   - コードを書いた直後に簡単なテストを実行
   - データベースエラーは実行時まで検出されないため、早めの確認が重要

4. **データベーススキーマドキュメントの作成**
   - 各テーブルのカラム一覧をドキュメント化する

---

## [エラーID: 6-001] [2025-11-27]

### エラー発生箇所
- ファイル: `frontend/src/api/documents.ts`
- 行番号: 4

### エラー内容
```
documents.ts:4  Uncaught SyntaxError: The requested module '/src/api/axios.ts' does not provide an export named 'apiClient' (at documents.ts:4:10)
```

### エラーの原因
- `axios.ts` では `axiosInstance` という名前でエクスポートしている
- `documents.ts` では `apiClient` という名前でインポートしようとした
- インポート名の不一致により、モジュールが見つからないエラーが発生

### 影響範囲
- 影響を受けるファイル: `frontend/src/api/documents.ts`
- 影響を受ける機能: ドキュメント生成機能全体（Invoice、Packing List生成、履歴表示）

### 解消方法

#### 1. `documents.ts` のインポート名を修正
```typescript
// 修正前
import { apiClient } from './axios';

// 修正後
import { axiosInstance } from './axios';
```

#### 2. すべてのAPI呼び出しを修正
```typescript
// 修正前
const response = await apiClient.post<Document>('/documents/invoice', ...);

// 修正後
const response = await axiosInstance.post<Document>('/api/documents/invoice', ...);
```

#### 3. URLパスにも `/api` プレフィックスを追加
- `/documents/...` → `/api/documents/...`

### 修正内容
```diff
# frontend/src/api/documents.ts

- import { apiClient } from './axios';
+ import { axiosInstance } from './axios';

- const response = await apiClient.post<Document>('/documents/invoice', {
+ const response = await axiosInstance.post<Document>('/api/documents/invoice', {

- const response = await apiClient.post<Document>('/documents/packing-list', {
+ const response = await axiosInstance.post<Document>('/api/documents/packing-list', {

- const response = await apiClient.get<DocumentListResponse>('/documents', {
+ const response = await axiosInstance.get<DocumentListResponse>('/api/documents', {

- const response = await apiClient.get(`/documents/${documentId}/download`, {
+ const response = await axiosInstance.get(`/api/documents/${documentId}/download`, {
```

### 検証結果
- ブラウザを再読み込み後、エラーが解消される
- ドキュメント生成機能が正常に動作する

### 再発防止策
1. **コーディング規約の策定**
2. **TypeScript型チェックの強化**
3. **ESLint ルールの追加**
4. **開発テンプレートの作成**

詳細は下記参照。

---

## 根本的な解決策

### 問題の本質
フロントエンドで頻繁にエラーが発生する主な原因:

1. **名前の不統一**: インポート/エクスポート名が統一されていない
2. **型チェック不足**: TypeScriptの型チェックが実行時まで検出できない
3. **パス指定ミス**: API URLパスのプレフィックス忘れ
4. **開発環境の問題**: ホットリロードが正しく動作しない場合がある

---

## 解決策1: コーディング規約の策定

### API クライアントの命名規則

**ファイル**: `frontend/CODING_STANDARDS.md` (新規作成推奨)

```markdown
## API クライアントの使用方法

### 1. axiosInstance の使用
すべてのAPIファイルで `axiosInstance` を使用すること。

```typescript
// ✅ 正しい
import { axiosInstance } from './axios';

// ❌ 間違い
import { apiClient } from './axios';
import { client } from './axios';
```

### 2. API パスのプレフィックス
すべてのAPIエンドポイントには `/api` プレフィックスを付けること。

```typescript
// ✅ 正しい
axiosInstance.get('/api/cases')
axiosInstance.post('/api/documents/invoice')

// ❌ 間違い
axiosInstance.get('/cases')
axiosInstance.post('/documents/invoice')
```
```

---

## 解決策2: TypeScript型チェックの強化

### tsconfig.json の厳格化

**ファイル**: `frontend/tsconfig.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "allowSyntheticDefaultImports": true
  }
}
```

### 型定義ファイルの作成

**ファイル**: `frontend/src/types/api.ts` (新規作成推奨)

```typescript
/**
 * API クライアントの型定義
 */
import { AxiosInstance } from 'axios';

// axiosInstance の型をエクスポート
export type ApiClient = AxiosInstance;
```

---

## 解決策3: ESLint ルールの追加

### .eslintrc.json の設定

**ファイル**: `frontend/.eslintrc.json` (既存ファイルに追加)

```json
{
  "rules": {
    "import/no-unresolved": "error",
    "import/named": "error",
    "no-unused-vars": "error",
    "@typescript-eslint/no-unused-vars": "error"
  },
  "settings": {
    "import/resolver": {
      "typescript": {}
    }
  }
}
```

### 必要なパッケージ

```bash
cd frontend
npm install --save-dev eslint-import-resolver-typescript
```

---

## 解決策4: 開発テンプレートの作成

### API ファイルのテンプレート

**ファイル**: `frontend/src/api/_template.ts` (新規作成推奨)

```typescript
/**
 * [機能名] API
 *
 * このテンプレートをコピーして新しいAPIファイルを作成してください
 */
import { axiosInstance } from './axios';

// 型定義
export interface YourDataType {
  id: number;
  name: string;
}

// 一覧取得
export const getItems = async (): Promise<YourDataType[]> => {
  const response = await axiosInstance.get<YourDataType[]>('/api/your-endpoint');
  return response.data;
};

// 詳細取得
export const getItem = async (id: number): Promise<YourDataType> => {
  const response = await axiosInstance.get<YourDataType>(`/api/your-endpoint/${id}`);
  return response.data;
};

// 作成
export const createItem = async (data: Omit<YourDataType, 'id'>): Promise<YourDataType> => {
  const response = await axiosInstance.post<YourDataType>('/api/your-endpoint', data);
  return response.data;
};

// 更新
export const updateItem = async (id: number, data: Partial<YourDataType>): Promise<YourDataType> => {
  const response = await axiosInstance.put<YourDataType>(`/api/your-endpoint/${id}`, data);
  return response.data;
};

// 削除
export const deleteItem = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/your-endpoint/${id}`);
};
```

---

## 解決策5: ビルド時チェックの追加

### package.json にスクリプト追加

**ファイル**: `frontend/package.json`

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit",
    "preview": "vite preview",
    "check-all": "npm run type-check && npm run lint"
  }
}
```

### 使用方法

```bash
# 開発前に型チェック＆リント実行
npm run check-all

# 型チェックのみ
npm run type-check

# リントのみ
npm run lint
```

---

## 解決策6: Pre-commit フックの設定

### Husky のインストール

```bash
cd frontend
npm install --save-dev husky lint-staged
npx husky install
```

### .husky/pre-commit の作成

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

cd frontend
npm run type-check
npm run lint
```

### package.json に lint-staged 設定追加

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

---

## 解決策7: 統合開発環境の設定

### VS Code 設定

**ファイル**: `.vscode/settings.json` (プロジェクトルート)

```json
{
  "typescript.tsdk": "frontend/node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.workingDirectories": ["frontend"],
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### VS Code 拡張機能（推奨）

1. **ESLint** (dbaeumer.vscode-eslint)
2. **Prettier** (esbenp.prettier-vscode)
3. **TypeScript Vue Plugin (Volar)** (Vue.vscode-typescript-vue-plugin)
4. **Error Lens** (usernamehw.errorlens) - エラーをインラインで表示

---

## 解決策8: API エンドポイント一覧の管理

### api/endpoints.ts の作成

**ファイル**: `frontend/src/api/endpoints.ts` (新規作成推奨)

```typescript
/**
 * API エンドポイント定義
 *
 * すべてのAPIパスを一元管理
 */

const API_PREFIX = '/api';

export const ENDPOINTS = {
  // 認証
  AUTH: {
    LOGIN: `${API_PREFIX}/auth/login`,
    LOGOUT: `${API_PREFIX}/auth/logout`,
    ME: `${API_PREFIX}/auth/me`,
    REFRESH: `${API_PREFIX}/auth/refresh`,
  },

  // 案件
  CASES: {
    LIST: `${API_PREFIX}/cases`,
    DETAIL: (id: number) => `${API_PREFIX}/cases/${id}`,
    CREATE: `${API_PREFIX}/cases`,
    UPDATE: (id: number) => `${API_PREFIX}/cases/${id}`,
    DELETE: (id: number) => `${API_PREFIX}/cases/${id}`,
  },

  // ドキュメント
  DOCUMENTS: {
    LIST: `${API_PREFIX}/documents`,
    INVOICE: `${API_PREFIX}/documents/invoice`,
    PACKING_LIST: `${API_PREFIX}/documents/packing-list`,
    DOWNLOAD: (id: number) => `${API_PREFIX}/documents/${id}/download`,
  },

  // 顧客
  CUSTOMERS: {
    LIST: `${API_PREFIX}/customers`,
    DETAIL: (id: number) => `${API_PREFIX}/customers/${id}`,
  },

  // 商品
  PRODUCTS: {
    LIST: `${API_PREFIX}/products`,
    DETAIL: (id: number) => `${API_PREFIX}/products/${id}`,
  },

  // 分析
  ANALYTICS: {
    SUMMARY: `${API_PREFIX}/analytics/summary`,
    TRENDS: `${API_PREFIX}/analytics/trends`,
    BY_CUSTOMER: `${API_PREFIX}/analytics/by-customer`,
  },
} as const;
```

### 使用例

```typescript
// documents.ts
import { axiosInstance } from './axios';
import { ENDPOINTS } from './endpoints';

export const generateInvoice = async (caseId: number) => {
  const response = await axiosInstance.post(ENDPOINTS.DOCUMENTS.INVOICE, {
    case_id: caseId,
    document_type: 'invoice',
  });
  return response.data;
};
```

---

## 推奨する実施順序

### 即座に実施（5分）
1. ✅ `documents.ts` の修正（完了）
2. ブラウザで動作確認

### 短期対応（30分）
1. コーディング規約ドキュメント作成
2. API エンドポイント一覧ファイル作成
3. 既存のAPIファイルをエンドポイント一覧を使うように修正

### 中期対応（1-2時間）
1. ESLint 設定強化
2. TypeScript 型チェック強化
3. VS Code 設定追加
4. API テンプレート作成

### 長期対応（今後のフェーズで）
1. Pre-commit フック設定
2. CI/CD パイプライン追加
3. 自動テスト追加

---

## まとめ

### このエラーが起きた理由
- 新しいファイル作成時に既存のパターンを確認せずにコーディングした
- TypeScriptの型チェックが不十分
- 統一されたコーディング規約がない

### 今後の予防策
1. **新しいファイルを作成する前に、既存の同じ種類のファイルを確認する**
2. **テンプレートファイルを使用する**
3. **コミット前に `npm run check-all` を実行する**
4. **VS Code の ESLint/Prettier 拡張機能を有効にする**

---

**作成日**: 2025-11-27
**最終更新**: 2025-11-27
