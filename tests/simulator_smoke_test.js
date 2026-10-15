const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

let now = 0;
let loop;
const elements = new Map();
function el(id) {
  if (!elements.has(id)) elements.set(id, {
    id, value: '', textContent: '', style: {}, classList: {toggle() {}},
    handlers: {}, attributes: {},
    addEventListener(name, handler) { this.handlers[name] = handler; },
    setAttribute(name, value) { this.attributes[name] = value; },
    replaceChildren(...children) { this.children = children; },
    querySelector() { return el('info-paragraph'); },
    append() {}
  });
  return elements.get(id);
}
const document = {
  getElementById: el,
  querySelectorAll: () => [],
  createElement: () => ({append() {}, style: {}, textContent: ''}),
  createTextNode: text => text
};
vm.runInNewContext(fs.readFileSync('simulator/app.js', 'utf8'), {
  document,
  performance: {now: () => now},
  setInterval: callback => { loop = callback; }
});
function advance(seconds) {
  for (let i = 0; i < seconds * 10; i++) { now += 100; loop(); }
}
function click(id) { el(id).handlers.click(); }
function input(id, value) { el(id).handlers.input({target: {value: String(value)}}); }

assert.equal(el('statusLabel').textContent, 'Conditioning');
click('conditionButton');
assert.equal(el('statusLabel').textContent, 'Pemanasan');
click('warmupButton');
assert.equal(el('statusLabel').textContent, 'Baseline diperlukan');
click('baselineButton');
assert.equal(el('statusLabel').textContent, 'Mengambil baseline');
advance(7);
assert.equal(el('statusLabel').textContent, 'Normal');
assert.equal(el('indicatorLabel').textContent, 'Hijau menyala');
input('gasSlider', 500);
advance(1.3);
assert.equal(el('statusLabel').textContent, 'Respons meningkat');
assert.equal(el('indicatorLabel').textContent, 'Merah menyala');
input('gasSlider', 310);
advance(1.3);
assert.equal(el('statusLabel').textContent, 'Normal');
click('resetButton');
assert.equal(el('statusLabel').textContent, 'Conditioning');
console.log('Alur conditioning, baseline, hysteresis, LED, dan reset: OK');
