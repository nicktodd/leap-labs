import { test, expect } from '@playwright/test';

test('an unauthenticated visitor is redirected to /login', async ({ page }) => {
  await page.goto('/holdings');
  await expect(page).toHaveURL(/\/login$/);
});

test('logging in navigates to /holdings and shows the current user', async ({ page }) => {
  await page.goto('/login');

  await page.fill('#username', 'alice');
  await page.fill('#password', 'mission123');
  await page.click('button[type=submit]');

  await expect(page).toHaveURL(/\/holdings$/);
  await expect(page.locator('.session')).toContainText('Logged in as alice');
});

test('logging in with the wrong password shows an error and does not navigate', async ({ page }) => {
  await page.goto('/login');

  await page.fill('#username', 'alice');
  await page.fill('#password', 'not-the-real-password');
  await page.click('button[type=submit]');

  await expect(page.locator('.error')).toContainText('Invalid username or password.');
  await expect(page).toHaveURL(/\/login$/);
});

test('logging out returns to /login and re-blocks protected routes', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#username', 'alice');
  await page.fill('#password', 'mission123');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/\/holdings$/);

  await page.click('text=Log Out');
  await expect(page).toHaveURL(/\/login$/);

  await page.goto('/holdings');
  await expect(page).toHaveURL(/\/login$/);
});
