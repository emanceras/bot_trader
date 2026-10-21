import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SeriesChart } from './SeriesChart';
import type { ChartSeries } from '../types';

const series: ChartSeries = {
  dataset_id: 'synthetic-test', dataset_version: 1, synthetic: true, quote_currency: 'USD',
  candles: [{ time: 1, open: 10, high: 12, low: 9, close: 11 }], volume: [{ time: 1, value: 20 }],
  overlay: [{ time: 1, value: 10.5, available_at: '2020-01-01T00:00:00.700Z' }],
  transform: { name: 'causal_sma', version: 'causal-sma/1', window: 5, input_content_hash: 'test' }, display_only: 'Technical fixture',
};

it('passes backend values unchanged to a replaceable renderer and cleans up on changes', async () => {
  const cleanup = vi.fn();
  const renderer = { mount: vi.fn(() => cleanup) };
  const view = render(<SeriesChart series={series} renderer={renderer} />);
  expect(renderer.mount).toHaveBeenCalledWith(expect.any(HTMLElement), series, true);
  expect(screen.getByRole('link', { name: /TradingView/ })).toHaveAttribute('href', 'https://www.tradingview.com/');
  expect(screen.getAllByText(/Copyright.*2025 TradingView/).length).toBeGreaterThan(0);
  await userEvent.click(screen.getByRole('checkbox', { name: 'Mostrar SMA' }));
  expect(cleanup).toHaveBeenCalledOnce();
  expect(renderer.mount).toHaveBeenLastCalledWith(expect.any(HTMLElement), series, false);
  view.unmount();
  expect(cleanup).toHaveBeenCalledTimes(2);
});
