import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const state = process.env.BOT_TRADER_E2E_STATE;
if (!state) throw new Error('BOT_TRADER_E2E_STATE must point to an initialized synthetic test state.');

async function signIn(page: Page, role = 'admin') {
  await page.goto('/');
  await page.getByLabel('Credencial de acceso').fill(readFileSync(resolve(state!, `${role}.token`), 'utf8').trim());
  await page.getByRole('button', { name: 'Entrar al laboratorio' }).click();
  await expect(page.getByRole('navigation', { name: 'Navegación principal' })).toBeVisible();
}

async function navigate(page: Page, name: string) {
  await page.getByRole('navigation').getByRole('link', { name, exact: true }).click();
}

test('F: actual hypotheses, synthetic catalog, chart, worker, results, audit and revocation', async ({ page, context }) => {
  const failures: string[] = [];
  page.on('pageerror', error => failures.push(error.message));
  await signIn(page);
  await expect(page.getByText('Hipótesis registradas', { exact: true })).toBeVisible();
  await navigate(page, 'Hipótesis');
  await expect(page.locator('.hypothesis-card')).toHaveCount(25);
  await page.getByRole('button', { name: /H-24/ }).click();
  await expect(page.getByRole('heading', { name: 'Condiciones de refutación' })).toBeVisible();
  await navigate(page, 'Datos y gráficos');
  await page.getByLabel('Observaciones').fill('24');
  await page.getByLabel('Semilla', { exact: true }).fill('73');
  const [created] = await Promise.all([
    page.waitForResponse(response => response.url().endsWith('/api/datasets') && response.request().method() === 'POST' && response.status() === 201),
    page.getByRole('button', { name: /Crear datos de prueba/ }).click(),
  ]);
  const datasetId = (await created.json()).id;
  expect(typeof datasetId).toBe('string');
  await expect(page.locator('.chart-canvas canvas').first()).toBeVisible();
  await expect(page.getByText(/24 observaciones sintéticas/)).toBeVisible();
  await expect(page.getByRole('link', { name: /Gráficos de TradingView/ })).toHaveAttribute('href', 'https://www.tradingview.com/');
  await page.screenshot({ path: resolve(state!, 'chart-desktop.png'), fullPage: true });
  await navigate(page, 'Pruebas técnicas');
  await page.getByRole('combobox', { name: 'Dataset', exact: true }).selectOption(datasetId);
  await page.getByRole('combobox', { name: 'Comprobación', exact: true }).selectOption('ledger_check');
  for (let attempt = 0; attempt < 2; attempt++) {
    const [response] = await Promise.all([
      page.waitForResponse(response => response.url().endsWith('/api/experiments') && response.request().method() === 'POST' && response.status() === 201),
      page.getByRole('button', { name: /Registrar prueba/ }).click(),
    ]);
    const run = await response.json();
    await expect(page.getByRole('row').filter({ hasText: run.id })).toContainText('Completado');
    await expect(page.getByRole('heading', { name: 'Resultado técnico' })).toBeVisible();
  }
  const boxes = page.getByRole('checkbox', { name: /^Comparar / });
  await boxes.nth(0).check();
  await boxes.nth(1).check();
  await page.getByRole('button', { name: 'Comparar (2)' }).click();
  await expect(page.getByText(/El resultado estable coincide/)).toBeVisible();
  const reportLink = page.getByRole('link', { name: /Informe JSON/ });
  const report = await context.request.get((await reportLink.getAttribute('href'))!);
  expect(report.ok()).toBe(true);
  expect((await report.json()).financial_validation).toBe(false);
  await page.getByRole('combobox', { name: 'Comprobación', exact: true }).selectOption('failure_fixture');
  await page.getByRole('button', { name: /Registrar prueba/ }).click();
  await expect(page.getByText('Fallo preservado', { exact: true })).toBeVisible();
  await navigate(page, 'Módulos');
  await expect(page.locator('.module-card')).toHaveCount(15);
  await expect(page.locator('.module-card').filter({ hasText: 'trading-engine' })).toContainText('Futuro');
  await navigate(page, 'Actividad y errores');
  await expect(page.getByRole('table')).toContainText('runs.finish');
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: resolve(state!, 'audit-mobile.png'), fullPage: true });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBe(true);
  await page.getByRole('button', { name: /Cerrar sesión/ }).click();
  await expect(page.getByLabel('Credencial de acceso')).toBeVisible();
  expect((await context.request.get('/api/status')).status()).toBe(401);
  expect(failures).toEqual([]);
});

test('viewer sees real records, cannot create datasets, and a server denial is explicit', async ({ page }) => {
  await signIn(page, 'viewer');
  await navigate(page, 'Datos y gráficos');
  await expect(page.getByRole('button', { name: /Crear datos de prueba/ })).toHaveCount(0);
  await expect(page.getByRole('heading', { name: 'Catálogo versionado' })).toBeVisible();
  const status = await page.evaluate(async () => {
    const session = await (await fetch('/api/session')).json();
    const response = await fetch('/api/datasets', { method: 'POST', headers: {
      'Content-Type': 'application/json', 'X-CSRF-Token': session.csrf,
    }, body: JSON.stringify({ rows: 4 }) });
    return response.status;
  });
  expect(status).toBe(403);
});
