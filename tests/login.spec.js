import { test, expect } from '@playwright/test';

test('valid login shows welcome message', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username').fill('student');
  await page.getByTestId('password').fill('pass123');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('message')).toHaveText('Welcome, student!');
});

test('wrong password shows error', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username').fill('student');
  await page.getByTestId('password').fill('wrong');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('message')).toHaveText('Invalid credentials');
});  