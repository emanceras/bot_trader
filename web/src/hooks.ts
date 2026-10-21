import { useCallback, useEffect, useState } from 'react';
import { api } from './api';

/** Abort old queries on navigation and polling; never let a stale response replace new data. */
export function useResource<T>(path: string | null, refreshSeconds = 0) {
  const [revision, setRevision] = useState(0);
  const [state, setState] = useState<{ data: T | null; error: Error | null; loading: boolean }>({
    data: null, error: null, loading: Boolean(path),
  });
  const refresh = useCallback(() => setRevision(value => value + 1), []);
  useEffect(() => {
    if (!path) {
      setState({ data: null, error: null, loading: false });
      return;
    }
    const controller = new AbortController();
    setState(previous => ({ ...previous, error: null, loading: true }));
    api.request<T>(path, { signal: controller.signal }).then(
      data => { if (!controller.signal.aborted) setState({ data, error: null, loading: false }); },
      error => { if (!controller.signal.aborted) setState({ data: null, error, loading: false }); },
    );
    return () => controller.abort();
  }, [path, revision]);
  useEffect(() => {
    if (!refreshSeconds) return;
    const timer = window.setInterval(refresh, refreshSeconds * 1000);
    return () => window.clearInterval(timer);
  }, [refresh, refreshSeconds]);
  return { ...state, refresh };
}
