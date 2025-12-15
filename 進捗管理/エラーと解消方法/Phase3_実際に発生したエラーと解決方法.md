# Phase 3: 案件管理API - 実際に発生したエラーと解決方法

## 📅 検証日
- **検証日**: 2025-11-25
- **検証者**: 関伸様

---

## 🐛 発生したエラーと解決方法

### エラー1: バッチファイルの文字化け

**発生日時**: 2025-11-25（Phase 3開発中）

**発生日時**: 2025-11-25

**エラー内容:**
```
'繝ｼ繧ｿ謚募・繧ｹ繧ｯ繝ｪ繝励ヨ' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

**発生状況:**
- `scripts\run_seed.bat` を実行したとき
- バッチファイルがUTF-8で保存されていたため、Windowsコマンドプロンプト（Shift-JIS）で文字化けした

**解決方法:**
1. バッチファイルを英語版に変更
   - `backend/scripts/run_seed.bat`
   - `backend/scripts/check_db.bat`
2. シンプル版バッチファイルを新規作成
   - `backend/scripts/run_seed_simple.bat`

**修正ファイル:**
- `backend/scripts/run_seed.bat` - 英語版に変更
- `backend/scripts/check_db.bat` - 英語版に変更
- `backend/scripts/run_seed_simple.bat` - 新規作成

**予防策:**
- Windowsバッチファイルには日本語を使用しない
- コメントも英語で記述する

---

### エラー2: ポート番号の誤記

**発生日時**: 2025-11-25

**エラー内容:**
- マニュアルに `http://localhost:5173` と記載
- 実際のポートは `http://localhost:3000`
- `http://localhost:5173` はページエラー
- `http://localhost:3000` は真っ白

**発生状況:**
- フロントエンドの起動後、マニュアル通りにアクセスしたがエラー
- `vite.config.ts` でポートが3000に設定されていた

**解決方法:**
1. 手順書のポート番号を3000に修正
2. README.mdも修正
3. QUICKSTART.mdを新規作成
4. バックエンドを先に起動する重要性を強調

**修正ファイル:**
- `進捗管理/フェーズ進捗メモ/Phase3_手動操作手順書.md`
- `README.md`
- `QUICKSTART.md` (新規作成)

**根本原因:**
- Viteのデフォルトポート（5173）を前提にマニュアルを作成
- 実際の設定（3000）を確認していなかった

---

### エラー3: axiosInstanceのエクスポート/インポート不一致

**発生日時**: 2025-11-25

**エラー内容:**
```
cases.ts:4  Uncaught SyntaxError: The requested module '/src/api/axios.ts' does not provide an export named 'axiosInstance' (at cases.ts:4:10)
```

**発生状況:**
- ブラウザでフロントエンドにアクセスしたとき
- `axios.ts`が`export default`を使用
- `cases.ts`と`caseNumbers.ts`が`import { }`を使用
- エクスポート形式の不一致

**解決方法:**
1. `frontend/src/api/axios.ts` を名前付きエクスポートに変更
   ```typescript
   // 変更前: export default axiosInstance;
   // 変更後: export { axiosInstance };
   ```

2. `frontend/src/api/auth.ts` のインポートを修正
   ```typescript
   // 変更前: import axiosInstance from './axios';
   // 変更後: import { axiosInstance } from './axios';
   ```

**修正ファイル:**
- `frontend/src/api/axios.ts`
- `frontend/src/api/auth.ts`

**予防策:**
- プロジェクト内でエクスポート/インポート形式を統一
- 名前付きエクスポートを優先的に使用

---

### エラー4: Decimal型の型変換エラー（rate.toFixed is not a function）

**発生日時**: 2025-11-25

**エラー内容:**
```
CaseTable.tsx:69  Uncaught TypeError: rate.toFixed is not a function
    at formatPercentage (CaseTable.tsx:69:18)
```

**発生状況:**
- 案件作成後、画面が真っ黒になった
- バックエンドから返される`Decimal`型が文字列としてシリアライズされていた
- フロントエンドのフォーマット関数が数値のみを想定

**解決方法:**
1. フォーマット関数を文字列も受け入れるように修正
   ```typescript
   const formatPercentage = (rate?: number | string | null): string => {
     if (rate === undefined || rate === null) return '-';
     const numRate = typeof rate === 'string' ? parseFloat(rate) : rate;
     if (isNaN(numRate)) return '-';
     return `${numRate.toFixed(2)}%`;
   };
   ```

2. 型定義を修正
   ```typescript
   quantity: number | string;
   sales_amount?: number | string | null;
   gross_profit?: number | string | null;
   gross_profit_rate?: number | string | null;
   ```

**修正ファイル:**
- `frontend/src/components/Table/CaseTable.tsx`
- `frontend/src/types/case.ts`

**根本原因:**
- PydanticのDecimal型がJSON化時に文字列になる
- フロントエンドが数値のみを想定していた

**予防策:**
- バックエンドのDecimal型フィールドは常に文字列として扱う
- フロントエンドで数値に変換してから処理

---

### エラー5: ソート機能が動作しない

**発生日時**: 2025-11-25

**エラー内容:**
- ソートフィールドと順序を変更しても表示結果が変わらない
- 常に`created_at`の降順でソートされる

**発生状況:**
- 「4.8 ソート機能の確認」の手順で発覚
- バックエンドAPIで`sort_by`と`sort_order`パラメータを受け取っていなかった

**解決方法:**
1. バックエンドAPIにソートパラメータを追加
   ```python
   sort_by: Optional[str] = Query("created_at", description="ソート項目"),
   sort_order: Optional[str] = Query("desc", description="ソート順（asc/desc）"),
   ```

2. 動的ソート処理を実装
   ```python
   sort_column = getattr(CaseModel, sort_by, CaseModel.created_at)
   if sort_order and sort_order.lower() == "asc":
       query = query.order_by(sort_column.asc())
   else:
       query = query.order_by(sort_column.desc())
   ```

**修正ファイル:**
- `backend/app/api/endpoints/cases.py`

**根本原因:**
- 初期実装時にソート機能を省略していた
- フロントエンドはパラメータを送信していたが、バックエンドが無視していた

**予防策:**
- APIエンドポイント設計時に全パラメータを明示的に定義
- フロントエンドとバックエンドのインターフェース仕様を事前に確認

---

### エラー6: データベース確認スクリプトで案件が表示されない

**発生日時**: 2025-11-25（Phase 3開発中）

**エラー内容:**
- `check_database.py` 実行時に案件テーブルが表示されない
- 案件番号管理までは表示されるが、案件データが表示されない

**発生状況:**
- 「5.1 データベースの確認」の手順で発覚
- スクリプトに`check_cases()`関数がなかった

**解決方法:**
1. Caseモデルをインポート
   ```python
   from app.models import User, Customer, Product, CaseNumber, Case
   ```

2. `check_cases()`関数を追加
   - 案件データを取得して表形式で表示
   - 案件番号、区分、顧客ID、商品ID、数量、ステータス、担当者を表示

3. メイン関数で`check_cases()`を呼び出し

**修正ファイル:**
- `backend/scripts/check_database.py`
- `進捗管理/フェーズ進捗メモ/Phase3_手動操作手順書.md` (期待される出力を更新)

**根本原因:**
- 初期実装時に案件テーブルの確認を実装していなかった
- Phase 1-2ではまだ案件データがなかったため気づかなかった

**予防策:**
- 新しいテーブルを追加したら、確認スクリプトも同時に更新
- 手順書の期待される出力を実際の出力と照合

---

### エラー7: customers.ts/products.tsのエクスポート不一致（追加エラー）

**発生日時**: 2025-11-25（Phase 3動作確認完了後、Phase 4準備中）

**エラー内容:**
```
Uncaught SyntaxError: The requested module '/src/api/axios.ts' does not provide an export named 'default' (at customers.ts:4:8)
```

**発生状況:**
- Phase 3の動作確認完了後、フロントエンドが再度真っ白になった
- Phase 4用に既に作成されていた`customers.ts`と`products.ts`がエラー3の修正時に見落とされていた
- これらのファイルがまだデフォルトインポート（`import apiClient from './axios'`）を使用していた

**解決方法:**
1. `frontend/src/api/customers.ts` を修正
   ```typescript
   // 変更前
   import apiClient from './axios';
   
   // 変更後
   import { axiosInstance } from './axios';
   
   // さらに、すべての apiClient を axiosInstance に置換
   ```

2. `frontend/src/api/products.ts` を修正
   ```typescript
   // 変更前
   import apiClient from './axios';
   
   // 変更後
   import { axiosInstance } from './axios';
   
   // さらに、すべての apiClient を axiosInstance に置換
   ```

**修正ファイル:**
- `frontend/src/api/customers.ts`
- `frontend/src/api/products.ts`

**根本原因:**
- Phase 4用のファイルが先に作成されていたため、Phase 3での修正時に見落とされた
- プロジェクト全体のファイルを確認せず、現在使用中のファイルのみを修正した

**予防策:**
- 全APIファイルを一括検索して確認
  ```bash
  grep -r "import .* from './axios'" frontend/src/api/
  ```
- プロジェクト全体でコーディング規約を統一
- 新しいファイルを作成する際は、既存の統一されたパターンを使用
- エクスポート/インポートの形式を決めたら、プロジェクト全体で徹底

**教訓:**
- **部分的な修正は危険**: 同じ問題が他のファイルにも存在する可能性を常に考慮
- **先行実装の確認**: 次のフェーズ用のファイルが既に存在する場合、それも修正対象に含める
- **検索ツールの活用**: grepやIDEの検索機能で、同じパターンを持つファイルをすべて洗い出す

---

## 📊 エラー統計（更新版）

### エラー分類

| 分類 | 件数 | 割合 |
|------|------|------|
| 環境・設定エラー | 2 | 29% |
| インターフェースエラー | 3 | 43% |
| データ型エラー | 1 | 14% |
| 機能未実装 | 1 | 14% |

### 重要度別

| 重要度 | 件数 | 内容 |
|--------|------|------|
| 高 | 4 | エラー3, 4, 5, 7（機能が動作しない） |
| 中 | 2 | エラー1, 2（マニュアル・環境の問題） |
| 低 | 1 | エラー6（確認スクリプトの問題） |

### 影響範囲

| 影響 | 件数 | 内容 |
|------|------|------|
| バックエンド | 2 | エラー5, 6 |
| フロントエンド | 3 | エラー3, 4, 7 |
| ドキュメント | 2 | エラー1, 2 |

---

## 💡 学んだこと

### 1. 文字コードの重要性
- Windowsバッチファイルは日本語を使用しない
- 英語で記述するか、PowerShellスクリプトを使用

### 2. ポート番号の確認
- 設定ファイル（vite.config.ts）を確認してからドキュメントを作成
- デフォルト値を前提にしない

### 3. エクスポート/インポートの統一（重要）
- プロジェクト全体でエクスポート形式を統一
- 名前付きエクスポートを優先（`export { }`）
- **修正時は全ファイルを確認**: 部分的な修正は危険
- grepやIDEの検索機能で同じパターンを持つファイルをすべて洗い出す

### 4. バックエンドとフロントエンドの型の不一致
- DecimalやDateなどの特殊型は文字列として扱う
- フロントエンドで型変換を行う

### 5. API仕様の完全性
- フロントエンドが送信するパラメータは全てバックエンドで受け取る
- 使用しないパラメータでも明示的に定義

### 6. 段階的な実装の落とし穴
- 機能追加時は関連するスクリプト・ドキュメントも更新
- チェックリストで漏れを防ぐ

---

## 🎯 今後の改善策

### コーディング規約
1. **エクスポート形式の統一**
   - 名前付きエクスポート（`export { }`）を使用
   - デフォルトエクスポートは避ける

2. **型定義の厳密化**
   - バックエンドから返されるDecimal型は`number | string`で定義
   - フロントエンドで型変換関数を用意

3. **バッチファイルの作成ルール**
   - 日本語を使用しない
   - または、PowerShellスクリプト（.ps1）を使用

### テスト・検証
1. **手順書作成前の確認**
   - 実際の動作環境で全手順を実行
   - ポート番号や設定値を実測

2. **エラーハンドリングの強化**
   - nullチェックを徹底
   - 型変換時のエラーハンドリング

3. **統合テストの実施**
   - バックエンドとフロントエンドの連携テスト
   - 実際のデータでE2Eテスト

### ドキュメント
1. **トラブルシューティングの充実**
   - 実際に発生したエラーを記録
   - 解決方法を詳細に記載

2. **クイックスタートガイドの作成**
   - 最速で起動する方法
   - よくあるエラーの回避方法

3. **API仕様書の完全性**
   - 全パラメータを文書化
   - レスポンス型を明示

---

## 📝 チェックリスト（次回以降）

### 実装前
- [ ] API仕様を完全に定義（リクエスト・レスポンス）
- [ ] 型定義を先に作成
- [ ] エクスポート形式を統一

### 実装中
- [ ] バックエンドとフロントエンドの型の整合性を確認
- [ ] nullableなフィールドの処理を実装
- [ ] 文字列→数値変換のエラーハンドリング

### 実装後
- [ ] 手順書を実際に実行して確認
- [ ] 各種スクリプトの動作確認
- [ ] エラーケースのテスト

### ドキュメント
- [ ] 実際の設定値（ポート番号等）を確認
- [ ] スクリーンショットを撮影
- [ ] トラブルシューティングを充実

---

## 🔗 関連ドキュメント

- **手動操作手順書**: `進捗管理/フェーズ進捗メモ/Phase3_手動操作手順書.md`
- **実装メモ**: `進捗管理/フェーズ進捗メモ/Phase3.md`
- **全体進捗管理書**: `進捗管理/全体進捗管理書.md`
- **クイックスタート**: `QUICKSTART.md`

---

**Phase 3 エラー記録 - 終わり**

**記録日**: 2025-11-25  
**最終更新**: 2025-11-25  
**記録者**: AI開発アシスタント  
**総エラー数**: 7件  
**ステータス**: すべてのエラーが解決済み

---

## 📝 記録方法について

**現在の記録方法:**
- エラー発生時に手動で記録（AIアシスタントが記録）
- 会話の中で解決したエラーを後から整理してファイルに追記

**今後の改善案:**
- 各エラーを解決した直後に記録を更新
- エラー番号を採番して追跡しやすくする


