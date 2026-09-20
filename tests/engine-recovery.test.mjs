import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const script = await readFile(new URL('../studio/web/app.js', import.meta.url), 'utf8');
const helpers = script.slice(script.indexOf('async function recoverEmbeddedEngine()'), script.indexOf('async function resolvePublicIpv4()'));
function runtime(fetch, platform = 'android') {
  let starts = 0;
  const context = vm.createContext({ fetch, AbortController, DOMException, setTimeout, clearTimeout,
    document: { documentElement: { dataset: { embedded: platform } } },
    AndroidThemeBridge: { ensureEngine() { starts++; } }, clientHeaders: () => ({}) });
  vm.runInContext('let embeddedEngineRecoveryTask = null;\n' + helpers, context);
  return { context, starts: () => starts };
}

test('concurrent reads join one recovery and retry only once', async () => {
  const counts = new Map();
  const { context, starts } = runtime(async (url) => {
    const count = (counts.get(url) || 0) + 1; counts.set(url, count);
    if (url !== '/api/status' && count === 1) throw new TypeError('Failed to fetch');
    return { ok: true };
  });
  await Promise.all([context.apiFetch('/api/history'), context.apiFetch('/api/jobs/id/state')]);
  assert.equal(starts(), 1);
  assert.equal(counts.get('/api/history'), 2);
  assert.equal(counts.get('/api/jobs/id/state'), 2);
});

test('lost mutation response never resends an upload or patch', async () => {
  const calls = [];
  const { context } = runtime(async (url) => {
    calls.push(url);
    if (url === '/api/status') return { ok: true };
    throw new TypeError('Lost response after submission');
  });
  await assert.rejects(context.apiFetch('/api/clean', { method: 'POST', body: '{}' }), /Lost response/);
  assert.deepEqual(calls, ['/api/status', '/api/clean']);
});

test('web platforms do not invoke the Android service', async () => {
  const { context, starts } = runtime(async () => { throw new TypeError('offline'); }, 'web');
  await assert.rejects(context.apiFetch('/api/history'), /offline/);
  assert.equal(starts(), 0);
});

test('aborted background reads do not wake the engine', async () => {
  const { context, starts } = runtime(async () => { throw new DOMException('aborted', 'AbortError'); });
  await assert.rejects(context.apiFetch('/api/history'), { name: 'AbortError' });
  assert.equal(starts(), 0);
});
