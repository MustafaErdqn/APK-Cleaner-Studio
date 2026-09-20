/* Local QA only: finite frame/geometry sampling, never shipped with the app. */
(() => {
  let sampling = 0;
  document.addEventListener('click', (event) => {
    if (!event.target.closest('button, summary, label, a')) return;
    cancelAnimationFrame(sampling);
    const start = performance.now();
    const frames = [], widths = [], dialogWidths = [], dialogScales = [];
    function sample(now) {
      frames.push(now);
      widths.push(document.body.getBoundingClientRect().width);
      const dialog = document.querySelector('.app-dialog:not(.hidden) [role=dialog], .report-viewer:not(.hidden) [role=dialog]');
      if (dialog) {
        dialogWidths.push(dialog.getBoundingClientRect().width);
        dialogScales.push(getComputedStyle(dialog).transform);
      }
      if (now - start < 650) { sampling = requestAnimationFrame(sample); return; }
      const gaps = frames.slice(1).map((t, i) => t - frames[i]);
      const range = values => values.length ? +(Math.max(...values) - Math.min(...values)).toFixed(3) : 0;
      document.documentElement.dataset.qaMotion = JSON.stringify({
        label: event.target.textContent.trim().slice(0, 60), frames: frames.length,
        maxFrameGap: gaps.length ? +Math.max(...gaps).toFixed(2) : null,
        bodyWidthChange: range(widths), dialogWidthChange: range(dialogWidths),
        dialogTransforms: [...new Set(dialogScales)],
      });
    }
    sampling = requestAnimationFrame(sample);
  }, true);
})();
