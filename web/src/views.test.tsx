import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { api } from './api';
import { Datasets, Experiments, Hypotheses } from './views';
import type { DocumentRecord, Session } from './types';

const viewer: Session = { principal: { id: 'viewer', role: 'viewer' }, csrf: 'test' };
const researcher: Session = { principal: { id: 'researcher', role: 'researcher' }, csrf: 'test' };
const document: DocumentRecord = { id: 'synthetic-test', kind: 'dataset', version: 2, content_hash: 'hash', created_at: '2020-01-01T00:00:00Z', body: { synthetic: true, partition: 'development', spec: { rows: 10 } } };

it('does not fabricate data or expose creation controls to a viewer', async () => {
  vi.spyOn(api, 'request').mockResolvedValue([]);
  render(<Datasets session={viewer} />);
  expect(await screen.findByText('El catálogo está vacío')).toBeVisible();
  expect(screen.queryByRole('button', { name: /Crear datos/ })).not.toBeInTheDocument();
  expect(screen.queryByRole('img')).not.toBeInTheDocument();
});

it('keeps reserved metadata visible without requesting a chart payload', async () => {
  const request = vi.spyOn(api, 'request').mockResolvedValue([{ ...document, body: { partition: 'final', payload_access: 'reserved' }, content_hash: 'reserved' }]);
  render(<Datasets session={viewer} />);
  await userEvent.click(await screen.findByRole('button', { name: /synthetic-test/ }));
  expect(await screen.findByText('Contenido reservado')).toBeVisible();
  expect(request.mock.calls.some(([path]) => path.includes('/series'))).toBe(false);
});

it('renders original hypothesis text safely, including untrusted source text', async () => {
  vi.spyOn(api, 'request').mockResolvedValue([{ ...document, id: 'H-24', kind: 'hypothesis', body: { statement: 'Conditional information', refutation: '<script>throw new Error("injected")</script>', null_and_comparator: 'No incremental information', source_excerpt: '<img src=x onerror=alert(1)>' } }]);
  render(<Hypotheses />);
  await userEvent.click(await screen.findByRole('button', { name: /H-24/ }));
  expect(screen.getByText('<script>throw new Error("injected")</script>')).toBeVisible();
  expect(globalThis.document.querySelector("script")).toBeNull();
  expect(globalThis.document.querySelector("img")).toBeNull();
  expect(screen.queryByRole('img')).not.toBeInTheDocument();
  expect(screen.getByText('No incremental information')).toBeVisible();
});

it('submits a bounded task against the selected immutable dataset version', async () => {
  vi.spyOn(api, 'request').mockImplementation(async path => path === '/api/datasets' ? [document] : []);
  const mutate = vi.spyOn(api, 'mutate').mockResolvedValue({ id: 'run-123' });
  render(<Experiments session={researcher} />);
  await waitFor(() => expect(screen.getByRole('option', { name: /synthetic-test/ })).toBeInTheDocument());
  await userEvent.selectOptions(screen.getByLabelText('Dataset'), 'synthetic-test');
  await userEvent.selectOptions(screen.getByLabelText('Comprobación'), 'failure_fixture');
  await userEvent.click(screen.getByRole('button', { name: /Registrar prueba/ }));
  expect(mutate).toHaveBeenCalledWith('/api/experiments', { task: 'failure_fixture', dataset_id: 'synthetic-test', dataset_version: 2, seed: 0, window: 5 });
});
