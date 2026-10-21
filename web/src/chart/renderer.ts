import { CandlestickSeries, ColorType, HistogramSeries, LineSeries, createChart, type UTCTimestamp } from 'lightweight-charts';
import type { ChartSeries } from '../types';

/** Replace a renderer without changing the backend's scientific transformations. */
export interface ChartRenderer {
  mount(container: HTMLElement, series: ChartSeries, showOverlay: boolean): () => void;
}

export const lightweightRenderer: ChartRenderer = {
  mount(container, data, showOverlay) {
    const chart = createChart(container, {
      autoSize: true,
      layout: { background: { type: ColorType.Solid, color: '#ffffff' }, textColor: '#789080', fontSize: 10, attributionLogo: true },
      grid: { vertLines: { color: '#f0f3ec' }, horzLines: { color: '#edf2e7' } },
      rightPriceScale: { borderColor: '#e3eadb' },
      timeScale: { borderColor: '#e3eadb', timeVisible: true, secondsVisible: true },
      crosshair: { vertLine: { color: '#a6b8a2', labelBackgroundColor: '#59775d' }, horzLine: { color: '#a6b8a2', labelBackgroundColor: '#59775d' } },
    });
    const candles = chart.addSeries(CandlestickSeries, {
      upColor: '#5f957d', downColor: '#c6816b', borderUpColor: '#5f957d', borderDownColor: '#c6816b',
      wickUpColor: '#5f957d', wickDownColor: '#c6816b', priceLineVisible: false,
    });
    candles.setData(data.candles.map(point => ({ ...point, time: point.time as UTCTimestamp })));
    const volume = chart.addSeries(HistogramSeries, { color: '#cbdacf', priceFormat: { type: 'volume' }, priceLineVisible: false, lastValueVisible: false }, 1);
    volume.setData(data.volume.map(point => ({ ...point, time: point.time as UTCTimestamp })));
    chart.panes()[1]?.setHeight(70);
    if (showOverlay) {
      const overlay = chart.addSeries(LineSeries, { color: '#b3965f', lineWidth: 2, priceLineVisible: false, lastValueVisible: false, crosshairMarkerVisible: false });
      overlay.setData(data.overlay.map(point => ({ time: point.time as UTCTimestamp, value: point.value })));
    }
    chart.timeScale().fitContent();
    return () => chart.remove();
  },
};
