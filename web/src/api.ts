import type { Json, Session } from './types';

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
    public readonly correlationId?: string,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/** Session secrets stay in memory; authentication itself uses an HttpOnly cookie. */
export class ApiClient {
  private csrf: string | undefined;
  onUnauthorized?: () => void;

  setSession(session: Session | null): void {
    this.csrf = session?.csrf;
  }

  async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    if (!path.startsWith('/api/') || path.includes('://')) {
      throw new Error('API requests must use same-origin platform routes.');
    }
    const method = options.method ?? 'GET';
    const headers = new Headers(options.headers);
    if (options.body) headers.set('Content-Type', 'application/json');
    if (!['GET', 'HEAD'].includes(method) && this.csrf) headers.set('X-CSRF-Token', this.csrf);
    const response = await fetch(path, { ...options, method, headers, credentials: 'same-origin' });
    if (!response.ok) {
      const failure = await response.json().catch(() => ({})) as {
        error?: { code?: string; message?: string; correlation_id?: string };
      };
      if (response.status === 401) this.onUnauthorized?.();
      throw new ApiError(
        response.status,
        failure.error?.code ?? 'request_failed',
        failure.error?.message ?? `La solicitud no se completó (HTTP ${response.status}).`,
        failure.error?.correlation_id,
      );
    }
    return await response.json() as T;
  }

  async mutate<T>(path: string, data: Json, method = 'POST'): Promise<T> {
    return this.request<T>(path, { method, body: JSON.stringify(data) });
  }
}

export const api = new ApiClient();
