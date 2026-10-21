import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  timeout: 90_000,
  expect: { timeout: 20_000 },
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:8000',
    headless: true,
    launchOptions: { executablePath: process.env.BOT_TRADER_CHROMIUM ?? '/usr/bin/chromium' },
    screenshot: 'off',
    trace: 'off',
    video: 'off',
  },
});
