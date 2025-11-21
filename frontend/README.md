# 貿易DX管理システム - フロントエンド

React + TypeScript + Vite を使用したフロントエンドアプリケーション

## 技術スタック

- **React**: 18.2
- **TypeScript**: 5.2
- **Vite**: 5.0
- **UI ライブラリ**: Material-UI (MUI) 5.14
- **状態管理**: React Query (TanStack Query) 5.8
- **テーブル**: TanStack Table 8.10
- **フォーム**: React Hook Form 7.48 + Zod 3.22
- **HTTP クライアント**: Axios 1.6
- **グラフ**: Recharts 2.10

## セットアップ

### 1. 依存パッケージのインストール

```bash
npm install
```

### 2. 開発サーバーの起動

```bash
npm run dev
```

アプリケーションは `http://localhost:3000` で起動します。

## スクリプト

- `npm run dev` - 開発サーバーを起動
- `npm run build` - プロダクションビルドを作成
- `npm run lint` - ESLintでコードをチェック
- `npm run preview` - ビルド結果をプレビュー

## ディレクトリ構造

```
frontend/
├── public/               # 静的ファイル
├── src/
│   ├── api/              # APIクライアント
│   ├── components/       # 共通コンポーネント
│   │   ├── Layout/       # レイアウトコンポーネント
│   │   ├── Table/        # テーブルコンポーネント
│   │   ├── Form/         # フォームコンポーネント
│   │   └── Modal/        # モーダルコンポーネント
│   ├── pages/            # ページコンポーネント
│   ├── hooks/            # カスタムフック
│   ├── context/          # Reactコンテキスト
│   ├── types/            # TypeScript型定義
│   ├── utils/            # ユーティリティ関数
│   ├── App.tsx           # メインアプリケーション
│   └── main.tsx          # エントリーポイント
├── index.html            # HTMLテンプレート
├── package.json          # 依存関係
├── tsconfig.json         # TypeScript設定
└── vite.config.ts        # Vite設定
```

## 開発ガイドライン

### コンポーネント作成

- Functional Component + Hooks を使用
- TypeScriptで型安全性を確保
- Material-UIコンポーネントを活用

### 状態管理

- サーバー状態: React Query を使用
- ローカル状態: useState / useReducer
- グローバル状態: Context API

### スタイリング

- Material-UI の sx prop を優先
- テーマは theme.ts で一元管理
- レスポンシブデザインを考慮

## API連携

バックエンドAPI（http://localhost:8000）とViteのプロキシ機能で連携します。

```typescript
// /api/* へのリクエストは自動的にバックエンドにプロキシされます
axios.get('/api/cases')  // → http://localhost:8000/api/cases
```

