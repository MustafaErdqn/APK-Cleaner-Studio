import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import test from 'node:test';

const source = await readFile(new URL('../studio/web/app.js', import.meta.url), 'utf8');
const renderer = source.slice(source.indexOf('function renderMessageCandidates('), source.indexOf('function openMessageReview('));
function render(rows, selected = []) {
  const list = { innerHTML: '', insertAdjacentHTML(position, html) { this.innerHTML += html; } };
  const context = vm.createContext({
    state: { messageTargets: selected }, $: () => list,
    escapeHTML: value => String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;'),
    shortDexClass: value => value, rows
  });
  vm.runInContext(renderer + ';renderMessageCandidates(rows)', context);
  return list.innerHTML;
}
const rows = [
  { id: 'toast', kind: 'Toast', focus: 'priority', location: 'before_super' },
  { id: 'dialog', kind: 'Diyalog', focus: 'priority', location: 'before_super' },
  { id: 'original', kind: 'Diyalog', focus: 'other', confidence: 'review' }
];
test('two focused candidates are visible and other calls are collapsed without auto-selection', () => {
  const html = render(rows);
  const [main, more] = html.split('<details class="message-other-results"');
  assert.match(main, /value="toast"/);
  assert.match(main, /value="dialog"/);
  assert.doesNotMatch(main, /value="original"/);
  assert.match(more, /value="original"/);
  assert.doesNotMatch(more.split('>')[0], /open/);
  assert.doesNotMatch(html, / checked/);
});
test('previous explicit selections in the advanced group remain visible', () => {
  const html = render(rows, ['original']);
  assert.match(html, /message-other-results" open/);
  assert.match(html, /value="original" checked/);
  assert.match(html, /1 seçili/);
});
test('no priority result is not presented as absence of messages', () => {
  const html = render(rows.slice(2));
  assert.match(html, /eklenmiş mesaj olmadığı anlamına gelmez/);
  assert.match(html, /message-other-results/);
  assert.doesNotMatch(render([]), /data-message-target/);
});
test('multi-signal review results are separated from likely internal calls', () => {
  const html = render([
    { id: 'review', kind: 'Diyalog', focus: 'review', assessment: 'needs_review', signals: ['Konum şüpheli.'] },
    { id: 'internal', kind: 'Toast', focus: 'other', assessment: 'likely_internal', signals: ['Ortak yardımcı.'] },
  ]);
  assert.match(html, /İncelenmesi gereken çağrılar/);
  assert.match(html, /Düşük olasılıklı uygulama içi çağrılar/);
  assert.match(html, /İnceleme gerekli/);
  assert.match(html, /Konum şüpheli/);
});
