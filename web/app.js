(function () {
  'use strict';
  const metric = window.KeytraceMetrics;
  const $ = id => document.getElementById(id);
  const dom = {
    consent: $('consent'), pad: $('typingPad'), start: $('startBtn'), stop: $('stopBtn'),
    reset: $('resetBtn'), export: $('exportBtn'), total: $('totalCount'), wpm: $('wpmCount'),
    time: $('timeCount'), status: $('sessionLabel'), badge: $('liveBadge'), recDot: $('recDot'),
    feed: $('eventFeed'), feedCount: $('feedCount'), canvas: $('activityCanvas'),
  };
  let active = false;
  let startedAt = 0;
  let stoppedElapsedMs = 0;
  let count = 0;
  let categories = metric.initialCounts();
  let events = [];
  let timeline = [];
  const colors = { letters: 'green', numbers: 'blue', editing: 'yellow', navigation: 'purple', other: 'slate' };
  const labels = { letters: 'Letter input', numbers: 'Numeric input', editing: 'Editing control', navigation: 'Navigation key', other: 'Other control' };

  function elapsedMs() { return active ? Math.max(0, performance.now() - startedAt) : stoppedElapsedMs; }
  function wpm() { return metric.estimateWpm(count, elapsedMs()); }
  function setButtons() {
    dom.start.disabled = active || !dom.consent.checked;
    dom.stop.disabled = !active;
    dom.export.disabled = count === 0;
    dom.pad.disabled = !active;
    dom.pad.placeholder = active ? 'Type sample text here. No raw characters are stored in event history.' : 'Your test playground is locked. Start a session to try it.';
    dom.status.innerHTML = (active ? 'Live' : count > 0 ? 'Stopped' : 'Ready') + '<span class="status-small-dot"></span>';
    dom.status.classList.toggle('status-live', active);
    dom.badge.textContent = active ? 'RECORDING IN FIELD' : 'NOT RECORDING';
    dom.recDot.classList.toggle('active', active);
  }
  function updateMetrics() {
    dom.total.innerHTML = `${count}<span class="metric-unit">events</span>`;
    dom.wpm.innerHTML = `${wpm()}<span class="metric-unit">WPM</span>`;
    dom.time.textContent = metric.timerText(elapsedMs());
    for (const key of metric.CATEGORIES) {
      const row = document.querySelector(`[data-category="${key}"]`);
      const value = categories[key];
      row.querySelector('strong').textContent = String(value);
      row.querySelector('.bar-fill').style.width = `${count ? (value / count) * 100 : 0}%`;
    }
  }
  function renderFeed() {
    dom.feedCount.textContent = String(Math.min(events.length, 6)).padStart(2, '0');
    if (!events.length) {
      dom.feed.innerHTML = '<div class="empty-feed"><div class="empty-icon">◌</div><strong>Ready when you are</strong><p>Input events will appear here once you start your session.</p></div>';
      return;
    }
    dom.feed.replaceChildren();
    for (const event of [...events].slice(-6).reverse()) {
      const row = document.createElement('div');
      row.className = 'feed-event';
      const left = document.createElement('div');
      left.className = 'event-name';
      const dot = document.createElement('span');
      dot.className = `event-icon ${colors[event.category]}`;
      dot.textContent = event.category === 'editing' ? '⌫' : event.category === 'navigation' ? '↔' : '⌁';
      const text = document.createElement('span');
      text.textContent = labels[event.category];
      left.append(dot, text);
      const when = document.createElement('span');
      when.className = 'event-time';
      when.textContent = `+${(event.ms / 1000).toFixed(1)}s`;
      row.append(left, when);
      dom.feed.append(row);
    }
  }
  function start() {
    if (active || !dom.consent.checked) return;
    count = 0;
    categories = metric.initialCounts();
    events = [];
    timeline = [];
    startedAt = performance.now();
    stoppedElapsedMs = 0;
    active = true;
    dom.pad.value = '';
    setButtons(); updateMetrics(); renderFeed(); drawChart(); dom.pad.focus();
  }
  function stop() {
    if (!active) return;
    stoppedElapsedMs = elapsedMs();
    active = false;
    dom.pad.value = ''; // Wipe the visible sample text on stop.
    setButtons(); updateMetrics(); drawChart();
  }
  function reset() {
    if (active) stop();
    count = 0; categories = metric.initialCounts(); events = []; timeline = [];
    stoppedElapsedMs = 0; dom.pad.value = '';
    setButtons(); updateMetrics(); renderFeed(); drawChart();
  }
  function record(event) {
    if (!active || event.target !== dom.pad || event.isComposing) return;
    const category = metric.categorize(event.key);
    const ms = elapsedMs();
    count++;
    categories[category]++;
    events.push({ category, ms });
    if (events.length > 6) events.shift();
    timeline.push(ms);
    if (timeline.length > 3000) timeline.shift();
    renderFeed(); updateMetrics(); drawChart();
  }
  function activityPoints() {
    const end = elapsedMs();
    const points = Array(30).fill(0);
    for (const ms of timeline) {
      const ago = Math.floor((end - ms) / 1000);
      if (ago >= 0 && ago < 30) points[29 - ago]++;
    }
    return points;
  }
  function drawChart() {
    const canvas = dom.canvas;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const size = canvas.getBoundingClientRect();
    if (!size.width || !size.height) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(size.width * dpr);
    canvas.height = Math.floor(size.height * dpr);
    ctx.scale(dpr, dpr);
    const w = size.width, h = size.height, inset = 8;
    ctx.strokeStyle = '#29394b'; ctx.lineWidth = 1;
    for (let i = 1; i <= 3; i++) {
      const y = (h / 4) * i;
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }
    const points = activityPoints();
    const peak = Math.max(3, ...points);
    const xFor = i => inset + i * ((w - 2 * inset) / (points.length - 1));
    const yFor = value => h - inset - (value / peak) * (h - 2 * inset);
    const gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, 'rgba(197, 250, 120, .32)');
    gradient.addColorStop(1, 'rgba(197, 250, 120, 0)');
    ctx.beginPath();
    ctx.moveTo(xFor(0), h);
    points.forEach((value, i) => ctx.lineTo(xFor(i), yFor(value)));
    ctx.lineTo(xFor(points.length - 1), h);
    ctx.closePath(); ctx.fillStyle = gradient; ctx.fill();
    ctx.beginPath();
    points.forEach((value, i) => i === 0 ? ctx.moveTo(xFor(i), yFor(value)) : ctx.lineTo(xFor(i), yFor(value)));
    ctx.lineWidth = 2.7; ctx.strokeStyle = '#c5fa78'; ctx.stroke();
    const last = points[points.length - 1];
    ctx.beginPath(); ctx.arc(xFor(points.length - 1), yFor(last), 4, 0, Math.PI * 2); ctx.fillStyle = '#c5fa78'; ctx.fill();
  }
  function exportStats() {
    if (!count) return;
    const summary = metric.anonymousExport(categories, elapsedMs(), count, wpm());
    const file = new Blob([JSON.stringify(summary, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(file);
    const link = document.createElement('a');
    link.href = url; link.download = 'keytrace-statistics.json';
    document.body.append(link); link.click(); link.remove();
    URL.revokeObjectURL(url);
  }
  dom.consent.addEventListener('change', setButtons);
  dom.start.addEventListener('click', start);
  dom.stop.addEventListener('click', stop);
  dom.reset.addEventListener('click', reset);
  dom.export.addEventListener('click', exportStats);
  dom.pad.addEventListener('keydown', record);
  const links = Array.from(document.querySelectorAll('.nav-link'));
  links.forEach(link => link.addEventListener('click', () => {
    links.forEach(item => item.classList.remove('active'));
    link.classList.add('active');
  }));
  window.addEventListener('resize', drawChart);
  setInterval(() => { if (active) { updateMetrics(); drawChart(); } }, 500);
  setButtons(); updateMetrics(); renderFeed(); drawChart();
})();
