# E2Eテスト実行ガイド

## デフォルト設定

セキュリティソフトの誤検知を避けるため、**デフォルトではChromiumのみでテストを実行**します。

## 実行方法

### Chromiumのみで実行（推奨・デフォルト）

```bash
npm run test:e2e
```

またはUIモードで：

```bash
npm run test:e2e:ui
```

### 全ブラウザで実行（オプション）

セキュリティソフトの除外設定を完了している場合、全ブラウザでテストを実行できます：

**Windows:**
```bash
set ALL_BROWSERS=true && npm run test:e2e
```

**PowerShell:**
```powershell
$env:ALL_BROWSERS="true"; npm run test:e2e
```

**Linux/Mac:**
```bash
ALL_BROWSERS=true npm run test:e2e
```

## 設定の変更

`playwright.config.ts`で、デフォルトのブラウザ設定を変更できます。

### Chromiumのみ（デフォルト）

現在の設定では、FirefoxとWebKitは環境変数`ALL_BROWSERS=true`が設定されている場合のみ実行されます。

### 全ブラウザを常に有効にする

`playwright.config.ts`の`projects`セクションで、FirefoxとWebKitのコメントを外してください：

```typescript
projects: [
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'] },
  },
  {
    name: 'firefox',
    use: { ...devices['Desktop Firefox'] },
  },
  {
    name: 'webkit',
    use: { ...devices['Desktop Safari'] },
  },
],
```

## セキュリティソフトの設定

NortonなどのセキュリティソフトがPlaywrightのブラウザを検疫に移動した場合：

1. 検疫から復元する
2. 除外設定に以下を追加：
   ```
   C:\Users\<ユーザー名>\AppData\Local\ms-playwright\
   ```

詳細は `PLAYWRIGHT_SECURITY_SETTINGS.md` を参照してください。




