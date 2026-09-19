import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:4200',
  },
  // Requires: ng serve running on 4200, plus the real auth service (3000)
  // and mission service (8090) - this is an end-to-end test, not a mock.
});
