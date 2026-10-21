import { ApiClient, ApiError } from './api';

describe('same-origin authenticated client', () => {
  it('uses an HttpOnly cookie session and adds CSRF only to mutations', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('{}', { status: 200 }));
    const client = new ApiClient();
    client.setSession({ principal: { id: 'tester', role: 'researcher' }, csrf: 'csrf-test' });
    await client.mutate('/api/datasets', { rows: 10 });
    const options = fetchMock.mock.calls[0][1]!;
    expect(options.credentials).toBe('same-origin');
    expect(new Headers(options.headers).get('X-CSRF-Token')).toBe('csrf-test');
    expect(new Headers(options.headers).has('Authorization')).toBe(false);
    expect(window.localStorage.length).toBe(0);
    fetchMock.mockResolvedValue(new Response('{}', { status: 200 }));
    await client.request('/api/modules');
    expect(new Headers(fetchMock.mock.calls[1][1]?.headers).has('X-CSRF-Token')).toBe(false);
    await expect(client.request('https://example.com/api/datasets')).rejects.toThrow('same-origin');
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('preserves safe errors and expires the session only for unauthorized responses', async () => {
    const unauthorized = vi.fn();
    const client = new ApiClient();
    client.onUnauthorized = unauthorized;
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify({ error: { code: 'reserved', message: 'Payload reserved.', correlation_id: 'correlation-123' } }), { status: 403 }));
    await expect(client.request('/api/datasets/reserved/series')).rejects.toMatchObject({ status: 403, code: 'reserved', correlationId: 'correlation-123' });
    expect(unauthorized).not.toHaveBeenCalled();
    fetchMock.mockResolvedValue(new Response('{}', { status: 401 }));
    await expect(client.request('/api/session')).rejects.toBeInstanceOf(ApiError);
    expect(unauthorized).toHaveBeenCalledOnce();
  });
});
