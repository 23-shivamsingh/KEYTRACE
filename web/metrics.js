/* Portable privacy-safe keyboard metrics. Browser global + CommonJS test export. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.KeytraceMetrics = api;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';
  const CATEGORIES = ['letters', 'numbers', 'editing', 'navigation', 'other'];
  const editing = new Set(['Backspace', 'Delete', 'Enter', 'Tab', ' ']);
  const navigation = new Set(['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End', 'PageUp', 'PageDown', 'Escape']);
  function categorize(key) {
    if (editing.has(key)) return 'editing';
    if (navigation.has(key)) return 'navigation';
    if (typeof key === 'string' && key.length === 1 && /\p{L}/u.test(key)) return 'letters';
    if (typeof key === 'string' && key.length === 1 && /\p{N}/u.test(key)) return 'numbers';
    return 'other';
  }
  function initialCounts() { return Object.fromEntries(CATEGORIES.map(category => [category, 0])); }
  function estimateWpm(events, elapsedMs) { return elapsedMs > 0 ? Math.round((events / 5) / (elapsedMs / 60000)) : 0; }
  function timerText(elapsedMs) {
    const seconds = Math.floor(Math.max(0, elapsedMs) / 1000);
    return String(Math.floor(seconds / 60)).padStart(2, '0') + ':' + String(seconds % 60).padStart(2, '0');
  }
  function anonymousExport(counts, elapsedMs, keyCount, wpm) {
    return {
      project: 'KEYTRACE | Keyboard Event Lab',
      note: 'Aggregated events only. No typed characters or input contents.',
      duration_seconds: Math.round(elapsedMs / 1000),
      events: keyCount,
      estimated_wpm: wpm,
      categories: { ...counts }
    };
  }
  return { CATEGORIES, categorize, initialCounts, estimateWpm, timerText, anonymousExport };
});
