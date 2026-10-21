import { useEffect, useRef, useState } from 'react';
import license from '../../licenses/lightweight-charts/LICENSE?raw';
import notice from '../../licenses/lightweight-charts/NOTICE?raw';
import type { ChartSeries } from '../types';
import { lightweightRenderer, type ChartRenderer } from './renderer';

export function SeriesChart({ series, renderer = lightweightRenderer }: { series: ChartSeries; renderer?: ChartRenderer }) {
  const container = useRef<HTMLDivElement>(null);
  const [showOverlay, setShowOverlay] = useState(true);
  useEffect(() => {
    if (!container.current) return;
    return renderer.mount(container.current, series, showOverlay);
  }, [series, showOverlay, renderer]);
  return <div className="chart-wrap">
    <div className="chart-toolbar"><div className="chart-legend"><span>Velas · {series.quote_currency}</span><span>Volumen sintético</span><span><i className="legend-line" /> SMA ({series.transform.window})</span></div><label><input type="checkbox" checked={showOverlay} onChange={event => setShowOverlay(event.target.checked)} /> Mostrar SMA</label></div>
    <div ref={container} className="chart-canvas" role="img" aria-label={`Velas y volumen sintéticos de ${series.dataset_id}, expresados en ${series.quote_currency}`} />
    <p className="chart-warning">Tiempo del evento en UTC · {series.candles.length} observaciones sintéticas. El indicador procede del backend ({series.transform.version}); su disponibilidad puede ser posterior al evento.</p>
    <div className="chart-caption"><span>{notice.trim()}</span><a href="https://www.tradingview.com/" target="_blank" rel="noreferrer noopener">Gráficos de TradingView ↗</a></div>
    <details className="chart-license"><summary>Licencia y atribución de Lightweight Charts</summary><pre>{notice}{'\n'}{license}</pre></details>
  </div>;
}
