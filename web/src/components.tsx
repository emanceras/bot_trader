import type { ReactNode } from 'react';
import { ApiError } from './api';

const stateLabels: Record<string, string> = {
  operational: 'Operativo', prepared: 'Preparado', planned: 'Futuro', queued: 'En cola',
  running: 'En ejecución', succeeded: 'Completado', failed: 'Fallido', interrupted: 'Interrumpido',
  cancelled: 'Cancelado', recorded: 'Registrado', denied: 'Denegado', synthetic: 'Sintético',
};
export function Badge({ state, children }: { state: string; children?: ReactNode }) {
  return <span className={`badge badge-${state}`}>{children ?? stateLabels[state] ?? state}</span>;
}
export function ErrorNotice({ error }: { error: Error | null }) {
  if (!error) return null;
  return <div className="notice error" role="alert">
    <strong>{error instanceof ApiError && error.status === 403 ? 'Acceso no permitido' : 'No se pudo completar la solicitud'}</strong>
    <p>{error.message}</p>
    {error instanceof ApiError && error.correlationId && <small>Referencia: <code>{error.correlationId}</code></small>}
  </div>;
}
export function Loading() {
  return <div className="loading" role="status"><span className="loading-dot" /> Consultando la plataforma…</div>;
}
export function Empty({ title, children }: { title: string; children: ReactNode }) {
  return <div className="empty"><span className="empty-mark" aria-hidden="true">∅</span><h3>{title}</h3><p>{children}</p></div>;
}
export function JsonDetails({ value, title = 'Registro completo' }: { value: unknown; title?: string }) {
  return <details className="json-details"><summary>{title}</summary><pre>{JSON.stringify(value, null, 2)}</pre></details>;
}
export function DateTime({ value }: { value: string | null }) {
  if (!value) return <>—</>;
  return <time dateTime={value} title={value}>{new Intl.DateTimeFormat('es-ES', {
    dateStyle: 'medium', timeStyle: 'short', timeZone: 'UTC',
  }).format(new Date(value))} UTC</time>;
}
export function Hash({ value }: { value: string }) {
  return <code className="hash" title={value}>{value}</code>;
}
