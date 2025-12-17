# TESTUSERログイン問題の解決方法

## 問題

TESTUSERでログインしようとすると、401 Unauthorizedエラーが発生し、「ユーザー名またはパスワードが正しくありません」というメッセージが表示されます。

## 原因

TESTUSERが本番環境のデータベースに存在しない可能性があります。シードデータ（`seed_data.py`）には、以下のユーザーしか含まれていません：
- `admin` / `admin123`
- `yamada` / `yamada123`
- `suzuki` / `suzuki123`

`testuser`は別途`add_testuser.py`スクリプトで作成する必要があります。

## 解決方法

### 方法1: Render.com Shellでtestuserを作成（推奨）

1. **Render.comダッシュボードにログイン**
   - https://dashboard.render.com/ にアクセス

2. **バックエンドサービスを開く**
   - 「Web Services」→ `trade-dx-v2` をクリック

3. **Shellタブを開く**
   - 上部の「Shell」タブをクリック

4. **testuser作成スクリプトを実行**
   ```bash
   cd backend
   python scripts/add_testuser.py
   ```

5. **実行結果を確認**
   - `[OK] testuser を作成しました` と表示されれば成功
   - `[OK] testuser は既に存在します` と表示された場合は、既に存在している

### 方法2: 既存のユーザーでログイン

TESTUSERが存在しない場合は、以下のユーザーでログインできます：

| ユーザー名 | パスワード | 説明 |
|----------|----------|------|
| `admin` | `admin123` | 管理者（スーパーユーザー） |
| `yamada` | `yamada123` | 一般ユーザー（山田太郎） |
| `suzuki` | `suzuki123` | 一般ユーザー（鈴木花子） |

### 方法3: シードデータにtestuserを追加（将来的な改善）

`backend/scripts/seed_data.py`の`seed_users`関数に、testuserを追加することで、今後は自動的に作成されるようにできます。

## testuserのログイン情報

`add_testuser.py`スクリプトで作成されるtestuserの情報：

- **ユーザー名**: `testuser`（小文字）
- **パスワード**: `testpass123`
- **メール**: `testuser@example.com`
- **フルネーム**: テストユーザー

**注意**: ユーザー名は大文字小文字を区別します。`TESTUSER`ではなく、`testuser`（小文字）でログインしてください。

## 確認方法

### testuserが存在するか確認

Render.com Shellで以下のコマンドを実行：

```bash
cd backend
python scripts/check_users.py
```

このスクリプトは、データベース内の全ユーザーを表示し、testuserが存在するかどうかを確認します。

## トラブルシューティング

### testuserを作成してもログインできない場合

1. **ユーザー名の大文字小文字を確認**
   - `testuser`（小文字）で入力してください
   - `TESTUSER`（大文字）ではログインできません

2. **パスワードを確認**
   - パスワード: `testpass123`
   - スペースが含まれていないか確認

3. **ブラウザのキャッシュをクリア**
   - Ctrl+Shift+Delete（Windows/Linux）
   - Cmd+Shift+Delete（Mac）

4. **シークレットモードで試す**
   - Ctrl+Shift+N（Chrome/Edge）
   - Ctrl+Shift+P（Firefox）

### Shellでスクリプトが実行できない場合

1. **Python環境を確認**
   ```bash
   python --version
   ```

2. **依存関係を確認**
   ```bash
   pip list | grep passlib
   pip list | grep sqlalchemy
   ```

3. **手動でユーザーを作成**
   - バックエンドAPIのエンドポイントを直接呼び出す（管理者権限が必要）
   - または、データベースに直接接続してユーザーを作成

---

**最終更新**: 2025-12-01

