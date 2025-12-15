# Playwright セキュリティソフト設定ガイド

## 問題

セキュリティソフト（Norton、Windows Defender等）がPlaywrightのブラウザ実行ファイルを誤検知し、検疫に移動することがあります。

## 解決方法

### 1. ブラウザの再インストール

```bash
cd frontend
npx playwright install
```

または、バッチファイルを使用：

```batch
cd frontend
.\install_playwright_browsers.bat
```

### 2. セキュリティソフトの除外設定

#### Nortonの場合

1. Nortonを開く
2. 「設定」→「ウイルス対策」→「除外/低リスク」を選択
3. 「除外」タブを開く
4. 「追加」をクリック
5. 以下のディレクトリを追加：
   ```
   C:\Users\<ユーザー名>\AppData\Local\ms-playwright\
   ```
6. 「OK」をクリックして保存

#### Windows Defenderの場合

1. Windowsセキュリティを開く
2. 「ウイルスと脅威の防止」を選択
3. 「ウイルスと脅威の防止の設定」の「設定の管理」をクリック
4. 「除外」セクションで「除外の追加または削除」をクリック
5. 「除外の追加」→「フォルダー」を選択
6. 以下のディレクトリを追加：
   ```
   C:\Users\<ユーザー名>\AppData\Local\ms-playwright\
   ```

### 3. 一時的な回避策：Chromiumのみでテスト実行

FirefoxとWebKitが検疫に移動された場合、一時的にChromiumのみでテストを実行できます：

```bash
cd frontend
npx playwright test --project=chromium
```

または、`playwright.config.ts`を一時的に変更してFirefoxとWebKitをコメントアウト：

```typescript
projects: [
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'] },
  },
  // 一時的にコメントアウト
  // {
  //   name: 'firefox',
  //   use: { ...devices['Desktop Firefox'] },
  // },
  // {
  //   name: 'webkit',
  //   use: { ...devices['Desktop Safari'] },
  // },
],
```

## 確認方法

ブラウザが正しくインストールされているか確認：

```bash
cd frontend
npx playwright install --dry-run
```

## 参考情報

- [Playwright公式ドキュメント - ブラウザのインストール](https://playwright.dev/docs/browsers#installing-browsers)
- [Playwrightトラブルシューティング](https://playwright.dev/docs/troubleshooting)




