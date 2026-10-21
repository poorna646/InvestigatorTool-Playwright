// @ts-check
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  retries: 1,
  timeout: 10000,
  reporter: [['list'], ['html', { open: 'never' }], ['./failure-reporter.js']],  
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npx http-server demo-app -p 3000 -s',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
  },
});