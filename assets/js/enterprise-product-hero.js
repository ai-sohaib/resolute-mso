(() => {
  const dashboard = document.querySelector('[data-rcm-dashboard]');
  if (!dashboard) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const counters = Array.from(dashboard.querySelectorAll('[data-kpi-value]'));

  const reveal = () => {
    dashboard.classList.add('is-visible');
    if (reduceMotion) return;

    counters.forEach((counter) => {
      const target = Number(counter.dataset.kpiValue || 0);
      const decimals = Number(counter.dataset.kpiDecimals || 0);
      const prefix = counter.dataset.kpiPrefix || '';
      const suffix = counter.dataset.kpiSuffix || '';
      const duration = 700;
      const start = performance.now();

      const tick = (time) => {
        const progress = Math.min((time - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = target * eased;
        counter.textContent = `${prefix}${value.toFixed(decimals)}${suffix}`;
        if (progress < 1) requestAnimationFrame(tick);
      };

      requestAnimationFrame(tick);
    });
  };

  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveal();
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    if (!entries.some((entry) => entry.isIntersecting)) return;
    reveal();
    observer.disconnect();
  }, { threshold: 0.18 });

  observer.observe(dashboard);
})();
