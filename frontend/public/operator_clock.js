window.heavyLogixClock = {
  stop() {
    if (this.interval) clearInterval(this.interval);
    if (this.observer) this.observer.disconnect();
    this.interval = null;
    this.observer = null;
  },
  mount() {
    this.stop();
    const node = document.getElementById('operator-elapsed');
    if (!node) return;
    const update = () => {
      if (!node.isConnected) { this.stop(); return; }
      const start = Date.parse(node.getAttribute('data-started-at') || '');
      const endValue = node.getAttribute('data-ended-at');
      const end = endValue ? Date.parse(endValue) : Date.now();
      const seconds = Number.isFinite(start) && Number.isFinite(end) ? Math.max(0, Math.floor((end - start) / 1000)) : 0;
      const values = [Math.floor(seconds / 3600), Math.floor(seconds / 60) % 60, seconds % 60];
      const text = values.map(n => String(n).padStart(2, '0')).join(':');
      if (node.textContent !== text) node.textContent = text;
    };
    update();
    this.interval = setInterval(update, 1000);
    this.observer = new MutationObserver(update);
    this.observer.observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['data-started-at', 'data-ended-at']});
  }
};
