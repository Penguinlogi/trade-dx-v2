import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright設定
 * https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './e2e',
  /* テストの最大実行時間 */
  timeout: 30 * 1000,
  expect: {
    /* アサーションのタイムアウト */
    timeout: 5000
  },
  /* テストを並列実行 */
  fullyParallel: true,
  /* CI環境でCIを失敗させる */
  forbidOnly: !!process.env.CI,
  /* CI環境でリトライを無効化 */
  retries: process.env.CI ? 2 : 0,
  /* CI環境で並列実行を無効化 */
  workers: process.env.CI ? 1 : undefined,
  /* レポーター設定 */
  reporter: 'html',
  /* 共有設定 */
  use: {
    /* ベースURL */
    baseURL: 'http://localhost:3000',
    /* アクションのタイムアウト */
    actionTimeout: 0,
    /* ナビゲーションのタイムアウト */
    navigationTimeout: 60000,
    /* トレースを収集 */
    trace: 'on-first-retry',
  },

  /* プロジェクト設定 */
  /* デフォルトではChromiumのみで実行（セキュリティソフトの誤検知を回避） */
  /* 全ブラウザでテストする場合は、環境変数 ALL_BROWSERS=true を設定 */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // FirefoxとWebKitはセキュリティソフトの誤検知を避けるため、デフォルトでは無効化
    // 全ブラウザでテストする場合は、環境変数 ALL_BROWSERS=true を設定してからコメントを外す
    ...(process.env.ALL_BROWSERS === 'true' ? [
      {
        name: 'firefox',
        use: { ...devices['Desktop Firefox'] },
      },
      {
        name: 'webkit',
        use: { ...devices['Desktop Safari'] },
      },
    ] : []),
  ],

  /* 開発サーバーの起動 */
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
