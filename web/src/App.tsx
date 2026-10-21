import { useEffect, useState, type FormEvent } from 'react';
import { api } from './api';
import { ErrorNotice, Loading } from './components';
import { sections, type SectionId } from './sections';
import type { Session } from './types';

function currentSection(): SectionId {
  const route = window.location.hash.slice(1);
  return sections.find(section => section.id === route)?.id ?? 'overview';
}

function Login({ onSession, initialError }: { onSession: (session: Session) => void; initialError: Error | null }) {
  const [token, setToken] = useState('');
  const [error, setError] = useState(initialError);
  const [pending, setPending] = useState(false);
  async function submit(event: FormEvent) {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      const session = await api.mutate<Session>('/api/session', { token });
      setToken('');
      onSession(session);
    } catch (failure) { setError(failure as Error); }
    finally { setPending(false); }
  }
  return <main className="login-layout">
    <div className="login-story">
      <Brand />
      <div><p className="eyebrow">Research infrastructure</p><h1>La evidencia<br />antes de la decisión.</h1>
        <p className="login-intro">Un espacio de trabajo para investigación cuantitativa, datos trazables y pruebas reproducibles.</p></div>
      <div className="login-footnote"><span className="status-dot" /> Fase III · Plataforma técnica</div>
    </div>
    <div className="login-panel"><div className="login-card">
      <p className="eyebrow">Acceso local</p><h2>Tu laboratorio</h2>
      <p className="muted">Introduce la credencial local generada al inicializar la plataforma.</p>
      <form onSubmit={submit} className="stack-form">
        <label>Credencial de acceso<input type="password" name="token" autoComplete="current-password" required minLength={24} value={token} onChange={event => setToken(event.target.value)} autoFocus /></label>
        <button className="primary" disabled={pending || token.length < 24}>{pending ? 'Comprobando…' : 'Entrar al laboratorio'}<span aria-hidden="true">↗</span></button>
      </form>
      <ErrorNotice error={error} />
      <p className="small muted login-helper">La sesión se guarda en una cookie protegida. No se solicitan credenciales de exchanges.</p>
      <div className="notice compact"><strong>Solo pruebas sintéticas</strong><p>Las investigaciones financieras y la conexión a mercados requieren autorización posterior.</p></div>
    </div></div>
  </main>;
}

function Brand() {
  return <div className="brand"><span className="brand-symbol" aria-hidden="true">b<span>_</span></span><span>bot_trader<small>QUANTITATIVE RESEARCH</small></span></div>;
}

export function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [checking, setChecking] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [sectionId, setSectionId] = useState(currentSection);
  const [signingOut, setSigningOut] = useState(false);
  const section = sections.find(item => item.id === sectionId) ?? sections[0];
  const View = section.component;

  useEffect(() => {
    const update = () => setSectionId(currentSection());
    window.addEventListener('hashchange', update);
    return () => window.removeEventListener('hashchange', update);
  }, []);
  useEffect(() => {
    const controller = new AbortController();
    api.onUnauthorized = () => { api.setSession(null); setSession(null); };
    api.request<Session>('/api/session', { signal: controller.signal }).then(value => {
      if (controller.signal.aborted) return;
      api.setSession(value); setSession(value);
    }).catch(failure => {
      if (!controller.signal.aborted && failure.status !== 401) setError(failure as Error);
    }).finally(() => { if (!controller.signal.aborted) setChecking(false); });
    return () => { controller.abort(); api.onUnauthorized = undefined; };
  }, []);

  if (checking) return <main className="boot-screen"><Loading /></main>;
  if (!session) return <Login initialError={error} onSession={value => { api.setSession(value); setSession(value); setError(null); }} />;
  async function logout() {
    setSigningOut(true);
    try {
      await api.request('/api/session', { method: 'DELETE' });
      api.setSession(null); setSession(null); setError(null);
    } catch (failure) { setError(failure as Error); }
    finally { setSigningOut(false); }
  }
  return <div className="app-shell">
    <a href="#main" className="skip-link" onClick={event => { event.preventDefault(); document.getElementById('main')?.focus(); }}>Saltar al contenido</a>
    <aside className="sidebar">
      <Brand />
      <p className="nav-label">ESPACIO DE INVESTIGACIÓN</p>
      <nav aria-label="Navegación principal">{sections.map(item => <a key={item.id} href={`#${item.id}`} className={item.id === sectionId ? 'nav-link active' : 'nav-link'} aria-current={item.id === sectionId ? 'page' : undefined}><span className="nav-symbol" aria-hidden="true">{item.symbol}</span>{item.label}<span className="nav-arrow" aria-hidden="true">↗</span></a>)}</nav>
      <div className="sidebar-bottom"><div className="phase-chip"><span className="status-dot" /> Fase III · Técnico</div><p>Investigación reproducible.<br />Sin conexión a mercados.</p><div className="identity"><span className="avatar">{session.principal.id.slice(0, 1).toUpperCase()}</span><div><strong>{session.principal.id}</strong><small>{session.principal.role}</small></div></div><button className="logout" onClick={logout} disabled={signingOut}>{signingOut ? 'Cerrando…' : 'Cerrar sesión'} <span aria-hidden="true">↗</span></button></div>
    </aside>
    <div className="workspace">
      <header className="topbar"><div><span className="breadcrumb">Plataforma</span><span className="separator">/</span><span>{section.label}</span></div><div className="topbar-actions"><span className="environment-tag"><span className="status-dot" /> Datos de prueba</span><button className="mobile-logout" onClick={logout} disabled={signingOut}>Cerrar sesión</button></div></header>
      <main id="main" tabIndex={-1}>
        <div className="page-heading"><div><p className="eyebrow">{section.kicker}</p><h1>{section.title}</h1><p className="page-subtitle">{section.description}</p></div><span className="phase-label">FASE III</span></div>
        <ErrorNotice error={error} />
        <View key={sectionId} session={session} />
        <footer className="workspace-footer"><span>bot_trader · Infraestructura de investigación · <a href="/THIRD_PARTY_NOTICES.txt" target="_blank" rel="noreferrer">Licencias</a></span><span>Resultados técnicos ≠ evidencia de rentabilidad</span></footer>
      </main>
    </div>
  </div>;
}
