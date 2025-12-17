# フロントエンド コーディング規約

## 目次
1. [はじめに](#はじめに)
2. [TypeScript/JavaScript](#typescriptjavascript)
3. [React コンポーネント](#react-コンポーネント)
4. [API クライアント](#api-クライアント)
5. [スタイリング](#スタイリング)
6. [ファイル・ディレクトリ構造](#ファイルディレクトリ構造)
7. [命名規則](#命名規則)
8. [コメント](#コメント)

---

## はじめに

このドキュメントは、貿易DX管理システムのフロントエンド開発における統一されたコーディングスタイルを定義します。すべての開発者はこの規約に従ってコードを記述してください。

---

## TypeScript/JavaScript

### 基本ルール

#### 1. TypeScript を使用する
すべての新規ファイルは `.ts` または `.tsx` 拡張子を使用してください。

```typescript
// ✅ 正しい
export const fetchData = async (): Promise<Data[]> => {
  // ...
};

// ❌ 間違い（型定義なし）
export const fetchData = async () => {
  // ...
};
```

#### 2. strict モードを有効にする
`tsconfig.json` で strict モードを有効にし、型安全性を確保してください。

#### 3. any型の使用を避ける
やむを得ない場合を除き、`any` 型の使用は避けてください。

```typescript
// ✅ 正しい
const handleResponse = (data: UserData) => { /* ... */ };

// ❌ 間違い
const handleResponse = (data: any) => { /* ... */ };
```

#### 4. Optional Chaining を使用する
```typescript
// ✅ 正しい
const userName = user?.profile?.name;

// ❌ 間違い
const userName = user && user.profile && user.profile.name;
```

#### 5. Nullish Coalescing を使用する
```typescript
// ✅ 正しい
const displayName = name ?? 'Unknown';

// ❌ 間違い
const displayName = name || 'Unknown'; // 空文字列でも 'Unknown' になってしまう
```

---

## React コンポーネント

### コンポーネントの基本

#### 1. 関数コンポーネントを使用する
クラスコンポーネントではなく、関数コンポーネントを使用してください。

```typescript
// ✅ 正しい
export const UserProfile: React.FC<UserProfileProps> = ({ user }) => {
  return <div>{user.name}</div>;
};

// ❌ 間違い（クラスコンポーネント）
class UserProfile extends React.Component {
  // ...
}
```

#### 2. Props に型定義を付ける
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false,
  variant = 'primary'
}) => {
  // ...
};
```

#### 3. useState の型を明示する
```typescript
// ✅ 正しい
const [user, setUser] = useState<User | null>(null);
const [count, setCount] = useState<number>(0);

// ⚠️ 注意（型推論に頼る場合）
const [count, setCount] = useState(0); // number と推論される
```

#### 4. useEffect の依存配列を正しく指定する
```typescript
// ✅ 正しい
useEffect(() => {
  fetchData(userId);
}, [userId]);

// ❌ 間違い（依存配列が不足）
useEffect(() => {
  fetchData(userId);
}, []); // ESLint 警告が出る
```

#### 5. カスタムフックを活用する
ロジックを再利用可能にするため、カスタムフックを作成してください。

```typescript
// hooks/useUser.ts
export const useUser = (userId: number) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);

  return { user, loading };
};
```

---

## API クライアント

### 必須ルール

#### 1. axiosInstance を使用する
すべてのAPIファイルで `axiosInstance` を使用すること。他の名前（`apiClient`、`client` など）は使用しないでください。

```typescript
// ✅ 正しい
import { axiosInstance } from './axios';

export const getUsers = async (): Promise<User[]> => {
  const response = await axiosInstance.get<User[]>('/api/users');
  return response.data;
};

// ❌ 間違い
import { apiClient } from './axios'; // 存在しない
```

#### 2. API パスには /api プレフィックスを付ける
すべてのAPIエンドポイントには `/api` プレフィックスを付けてください。

```typescript
// ✅ 正しい
axiosInstance.get('/api/cases')
axiosInstance.post('/api/documents/invoice')

// ❌ 間違い
axiosInstance.get('/cases')
axiosInstance.post('/documents/invoice')
```

#### 3. endpoints.ts を使用する（推奨）
APIパスは `endpoints.ts` で一元管理してください。

```typescript
// ✅ 正しい
import { ENDPOINTS } from './endpoints';

export const getUsers = async () => {
  const response = await axiosInstance.get(ENDPOINTS.USERS.LIST);
  return response.data;
};

// ⚠️ 許容（小規模な場合）
export const getUsers = async () => {
  const response = await axiosInstance.get('/api/users');
  return response.data;
};
```

#### 4. レスポンスに型を付ける
```typescript
// ✅ 正しい
export const getUser = async (id: number): Promise<User> => {
  const response = await axiosInstance.get<User>(`/api/users/${id}`);
  return response.data;
};

// ❌ 間違い（型なし）
export const getUser = async (id: number) => {
  const response = await axiosInstance.get(`/api/users/${id}`);
  return response.data;
};
```

#### 5. エラーハンドリングを実装する
```typescript
// ✅ 正しい
export const deleteUser = async (id: number): Promise<void> => {
  try {
    await axiosInstance.delete(`/api/users/${id}`);
  } catch (error) {
    console.error('User deletion failed:', error);
    throw error;
  }
};
```

#### 6. 新しいAPIファイルはテンプレートを使用する
`src/api/_template.ts` をコピーして新しいAPIファイルを作成してください。

---

## スタイリング

### Material-UI (MUI) の使用

#### 1. sx prop を使用する
インラインスタイルには `sx` prop を使用してください。

```typescript
// ✅ 正しい
<Box sx={{ p: 2, mt: 3, bgcolor: 'primary.main' }}>
  Content
</Box>

// ❌ 間違い
<Box style={{ padding: '16px', marginTop: '24px' }}>
  Content
</Box>
```

#### 2. テーマを活用する
カラー、スペーシング、ブレークポイントはテーマから取得してください。

```typescript
// ✅ 正しい
sx={{ color: 'primary.main', spacing: 2 }}

// ❌ 間違い
sx={{ color: '#667eea', spacing: '16px' }}
```

#### 3. レスポンシブデザイン
```typescript
// ✅ 正しい
<Grid container spacing={2}>
  <Grid item xs={12} md={6} lg={4}>
    <Card>...</Card>
  </Grid>
</Grid>
```

---

## ファイル・ディレクトリ構造

### ディレクトリ構造

```
frontend/src/
├── api/              # API クライアント
│   ├── axios.ts      # Axios 設定
│   ├── endpoints.ts  # エンドポイント定義
│   ├── _template.ts  # APIファイルテンプレート
│   ├── auth.ts
│   ├── cases.ts
│   └── ...
├── components/       # 再利用可能なコンポーネント
│   ├── Dashboard/
│   ├── Form/
│   ├── Layout/
│   ├── Modal/
│   └── Table/
├── pages/            # ページコンポーネント
│   ├── DashboardPage.tsx
│   ├── CasesPage.tsx
│   └── ...
├── hooks/            # カスタムフック
│   ├── useAuth.ts
│   └── ...
├── context/          # React Context
│   ├── AuthContext.tsx
│   └── ...
├── types/            # 型定義
│   ├── auth.ts
│   ├── case.ts
│   └── ...
├── utils/            # ユーティリティ関数
│   └── ...
├── App.tsx           # メインアプリ
└── main.tsx          # エントリーポイント
```

### ファイル命名規則

#### コンポーネント
- PascalCase を使用
- 例: `UserProfile.tsx`, `CaseTable.tsx`

#### API ファイル
- camelCase を使用
- 例: `auth.ts`, `cases.ts`, `caseNumbers.ts`

#### 型定義ファイル
- camelCase を使用
- 例: `user.ts`, `case.ts`

#### ユーティリティ
- camelCase を使用
- 例: `formatDate.ts`, `validation.ts`

---

## 命名規則

### 変数・関数

```typescript
// ✅ 正しい
const userName = 'John';
const isActive = true;
const getUserData = () => { /* ... */ };
const handleSubmit = () => { /* ... */ };

// ❌ 間違い
const user_name = 'John';  // snake_case
const UserName = 'John';   // PascalCase (変数には不適切)
const get_user_data = () => { /* ... */ };  // snake_case
```

### 定数

```typescript
// ✅ 正しい
const MAX_ITEMS = 100;
const API_BASE_URL = 'http://localhost:8000';

// ⚠️ 許容（定数オブジェクト）
const ENDPOINTS = {
  USERS: '/api/users',
  POSTS: '/api/posts',
};
```

### Boolean 変数

```typescript
// ✅ 正しい
const isLoading = true;
const hasPermission = false;
const canEdit = true;
const shouldUpdate = false;

// ❌ 間違い
const loading = true;  // is/has/can などのプレフィックスなし
const permission = false;
```

### イベントハンドラ

```typescript
// ✅ 正しい
const handleClick = () => { /* ... */ };
const handleSubmit = () => { /* ... */ };
const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => { /* ... */ };

// ❌ 間違い
const onClick = () => { /* ... */ };  // on はpropsに使用
const submit = () => { /* ... */ };
```

### Props のイベントハンドラ

```typescript
// ✅ 正しい
interface ButtonProps {
  onClick: () => void;
  onSubmit: () => void;
}

// コンポーネント内では handle を使用
const Button: React.FC<ButtonProps> = ({ onClick }) => {
  const handleClick = () => {
    // 追加の処理
    onClick();
  };

  return <button onClick={handleClick}>Submit</button>;
};
```

---

## コメント

### JSDoc コメント

#### 関数・クラス
```typescript
/**
 * ユーザー情報を取得する
 *
 * @param userId - ユーザーID
 * @returns ユーザー情報
 * @throws {Error} ユーザーが見つからない場合
 */
export const getUser = async (userId: number): Promise<User> => {
  // ...
};
```

#### インターフェース
```typescript
/**
 * ユーザー情報
 */
interface User {
  /** ユーザーID */
  id: number;
  /** ユーザー名 */
  name: string;
  /** メールアドレス */
  email: string;
}
```

### インラインコメント

```typescript
// ✅ 正しい（必要な場合のみ）
// NOTE: この処理は IE11 対応のため必要
const isSupported = !!window.fetch;

// FIXME: パフォーマンス改善が必要
const result = slowFunction();

// TODO: エラーハンドリングを追加
fetchData();

// ❌ 間違い（自明なコメント）
// ユーザー名を取得
const name = user.name;
```

---

## チェックリスト

新しいコードを書く前に、以下を確認してください：

### 開発前
- [ ] 既存の同じ種類のファイルを確認した
- [ ] テンプレートファイルを使用した（該当する場合）
- [ ] 命名規則を確認した

### 開発中
- [ ] TypeScript の型を正しく定義した
- [ ] axiosInstance を使用した（API ファイル）
- [ ] `/api` プレフィックスを付けた（API パス）
- [ ] エラーハンドリングを実装した
- [ ] コンポーネントの Props に型を付けた

### 開発後
- [ ] `npm run type-check` を実行してエラーがない
- [ ] `npm run lint` を実行してエラーがない
- [ ] ブラウザのコンソールにエラーがない
- [ ] 不要な console.log を削除した
- [ ] コメントを追加した（必要な場合）

---

## 参考リンク

- [TypeScript 公式ドキュメント](https://www.typescriptlang.org/docs/)
- [React 公式ドキュメント](https://react.dev/)
- [Material-UI 公式ドキュメント](https://mui.com/)
- [Axios 公式ドキュメント](https://axios-http.com/)
- [ESLint Rules](https://eslint.org/docs/latest/rules/)

---

**作成日**: 2025-11-27
**最終更新**: 2025-11-27
**バージョン**: 1.0.0









