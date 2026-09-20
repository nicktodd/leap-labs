import { test, expect } from '@playwright/test';

test('unauthenticated visit to protected route redirects to /login', async ({ page }) => {
  await page.goto('/holdings');
  await expect(page).toHaveURL(/\/login/);
  await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
});

test('valid credentials navigate to /holdings and show nav', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Username').fill('alice');
  await page.getByLabel('Password').fill('mission123');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(/\/holdings/);
  await expect(page.getByRole('heading', { name: 'Holdings Summary' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Place Order' })).toBeVisible();
});

test('invalid credentials show error and do not navigate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Username').fill('alice');
  await page.getByLabel('Password').fill('wrongpassword');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(/\/login/);
  await expect(page.getByText('Invalid username or password')).toBeVisible();
});

test('logout returns to /login and re-blocks protected route', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Username').fill('alice');
  await page.getByLabel('Password').fill('mission123');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(/\/holdings/);

  await page.getByRole('button', { name: 'Logout' }).click();
  await expect(page).toHaveURL(/\/login/);

  await page.goto('/holdings');
  await expect(page).toHaveURL(/\/login/);
});
