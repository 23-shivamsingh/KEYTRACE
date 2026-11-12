const test = require('node:test');
const assert = require('node:assert/strict');
const m = require('./metrics.js');

test('categorizes key names without retaining text', () => {
  assert.equal(m.categorize('A'), 'letters');
  assert.equal(m.categorize('8'), 'numbers');
  assert.equal(m.categorize('Backspace'), 'editing');
  assert.equal(m.categorize('ArrowLeft'), 'navigation');
  assert.equal(m.categorize('Shift'), 'other');
});
test('formats duration and speed correctly', () => {
  assert.equal(m.timerText(61000), '01:01');
  assert.equal(m.estimateWpm(50, 60000), 10);
  assert.equal(m.estimateWpm(20, 0), 0);
});
test('export contains aggregate counts but no typed content', () => {
  const result = m.anonymousExport({...m.initialCounts(), letters: 5}, 30000, 5, 2);
  assert.equal(result.categories.letters, 5);
  assert.equal(result.events, 5);
  assert.equal('characters' in result, false);
  assert.equal('raw_text' in result, false);
});
