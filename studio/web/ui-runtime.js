/* Shared, dependency-free presentation helpers. No remote assets or timers at idle. */
(() => {
  "use strict";
  // Elapsed time, not frames: identical speed on 60/90/120/144 Hz displays.
  function advanceProgress(current, target, elapsedMs) {
    return Math.min(target, current + Math.max(0, Math.min(80, elapsedMs)) / 24);
  }
  function selectClientId(cookieId, storedId, generate) {
    const valid = (value) => /^[A-Za-z0-9._:-]{8,80}$/.test(String(value || ""));
    if (valid(cookieId)) return cookieId;
    if (valid(storedId)) return storedId;
    const generated = generate();
    if (!valid(generated)) throw new Error("Invalid generated client id");
    return generated;
  }
  function createScheduler({ setTimer = setTimeout, clearTimer = clearTimeout } = {}) {
    const tasks = new Map();
    let active = false;
    function schedule(task) {
      if (!active || task.running || task.timer !== null) return;
      task.timer = setTimer(async () => {
        task.timer = null;
        if (!active) return;
        task.running = true;
        try { await task.run(); } catch { /* The task owns its user-facing errors. */ }
        finally { task.running = false; schedule(task); }
      }, task.delay);
    }
    return {
      add(name, run, delay) {
        if (tasks.has(name)) throw new Error("Duplicate UI task: " + name);
        const task = { run, delay, running: false, timer: null };
        tasks.set(name, task); schedule(task);
      },
      setActive(value) {
        active = Boolean(value);
        for (const task of tasks.values()) {
          if (active) schedule(task);
          else if (task.timer !== null) { clearTimer(task.timer); task.timer = null; }
        }
      },
    };
  }

  function createModalMotion({ reduced = () => false, desktop = () => false, setTimer = setTimeout, clearTimer = clearTimeout } = {}) {
    const pending = new Map();
    const returns = new WeakMap();
    function cancel(element) {
      const entry = pending.get(element);
      if (!entry) return;
      pending.delete(element);
      clearTimer(entry.timer);
      entry.animation?.cancel();
    }
    function transition(element, closing, done) {
      cancel(element);
      const card = element.querySelector('[role="dialog"]');
      if (!card?.animate || reduced()) { done?.(); return; }
      // Desktop text remains at its native raster size throughout the fade.
      const stationary = desktop();
      const frames = stationary ? (closing ? [{ opacity: 1 }, { opacity: 0 }] : [{ opacity: 0 }, { opacity: 1 }]) : closing
        ? [{ opacity: 1, transform: "translateY(0) scale(1)" }, { opacity: 0, transform: "translateY(8px) scale(.985)" }]
        : [{ opacity: 0, transform: "translateY(10px) scale(.985)" }, { opacity: 1, transform: "translateY(0) scale(1)" }];
      const duration = stationary ? (closing ? 140 : 180) : (closing ? 160 : 240);
      const entry = { animation: null, timer: null, done };
      pending.set(element, entry);
      const finish = () => {
        if (pending.get(element) !== entry) return;
        pending.delete(element); clearTimer(entry.timer);
        done?.();
        entry.animation?.cancel();
      };
      entry.animation = card.animate(frames, { duration, easing: "cubic-bezier(.22,.61,.36,1)", fill: "both" });
      entry.animation.finished.then(finish, () => {});
      entry.timer = setTimer(finish, duration + 100);
    }
    return {
      open(element) {
        if (element.classList.contains("hidden")) returns.set(element, element.ownerDocument?.activeElement);
        element.classList.remove("hidden", "is-closing");
        const card = element.querySelector('[role="dialog"]');
        if (card) card.inert = false;
        element.setAttribute("aria-hidden", "false");
        transition(element, false);
      },
      close(element, done) {
        if (element.classList.contains("hidden")) { done?.(); return; }
        if (element.classList.contains("is-closing")) return;
        element.classList.add("is-closing");
        const card = element.querySelector('[role="dialog"]');
        if (card) card.inert = true;
        transition(element, true, () => {
          element.classList.add("hidden"); element.classList.remove("is-closing");
          element.setAttribute("aria-hidden", "true");
          if (card) card.inert = false;
          done?.();
          const target = returns.get(element);
          if (target?.isConnected && !element.ownerDocument?.querySelector('.app-dialog:not(.hidden), .report-viewer:not(.hidden)')) {
            target.focus?.({ preventScroll: true });
          }
        });
      },
      settle() {
        for (const [element, entry] of [...pending]) { cancel(element); entry.done?.(); }
      },
    };
  }

  // Original geometric identifiers, not representations of official brand artwork.
  // Fixed SVG paths only: analysis labels never become SVG markup or asset URLs.
  const badges = {
    google_ads: ["blue", "M7 22 16 6l9 16M11 17h10", "4"],
    applovin: ["violet", "M6 23 13 8l7 15M16 8l9 15M10 18h7", "3"],
    vungle: ["orange", "m6 8 10 17L26 8M11 8l5 9 5-9", "3"],
    pangle: ["coral", "M9 25V7h8a6 6 0 0 1 0 12h-3M14 11h3a2 2 0 0 1 0 4h-3", "3"],
    inmobi: ["blue", "M8 13v11m8-11v11m8-11v11M8 7h0m8 0h0m8 0h0", "4"],
    unity_ads: ["slate", "m16 4 11 6v12l-11 6-11-6V10ZM5 10l11 6 11-6M16 16v12", "2.5"],
    ironsource: ["violet", "m5 11 11-6 11 6-11 6ZM5 17l11 6 11-6M5 23l11 6 11-6", "2.5"],
    mintegral: ["teal", "M5 24V8l11 9L27 8v16M10 24v-6l6 5 6-5v6", "3"],
    fyber: ["orange", "M8 25V7h17M8 15h13M18 22l7-7", "3.5"],
    ogury: ["violet", "M25 16a9 9 0 1 1-4-7M16 7v9h9", "3"],
    facebook_ads: ["blue", "M4 20C4 5 11 5 16 16s12 12 12 2C28 5 22 5 16 16S4 28 4 20Z", "2.8"],
    startapp: ["teal", "m16 4 3 8 9 1-7 6 2 9-7-5-7 5 2-9-7-6 9-1Z", "2.3"],
    chartboost: ["teal", "M7 25v-9m9 9V10m9 15V5M5 11l8-5h8", "3.5"],
    adcolony: ["coral", "m16 4 12 21H4ZM11 21l5-9 5 9", "2.5"],
    tapjoy: ["orange", "M7 9h18M16 9v17M7 19v3m18-3v3M10 5h12", "3.5"],
    smaato: ["violet", "M25 7H12a6 6 0 0 0 0 12h8a3 3 0 0 1 0 6H7M23 13H12", "3"],
    yandex_ads: ["coral", "M24 26V6h-7a7 7 0 0 0 0 14h7M16 20l-8 6", "3"],
    amazon_ads: ["orange", "M8 19 16 5l8 14M12 14h8M5 23q11 8 22-1m-5-1 5 1-2 5", "2.5"],
  };
  function networkBadge(key) {
    const [tone, path, width] = Object.prototype.hasOwnProperty.call(badges, key) ? badges[key]
      : ["slate", "M16 4 28 16 16 28 4 16ZM11 16h10M16 11v10", "2.5"];
    return '<span class="network-badge tone-' + tone + '" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="' + width + '" stroke-linecap="round" stroke-linejoin="round" focusable="false"><path d="' + path + '"/></svg></span>';
  }
  globalThis.StudioUI = Object.freeze({ createScheduler, createModalMotion, networkBadge, advanceProgress, selectClientId });
})();
