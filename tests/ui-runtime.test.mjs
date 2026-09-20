import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import test from 'node:test';

const source = await readFile(new URL('../studio/web/ui-runtime.js', import.meta.url), 'utf8');
const context = vm.createContext({ setTimeout, clearTimeout });
vm.runInContext(source, context);
const { createScheduler, createModalMotion, networkBadge, advanceProgress, selectClientId } = context.StudioUI;

test('HTTP to HTTPS hand-off reuses the shared host identity', () => {
  let generated = 0;
  const create = () => { generated++; return 'new-client-12345'; };
  assert.equal(selectClientId('http-client-12345', '', create), 'http-client-12345');
  assert.equal(selectClientId('http-client-12345', 'stale-https-client', create), 'http-client-12345');
  assert.equal(selectClientId('', 'stored-client-123', create), 'stored-client-123');
  assert.equal(selectClientId('invalid cookie value', 'also invalid!', create), 'new-client-12345');
  assert.equal(generated, 1);
});

test('progress is time-based at 60, 90, 120 and 144 Hz without skipping frames', () => {
  for (const hz of [60, 90, 120, 144]) {
    let value = 0;
    for (let frame = 0; frame < hz; frame++) {
      const next = advanceProgress(value, 100, 1000 / hz);
      assert.ok(next > value, `${hz} Hz frame ${frame} was skipped`);
      value = next;
    }
    assert.ok(Math.abs(value - 1000 / 24) < 1e-8, `${hz} Hz changed animation speed`);
  }
  assert.equal(advanceProgress(99.9, 100, 16), 100);
  assert.equal(advanceProgress(100, 100, 16), 100);
  assert.equal(advanceProgress(10, 100, -5), 10);
});

test('rapid list toggles sample visible geometry before cancelling animation', async () => {
  const app = await readFile(new URL('../studio/web/app.js', import.meta.url), 'utf8');
  const body = app.slice(app.indexOf('function captureInstalledAppPositions('), app.indexOf('function animateInstalledAppReflow('));
  const sandbox = vm.createContext({ Map });
  vm.runInContext(body, sandbox);
  const events = [];
  const entry = { dataset:{installedEntry:'example'}, getBoundingClientRect(){events.push('read'); return {top:25,bottom:80};}, getAnimations(){return [{cancel(){events.push('cancel');}}];} };
  const result = sandbox.captureInstalledAppPositions({getBoundingClientRect:()=>({top:0,bottom:100}),querySelectorAll:()=>[entry]});
  assert.equal(result.get('example'),25);
  assert.deepEqual(events,['read','cancel']);
});

function clock() {
  let next = 0;
  const timers = new Map();
  return {
    timers,
    setTimer: (run) => { timers.set(++next, run); return next; },
    clearTimer: (id) => timers.delete(id),
    async tick() {
      const entries = [...timers];
      for (const [id, run] of entries) { if (timers.delete(id)) await run(); }
    },
  };
}

test('idle UI has zero periodic timers and resumes without duplication', async () => {
  const time = clock();
  const scheduler = createScheduler(time);
  let calls = 0;
  scheduler.add('status', () => calls++, 10000);
  scheduler.add('history', () => calls++, 30000);
  assert.equal(time.timers.size, 0);
  scheduler.setActive(true); scheduler.setActive(true);
  assert.equal(time.timers.size, 2);
  await time.tick(); assert.equal(calls, 2);
  scheduler.setActive(false); assert.equal(time.timers.size, 0);
  await time.tick(); assert.equal(calls, 2);
  scheduler.setActive(true); assert.equal(time.timers.size, 2);
  assert.throws(() => scheduler.add('status', () => {}, 10000), /Duplicate/);
});

test('an in-flight read cannot restart a timer while the UI is suspended', async () => {
  const time = clock();
  const scheduler = createScheduler(time);
  let release;
  scheduler.add('read', () => new Promise((resolve) => { release = resolve; }), 100);
  scheduler.setActive(true);
  const running = time.tick();
  scheduler.setActive(false);
  release(); await running;
  assert.equal(time.timers.size, 0);
  scheduler.setActive(true);
  assert.equal(time.timers.size, 1);
});

function modal() {
  const classes = new Set(['hidden']);
  const animations = [];
  const card = {
    inert: false,
    animate(frames, options) {
      let resolve;
      const animation = { frames, options, finished: new Promise((done) => { resolve = done; }), cancel() {} };
      animation.complete = resolve; animations.push(animation); return animation;
    },
  };
  const attributes = new Map();
  const element = {
    classList: { add: (...names) => names.forEach((n) => classes.add(n)), remove: (...names) => names.forEach((n) => classes.delete(n)), contains: (n) => classes.has(n) },
    querySelector: () => card,
    setAttribute: (key, value) => attributes.set(key, value),
  };
  return { element, classes, card, animations, attributes };
}

test('modal exit keeps scroll lock until the animation finishes', async () => {
  const time = clock(); const motion = createModalMotion(time); const m = modal();
  let unlocks = 0;
  motion.open(m.element);
  m.animations[0].complete(); await Promise.resolve();
  motion.close(m.element, () => unlocks++);
  assert.equal(m.classes.has('hidden'), false);
  assert.equal(m.card.inert, true);
  assert.equal(unlocks, 0);
  m.animations[1].complete(); await Promise.resolve();
  assert.equal(unlocks, 1);
  assert.equal(m.classes.has('hidden'), true);
  assert.equal(time.timers.size, 0);
});

test('desktop modals fade without scaling text; mobile retains the slide', async () => {
  const time = clock(); const m = modal();
  let desktop = true;
  const motion = createModalMotion({ ...time, desktop: () => desktop });
  motion.open(m.element);
  assert.equal(m.animations[0].options.duration, 180);
  assert.ok(m.animations[0].frames.every(frame => !('transform' in frame)));
  motion.close(m.element);
  assert.equal(m.animations[1].options.duration, 140);
  assert.ok(m.animations[1].frames.every(frame => !('transform' in frame)));
  m.animations[1].complete(); await Promise.resolve();
  desktop = false; motion.open(m.element);
  assert.match(m.animations[2].frames[0].transform, /translateY/);
  assert.equal(m.animations[2].options.duration, 240);
});

test('rapid reopen cancels stale exit and does not unlock the new dialog', async () => {
  const time = clock(); const motion = createModalMotion(time); const m = modal();
  let unlocks = 0;
  motion.open(m.element);
  motion.close(m.element, () => unlocks++);
  const stale = m.animations[1];
  motion.open(m.element);
  stale.complete(); await Promise.resolve(); await time.tick();
  assert.equal(unlocks, 0);
  assert.equal(m.classes.has('hidden'), false);
  assert.equal(m.card.inert, false);
});

test('duplicate close and missing animation completion are safe', async () => {
  const time = clock(); const motion = createModalMotion(time); const m = modal();
  let unlocks = 0;
  motion.open(m.element);
  motion.close(m.element, () => unlocks++);
  motion.close(m.element, () => unlocks++);
  await time.tick(); assert.equal(unlocks, 1);
  assert.equal(m.classes.has('hidden'), true);
});

test('reduced motion and background settling do not leave stuck popups', () => {
  const time = clock(); const m = modal();
  const reduced = createModalMotion({ ...time, reduced: () => true });
  let unlocks = 0;
  reduced.open(m.element); reduced.close(m.element, () => unlocks++);
  assert.equal(m.animations.length, 0); assert.equal(unlocks, 1);
  const motion = createModalMotion(time);
  motion.open(m.element); motion.close(m.element, () => unlocks++); motion.settle();
  assert.equal(m.classes.has('hidden'), true); assert.equal(unlocks, 2);
  assert.equal(time.timers.size, 0);
});

test('all 18 detected networks have distinct local vector identifiers', async () => {
  const profiles = JSON.parse(await readFile(new URL('../studio/profiles.json', import.meta.url), 'utf8'));
  const marks = Object.keys(profiles).map(networkBadge);
  assert.equal(new Set(marks).size, 18);
  for (const mark of marks) {
    assert.match(mark, /<svg/); assert.match(mark, /aria-hidden="true"/);
    assert.doesNotMatch(mark, /https?:|<img|<script|<text/);
  }
  assert.equal(networkBadge('__proto__'), networkBadge('unknown'));
  assert.doesNotMatch(networkBadge('<script>alert(1)</script>'), /<script/);
});

test('shared page and native shell wire visibility without pausing the engine', async () => {
  const script = await readFile(new URL('../studio/web/app.js', import.meta.url), 'utf8');
  const html = await readFile(new URL('../studio/web/index.html', import.meta.url), 'utf8');
  const java = await readFile(new URL('../android/app/src/main/java/com/apkcleaner/studio/MainActivity.java', import.meta.url), 'utf8');
  assert.match(html, /ui-runtime\.js[\s\S]*app\.js/);
  assert.doesNotMatch(script, /setInterval\(/);
  assert.match(script, /await waitForUiActive\(\)/);
  assert.match(script, /uiReadController\.abort\(\)/);
  assert.match(script, /renderHistory\.signature === signature/);
  assert.match(java, /onPause\(\)[\s\S]*?webView\.onPause\(\)/);
  assert.match(java, /onResume\(\)[\s\S]*?webView\.onResume\(\)/);
  assert.doesNotMatch(java, /webView\.pauseTimers\(/);
});
