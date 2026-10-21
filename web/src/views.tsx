import { useState, type FormEvent } from 'react';
import { api } from './api';
import { Badge, DateTime, Empty, ErrorNotice, Hash, JsonDetails, Loading } from './components';
import { useResource } from './hooks';
import { SeriesChart } from './chart/SeriesChart';
import type { AuditRecord, ChartSeries, DocumentRecord, Json, ModuleManifest, PlatformStatus, RunRecord, Session } from './types';

const object = (value: Json | undefined): Record<string, Json> => value && typeof value === 'object' && !Array.isArray(value) ? value : {};
const text = (value: Json | undefined, fallback = '—') => value == null ? fallback : String(value);
const canWrite = (session: Session) => ['admin', 'researcher'].includes(session.principal.role);

export function Overview() {
  const status = useResource<PlatformStatus>('/api/status');
  const modules = useResource<ModuleManifest[]>('/api/modules');
  return <>
    <ErrorNotice error={status.error} />
    {status.loading && <Loading />}
    {status.data && <>
      <div className="stats-grid">
        {[['Hipótesis registradas', status.data.hypotheses, 'Preguntas preservadas'], ['Datasets', status.data.datasets, 'Catálogo de fixtures'], ['Ejecuciones técnicas', status.data.runs, 'Incluye fallos e interrupciones'], ['Experimentos financieros', status.data.financial_experiments, 'Sin evaluación económica']].map(([label, value, note]) => <div className="stat-card" key={label}><span>{label}</span><strong>{value}</strong><small>{note}</small></div>)}
      </div>
      <div className="overview-grid">
        <section className="panel status-panel"><div className="panel-heading"><h2>Estado de la plataforma</h2><Badge state="synthetic">Entorno técnico</Badge></div>
          <dl className="definition-list"><div><dt>Fase autorizada</dt><dd>{status.data.phase}</dd></div><div><dt>Moneda de cuenta</dt><dd>{status.data.account_currency}</dd></div><div><dt>Ejecución real</dt><dd>{status.data.live_execution ? 'Revisar estado de ejecución' : 'Inactiva'}</dd></div><div><dt>Procesamiento de tareas</dt><dd>Proceso separado</dd></div></dl>
          <div className="notice compact"><strong>Estado del worker</strong><p>{status.data.worker}</p></div>
          <p className="small muted">Los contadores consultan hasta {status.data.counts_limit} registros por categoría. Los datos se actualizan al abrir esta vista.</p>
        </section>
        <section className="panel research-panel"><p className="eyebrow">MÉTODO DEL PROYECTO</p><h2>Conservar la incertidumbre.<br />Hacer verificable el proceso.</h2><p>Las pruebas de esta fase comprueban contratos, integridad y reproducibilidad con datos sintéticos. El registro científico conserva las hipótesis y sus condiciones de fracaso.</p><a href="#hypotheses" className="text-link">Explorar el registro de hipótesis <span aria-hidden="true">↗</span></a><div className="research-divider" /><p className="small">USD es la referencia contable. USDT y USDC no se consideran equivalentes automáticamente.</p></section>
      </div>
    </>}
    <section className="panel"><div className="panel-heading"><h2>Capacidades de la plataforma</h2><a href="#modules" className="text-link">Ver inventario ↗</a></div><ErrorNotice error={modules.error} />{modules.loading && <Loading />}{modules.data && <div className="module-summary">{['operational', 'prepared', 'planned'].map(state => <div key={state}><Badge state={state} /><strong>{modules.data!.filter(module => module.status === state).length}</strong><span>{state === 'operational' ? 'Servicios implementados' : state === 'prepared' ? 'Contratos o alcance parcial' : 'Trabajo futuro'}</span></div>)}</div>}</section>
  </>;
}

export function Hypotheses() {
  const resource = useResource<DocumentRecord[]>('/api/hypotheses');
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState<string | null>(null);
  const records = resource.data?.filter(record => `${record.id} ${text(record.body.statement)}`.toLowerCase().includes(search.toLowerCase())) ?? [];
  const selectedRecord = resource.data?.find(record => record.id === selected);
  return <>
    <div className="toolbar"><label className="search-field"><span className="sr-only">Buscar hipótesis</span><input type="search" placeholder="Buscar por identificador o enunciado…" value={search} onChange={event => setSearch(event.target.value)} /></label><span className="small muted">{records.length} hipótesis</span></div>
    <ErrorNotice error={resource.error} />{resource.loading && <Loading />}
    {!resource.loading && resource.data?.length === 0 && <Empty title="Sin hipótesis importadas">Inicializa el registro desde el documento científico preservado del proyecto.</Empty>}
    {resource.data && records.length === 0 && resource.data.length > 0 && <Empty title="Sin coincidencias">Prueba otro identificador o término.</Empty>}
    <div className="split-view"><section className="hypothesis-list" aria-label="Hipótesis registradas">{records.map(record => <button key={record.id} className={`hypothesis-card ${selected === record.id ? 'selected' : ''}`} onClick={() => setSelected(record.id)}><div><span className="record-id">{record.id}</span><small>v{record.version}</small></div><p>{text(record.body.statement)}</p><span className="small muted">Propuesta · Sin validación financiera <span aria-hidden="true">↗</span></span></button>)}</section>
      {selectedRecord ? <aside className="panel detail-panel"><div className="panel-heading"><h2>{selectedRecord.id}</h2><span className="version">v{selectedRecord.version}</span></div><h3>Enunciado</h3><p>{text(selectedRecord.body.statement)}</p><h3>Hipótesis nula y comparación</h3><p>{text(selectedRecord.body.null_and_comparator, 'Incluida en el enunciado original.')}</p><h3>Condiciones de refutación</h3><p>{text(selectedRecord.body.refutation, 'Consultar el contexto del documento original.')}</p><h3>Datos requeridos</h3><p>{text(selectedRecord.body.required_data)}</p><h3>Procedencia</h3><p className="small">{text(selectedRecord.body.source_path)} · {text(selectedRecord.body.source_section)}</p><Hash value={text(selectedRecord.body.source_sha256)} /><details className="json-details"><summary>Contexto científico original</summary><pre>{text(selectedRecord.body.source_excerpt)}</pre></details><JsonDetails value={selectedRecord} title="Versión y procedencia completas" /></aside> : <aside className="panel selection-hint"><span aria-hidden="true">◇</span><h3>Inspecciona una pregunta</h3><p>Selecciona una hipótesis para consultar su nula, refutación y fuente original.</p></aside>}
    </div>
  </>;
}

export function Datasets({ session }: { session: Session }) {
  const resource = useResource<DocumentRecord[]>('/api/datasets');
  const [selected, setSelected] = useState<string | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [pending, setPending] = useState(false);
  const [rows, setRows] = useState(120);
  const [seed, setSeed] = useState(42);
  const [interval, setInterval] = useState(60);
  const dataset = resource.data?.find(record => record.id === selected);
  const series = useResource<ChartSeries>(dataset && dataset.body.partition !== 'final' ? `/api/datasets/${encodeURIComponent(dataset.id)}/series?version=${dataset.version}` : null);
  async function create(event: FormEvent) {
    event.preventDefault(); setPending(true); setError(null);
    try {
      const record = await api.mutate<DocumentRecord>('/api/datasets', { rows, seed, interval_seconds: interval });
      resource.refresh(); setSelected(record.id);
    } catch (failure) { setError(failure as Error); } finally { setPending(false); }
  }
  return <>
    {canWrite(session) && <section className="panel"><div className="panel-heading"><div><h2>Crear fixture sintética</h2><p className="small muted">SYNTH-USD · Prueba de infraestructura, sin precios de mercado.</p></div><Badge state="synthetic" /></div><form className="inline-form" onSubmit={create}><label>Observaciones<input type="number" required min={2} max={10000} value={rows} onChange={event => setRows(event.target.valueAsNumber)} /></label><label>Semilla<input type="number" required min={0} max={4294967295} value={seed} onChange={event => setSeed(event.target.valueAsNumber)} /></label><label>Intervalo (segundos)<input type="number" required min={1} max={31536000} value={interval} onChange={event => setInterval(event.target.valueAsNumber)} /></label><button className="primary" disabled={pending}>{pending ? 'Creando…' : 'Crear datos de prueba'}<span aria-hidden="true">＋</span></button></form><ErrorNotice error={error} /></section>}
    <section className="panel"><div className="panel-heading"><h2>Catálogo versionado</h2><button className="secondary small-button" onClick={resource.refresh}>Actualizar</button></div><ErrorNotice error={resource.error} />{resource.loading && <Loading />}
      {resource.data?.length === 0 && <Empty title="El catálogo está vacío">Crea una fixture sintética para comprobar datos, gráficos y ejecuciones técnicas.</Empty>}
      {Boolean(resource.data?.length) && <div className="table-scroll"><table><thead><tr><th>Dataset / versión</th><th>Origen</th><th>Observaciones</th><th>Partición</th><th>Registrado</th></tr></thead><tbody>{resource.data?.map(record => <tr key={record.id} className={selected === record.id ? 'selected-row' : ''}><td><button className="table-link" onClick={() => setSelected(record.id)}>{record.id}<small>v{record.version}</small></button></td><td><Badge state="synthetic" /></td><td>{text(object(record.body.spec).rows)}</td><td>{text(record.body.partition)}</td><td><DateTime value={record.created_at} /></td></tr>)}</tbody></table></div>}
    </section>
    {dataset && <section className="panel"><div className="panel-heading"><div><h2>{dataset.body.partition === 'final' ? 'Partición reservada' : 'SYNTH-USD · Serie de prueba'}</h2><p className="small muted">{dataset.id} · v{dataset.version}</p></div><Badge state="synthetic" /></div>
      {dataset.body.partition === 'final' ? <div className="notice"><strong>Contenido reservado</strong><p>El payload final no está disponible para ningún rol en esta fase.</p></div> : <><ErrorNotice error={series.error} />{series.loading && <Loading />}{!series.loading && series.data?.dataset_id === dataset.id && series.data.dataset_version === dataset.version && <SeriesChart series={series.data} />}</>}
      <JsonDetails value={dataset} title="Procedencia, versión y controles de calidad" />
    </section>}
  </>;
}

const tasks = [
  ['quality_check', 'Integridad de datos'], ['transform_check', 'Transformación reproducible'],
  ['ledger_check', 'Contabilidad sintética'], ['failure_fixture', 'Fallo intencionado'],
];

export function Experiments({ session }: { session: Session }) {
  const runs = useResource<RunRecord[]>('/api/experiments', 5);
  const datasets = useResource<DocumentRecord[]>('/api/datasets');
  const [selected, setSelected] = useState<string | null>(null);
  const [checked, setChecked] = useState<string[]>([]);
  const [datasetId, setDatasetId] = useState('');
  const [task, setTask] = useState('quality_check');
  const [seed, setSeed] = useState(0);
  const [window, setWindow] = useState(5);
  const [error, setError] = useState<Error | null>(null);
  const [pending, setPending] = useState(false);
  const [comparison, setComparison] = useState<Record<string, Json> | null>(null);
  const available = datasets.data?.filter(dataset => dataset.body.partition !== 'final') ?? [];
  const selectedRun = runs.data?.find(run => run.id === selected);
  async function submit(event: FormEvent) {
    event.preventDefault(); setPending(true); setError(null);
    const dataset = available.find(record => record.id === datasetId);
    if (!dataset) { setError(new Error('Selecciona un dataset disponible.')); setPending(false); return; }
    try {
      const run = await api.mutate<RunRecord>('/api/experiments', { task, dataset_id: dataset.id, dataset_version: dataset.version, seed, window });
      setSelected(run.id); runs.refresh();
    } catch (failure) { setError(failure as Error); } finally { setPending(false); }
  }
  async function compare() {
    setPending(true); setError(null); setComparison(null);
    try { setComparison(await api.mutate<Record<string, Json>>('/api/experiments/compare', { run_ids: checked })); }
    catch (failure) { setError(failure as Error); } finally { setPending(false); }
  }
  async function cancel(identifier: string) {
    setPending(true); setError(null);
    try { await api.mutate(`/api/experiments/${encodeURIComponent(identifier)}/cancel`, {}); runs.refresh(); }
    catch (failure) { setError(failure as Error); } finally { setPending(false); }
  }
  return <>
    {canWrite(session) && <section className="panel"><div className="panel-heading"><h2>Nueva prueba técnica</h2><Badge state="synthetic" /></div><form className="inline-form run-form" onSubmit={submit}>
      <label>Dataset<select required value={datasetId} onChange={event => setDatasetId(event.target.value)}><option value="">Seleccionar fixture…</option>{available.map(dataset => <option key={dataset.id} value={dataset.id}>{dataset.id} · v{dataset.version}</option>)}</select></label>
      <label>Comprobación<select value={task} onChange={event => setTask(event.target.value)}>{tasks.map(([id, label]) => <option key={id} value={id}>{label}</option>)}</select></label>
      <label>Semilla<input type="number" min={0} max={4294967295} required value={seed} onChange={event => setSeed(event.target.valueAsNumber)} /></label>
      <label>Ventana de transformación<input type="number" min={2} max={500} required value={window} onChange={event => setWindow(event.target.valueAsNumber)} /></label>
      <button className="primary" disabled={pending || !datasetId}>{pending ? 'Procesando…' : 'Registrar prueba'}<span aria-hidden="true">↗</span></button>
    </form><p className="small muted">La prueba se registra en una cola persistente. El worker de la plataforma debe estar en marcha para procesarla. Esta vista consulta los estados cada 5 segundos.</p><ErrorNotice error={datasets.error} /></section>}
    <ErrorNotice error={error} />
    <section className="panel"><div className="panel-heading"><h2>Registro de ejecuciones</h2><div className="button-group"><button className="secondary small-button" onClick={runs.refresh}>Actualizar</button><button className="secondary small-button" disabled={checked.length < 2 || pending} onClick={compare}>Comparar ({checked.length})</button></div></div><ErrorNotice error={runs.error} />{runs.loading && !runs.data && <Loading />}
      {runs.data?.length === 0 && <Empty title="Todavía no hay ejecuciones">Los intentos y sus fallos aparecerán aquí con su configuración y resultados.</Empty>}
      {Boolean(runs.data?.length) && <div className="table-scroll"><table><thead><tr><th><span className="sr-only">Comparar</span></th><th>Ejecución</th><th>Comprobación</th><th>Estado</th><th>Creada</th></tr></thead><tbody>{runs.data?.map(run => <tr key={run.id} className={selected === run.id ? 'selected-row' : ''}><td><input type="checkbox" aria-label={`Comparar ${run.id}`} checked={checked.includes(run.id)} disabled={!checked.includes(run.id) && checked.length >= 10} onChange={event => { setChecked(current => event.target.checked ? [...current, run.id] : current.filter(id => id !== run.id)); setComparison(null); }} /></td><td><button className="table-link" onClick={() => setSelected(run.id)}>{run.id}</button></td><td>{tasks.find(([id]) => id === run.config.task)?.[1] ?? text(run.config.task)}</td><td><Badge state={run.state} /></td><td><DateTime value={run.created_at} /></td></tr>)}</tbody></table></div>}
    </section>
    {comparison && <section className="panel"><div className="panel-heading"><h2>Comparación técnica</h2><span className="small muted">Sin clasificación financiera</span></div><p>{comparison.comparable ? 'Configuraciones comparables según el servicio.' : 'Estas ejecuciones no cumplen el criterio de comparabilidad.'} {comparison.same_result === true ? 'El resultado estable coincide.' : comparison.same_result === false ? 'La coincidencia de resultados no se ha confirmado; revisa los estados y hashes disponibles.' : ''}</p><JsonDetails value={comparison} title="Criterios y diferencias de la comparación" /></section>}
    {selectedRun && <section className="panel"><div className="panel-heading"><div><h2>Detalle de ejecución</h2><p className="small muted break-word">{selectedRun.id}</p></div><Badge state={selectedRun.state} /></div>
      <div className="run-meta"><div><span>Creada</span><DateTime value={selectedRun.created_at} /></div><div><span>Inicio</span><DateTime value={selectedRun.started_at} /></div><div><span>Fin</span><DateTime value={selectedRun.finished_at} /></div></div>
      {selectedRun.state === 'queued' && <div className="notice"><strong>En espera del worker</strong><p>La tarea está guardada. El registro no indica que un worker esté activo.</p></div>}
      {selectedRun.error && <div className="notice error"><strong>Fallo preservado</strong><pre>{JSON.stringify(selectedRun.error, null, 2)}</pre></div>}
      {selectedRun.result && <><h3>Resultado técnico</h3><pre className="result-json">{JSON.stringify(selectedRun.result, null, 2)}</pre><div className="button-group artifact-links"><a className="secondary" href={`/api/experiments/${encodeURIComponent(selectedRun.id)}/artifacts/report.json`} download>Informe JSON ↓</a><a className="secondary" href={`/api/experiments/${encodeURIComponent(selectedRun.id)}/artifacts/report.md`} download>Informe Markdown ↓</a></div></>}
      <JsonDetails value={selectedRun.config} title="Configuración congelada" /><JsonDetails value={selectedRun.manifest} title="Datos, código, entorno y semillas" /><JsonDetails value={selectedRun} title="Registro completo del intento" />
      {canWrite(session) && selectedRun.state === 'queued' && <button className="secondary danger small-button" onClick={() => cancel(selectedRun.id)} disabled={pending}>Cancelar tarea en cola</button>}
    </section>}
  </>;
}

export function Modules() {
  const resource = useResource<ModuleManifest[]>('/api/modules');
  return <><div className="notice"><strong>Estados explícitos</strong><p>Operativo: servicio implementado dentro del alcance declarado. Preparado: contrato o implementación parcial. Futuro: capacidad pendiente, sin control de ejecución.</p></div><ErrorNotice error={resource.error} />{resource.loading && <Loading />}<div className="modules-grid">{resource.data?.map(module => <article className="panel module-card" key={module.id}><div className="panel-heading"><span className="module-symbol" aria-hidden="true">▦</span><Badge state={module.status} /></div><h2>{module.id}</h2><p>{module.description}</p><dl><div><dt>Versión</dt><dd>{module.version}</dd></div><div><dt>Dependencias</dt><dd>{module.dependencies.join(', ') || 'Ninguna'}</dd></div><div><dt>Capacidades registradas</dt><dd>{module.capabilities.join(', ') || 'Sin capacidades opcionales'}</dd></div></dl></article>)}</div>{resource.data?.length === 0 && <Empty title="Sin módulos registrados">Comprueba la composición y el registro del backend.</Empty>}</>;
}

export function Audit() {
  const resource = useResource<AuditRecord[]>('/api/audit');
  const [query, setQuery] = useState('');
  const entries = resource.data?.filter(item => `${item.action} ${item.outcome} ${item.actor} ${item.resource}`.toLowerCase().includes(query.toLowerCase())) ?? [];
  return <><div className="toolbar"><label className="search-field"><span className="sr-only">Filtrar actividad</span><input type="search" placeholder="Filtrar por acción, resultado o referencia…" value={query} onChange={event => setQuery(event.target.value)} /></label><button className="secondary" onClick={resource.refresh}>Actualizar</button></div><section className="panel"><div className="panel-heading"><h2>Actividad reciente</h2><span className="small muted">{entries.length} registros visibles</span></div><ErrorNotice error={resource.error} />{resource.loading && <Loading />}{resource.data && entries.length === 0 && <Empty title="Sin registros para mostrar">La actividad disponible aparecerá aquí. Revisa el filtro si lo has aplicado.</Empty>}{entries.length > 0 && <div className="table-scroll"><table><thead><tr><th>Momento</th><th>Acción / actor</th><th>Resultado</th><th>Referencia y detalle</th></tr></thead><tbody>{entries.map(item => <tr key={item.id}><td><DateTime value={item.created_at} /></td><td><strong>{item.action}</strong><small className="table-small">{item.actor}</small></td><td><Badge state={item.outcome} /></td><td><code className="audit-resource">{item.resource}</code>{Object.keys(item.details).length > 0 && <JsonDetails value={item.details} title="Detalle" />}</td></tr>)}</tbody></table></div>}</section></>;
}
