import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:4200',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
  ],
});
