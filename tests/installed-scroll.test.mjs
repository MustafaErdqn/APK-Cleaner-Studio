import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import test from 'node:test';

const source = await readFile(new URL('../studio/web/app.js', import.meta.url), 'utf8');
function fixture() {
  const timers = new Map(), scrolls = [];
  let next = 0;
  const list = { scrollTop: 100, getBoundingClientRect: () => ({top: 0, bottom: 200}), scrollTo: options => scrolls.push(options) };
  const entry = { isConnected: true, classList: { contains: () => true }, getBoundingClientRect: () => ({top: 150, bottom: 260}) };
  const modal = { matches: () => false };
  const sandbox = vm.createContext({
    $: selector => selector === '#installedAppsList' ? list : modal,
    isUiActive: () => true, motionMedia: {matches: false},
    setTimeout: run => {timers.set(++next, run); return next;}, clearTimeout: id => timers.delete(id),
  });
  vm.runInContext(source.slice(source.indexOf('let installedRevealTimer'), source.indexOf('function captureInstalledAppPositions')), sandbox);
  return { ...sandbox, list, entry, scrolls, timers, tick() { for (const [id, run] of [...timers]) {timers.delete(id); run();} } };
}

test('new finger/wheel interaction cancels a pending reveal on every gesture', () => {
  const f = fixture();
  for (let i = 0; i < 3; i++) {
    f.scheduleInstalledAppReveal(f.list, f.entry);
    f.cancelInstalledAppReveal(); f.tick();
    assert.equal(f.scrolls.length, 0);
  }
  assert.match(source, /\["pointerdown", "touchstart", "wheel", "keydown"\]/);
  assert.match(source, /addEventListener\(name, cancelInstalledAppReveal, \{ passive: true \}\)/);
});

test('reveal targets only list; user interruption stops its smooth scroll once', () => {
  const f = fixture(); f.scheduleInstalledAppReveal(f.list, f.entry); f.tick();
  assert.equal(f.scrolls[0].top, 160); assert.equal(f.scrolls[0].behavior, 'smooth');
  f.cancelInstalledAppReveal(); f.cancelInstalledAppReveal();
  assert.equal(f.scrolls.length, 2); assert.equal(f.scrolls[1].behavior, 'instant');
  assert.equal(f.scrolls[1].top, 100);
});

test('reselection replaces timer and detached/visible rows are not scrolled', () => {
  const f = fixture();
  f.scheduleInstalledAppReveal(f.list, f.entry); f.scheduleInstalledAppReveal(f.list, f.entry);
  assert.equal(f.timers.size, 1);
  f.entry.isConnected = false; f.tick(); assert.equal(f.scrolls.length, 0);
  f.entry.isConnected = true; f.entry.getBoundingClientRect = () => ({top: 40,bottom: 100});
  f.scheduleInstalledAppReveal(f.list, f.entry); f.tick(); assert.equal(f.scrolls.length, 0);
});

test('modern CSS scroll containment avoids a blocking touch listener; legacy fallback remains', () => {
  const handlers = [];
  const sandbox = vm.createContext({CSS: {supports: () => true}, $: () => ({addEventListener: (...args) => handlers.push(args)})});
  vm.runInContext(source.slice(source.indexOf('function containModalTouch'), source.indexOf('function closeAppDialog')), sandbox);
  sandbox.containModalTouch('#modal', '.list'); assert.equal(handlers.length, 0);
  sandbox.CSS.supports = () => false;
  sandbox.containModalTouch('#modal', '.list'); assert.equal(handlers.length, 1);
  let prevented = 0;
  handlers[0][1]({target: {closest: () => ({})}, preventDefault: () => prevented++});
  assert.equal(prevented, 0);
  handlers[0][1]({target: {closest: () => null}, preventDefault: () => prevented++});
  assert.equal(prevented, 1);
});

test('progress breathing preserves reduced motion and background pause', async () => {
  const css = await readFile(new URL('../studio/web/theme.css', import.meta.url), 'utf8');
  assert.doesNotMatch(css, /progress-orbit|progress-breathe|\.progress-ring::before/);
  assert.match(css, /prefers-reduced-motion: reduce[\s\S]*?\.progress-ring,[\s\S]*?animation: none/);
  assert.match(css, /html\.ui-suspended \*::after,[\s\S]*?animation-play-state: paused/);
  assert.match(css, /body\.modal-scroll-locked > main \*[\s\S]*?animation-play-state: paused/);
});
