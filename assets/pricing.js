/* Pricing widget for /pricing/: audience tabs, a monthly/yearly switch and up to three plan cards per tab.
   Data comes from <script id="pricing-data"> (written by _build/pricing.py). No dependencies; the confetti on
   switching to yearly loads canvas-confetti from jsDelivr only when needed and is skipped for reduced motion. */
(function () {
  var root = document.querySelector('[data-pricing]');
  var src = document.getElementById('pricing-data');
  if (!root || !src) return;
  var D = JSON.parse(src.textContent), T = D.t;
  var fmt = new Intl.NumberFormat(D.locale, { maximumFractionDigits: 0 });
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var state = { tab: D.tabs[0].id, yearly: false };
  try { var saved = sessionStorage.getItem('td_pricing_tab'); if (saved && D.tabs.some(function (t) { return t.id === saved; })) state.tab = saved; } catch (e) {}
  var hash = location.hash.replace('#', ''); if (D.tabs.some(function (t) { return t.id === hash; })) state.tab = hash;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var CHECK = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var STAR = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5l1.9 4 4.3.5-3.2 3 .9 4.3L8 11.1 4.1 13.3 5 9 1.8 6l4.3-.5z" fill="currentColor"/></svg>';

  function priceOf(c) {
    if (c.free) return { value: 0, per: '', bill: T.free };
    if (!c.monthly) return { value: c.yearly, per: T.year, bill: T.yearlyOnly };
    return state.yearly ? { value: c.yearly, per: T.year, bill: T.billedYearly } : { value: c.monthly, per: T.month, bill: T.billedMonthly };
  }

  function render() {
    var tab = D.tabs.filter(function (t) { return t.id === state.tab; })[0];
    var hasMonthly = tab.cards.some(function (c) { return c.monthly; });
    var html = '<div class="pr-controls">' +
      '<div class="pr-tabs" role="tablist" aria-label="' + esc(T.tabs) + '">' + D.tabs.map(function (t) {
        var on = t.id === state.tab;
        return '<button type="button" role="tab" aria-selected="' + on + '" class="' + (on ? 'on' : '') + '" data-tab="' + t.id + '">' + esc(t.label) + '</button>';
      }).join('') + '</div>' +
      '<label class="pr-switch' + (hasMonthly ? '' : ' off') + '"><input type="checkbox" role="switch"' + (state.yearly ? ' checked' : '') + (hasMonthly ? '' : ' disabled') + '>' +
      '<span class="track"><span class="thumb"></span></span><span>' + esc(T.toggle) + ' <b>(' + esc(T.save) + ')</b></span></label></div>' +
      '<div class="pr-cards n' + tab.cards.length + '">' + tab.cards.map(function (c, i) {
        var p = priceOf(c);
        return '<article class="pr-card' + (c.popular ? ' popular' : '') + '" style="--i:' + i + '">' +
          (c.popular ? '<span class="pr-badge">' + STAR + esc(T.popular) + '</span>' : '') +
          '<h3>' + esc(c.name) + '</h3><p class="pr-tag">' + esc(c.tag) + '</p>' +
          '<p class="pr-price"><span class="num" data-value="' + p.value + '">' + fmt.format(p.value) + '</span></p>' +
          '<p class="pr-unit">VND' + (p.per ? ' / ' + esc(p.per) : '') + '</p>' +
          '<p class="pr-bill">' + esc(p.bill) + (c.free ? '' : ' · ' + esc(tab.unit)) + '</p>' +
          '<ul>' + c.features.map(function (f) { return '<li>' + CHECK + '<span>' + esc(f) + '</span></li>'; }).join('') + '</ul>' +
          '<a class="btn' + (c.popular ? ' primary' : '') + '" href="' + esc(c.button.href) + '"' +
          (c.button.demo ? ' target="_blank" rel="noopener" data-demo-window="' + esc(c.button.demo) + '"' : (/^https?:\/\/(?!myteachersdeck\.com)/.test(c.button.href) ? ' target="_blank" rel="noopener"' : '')) +
          '>' + esc(c.button.text) + '</a>' +
          (c.desc ? '<p class="pr-desc">' + esc(c.desc) + '</p>' : '') +
          (c.links && c.links.length ? '<p class="pr-links">' + c.links.map(function (l) { return '<a href="' + esc(l.href) + '">' + esc(l.text) + ' →</a>'; }).join('') + '</p>' : '') +
          '</article>';
      }).join('') + '</div>' +
      (tab.notes.length ? '<ul class="pr-notes">' + tab.notes.map(function (n) {
        return '<li>' + esc(n.text) + (n.links.length ? ' ' + n.links.map(function (l) { return '<a href="' + esc(l.href) + '">' + esc(l.text) + ' →</a>'; }).join(' ') : '') + '</li>';
      }).join('') + '</ul>' : '');
    root.innerHTML = html;
    root.querySelectorAll('[data-tab]').forEach(function (b) {
      b.addEventListener('click', function () { state.tab = b.getAttribute('data-tab'); try { sessionStorage.setItem('td_pricing_tab', state.tab); } catch (e) {} history.replaceState(null, '', '#' + state.tab); render(); root.querySelector('[data-tab="' + state.tab + '"]').focus(); });
      b.addEventListener('keydown', function (e) {
        var ids = D.tabs.map(function (t) { return t.id; }), k = ids.indexOf(state.tab);
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); state.tab = ids[(k + (e.key === 'ArrowRight' ? 1 : ids.length - 1)) % ids.length]; render(); root.querySelector('[data-tab="' + state.tab + '"]').focus(); }
      });
    });
    var sw = root.querySelector('.pr-switch input');
    sw.addEventListener('change', function () {
      var before = values(); state.yearly = sw.checked; render(); tween(before); root.querySelector('.pr-switch input').focus();
      if (state.yearly) confetti(root.querySelector('.pr-switch .track'));
    });
    requestAnimationFrame(function () { root.classList.add('shown'); });
  }

  function values() { return Array.prototype.map.call(root.querySelectorAll('.pr-price .num'), function (n) { return +n.getAttribute('data-value'); }); }
  function tween(from) {
    if (reduce) return;
    var nums = root.querySelectorAll('.pr-price .num'), t0 = performance.now();
    (function step(now) {
      var k = Math.min(1, (now - t0) / 500), e = 1 - Math.pow(1 - k, 3);
      nums.forEach(function (n, i) { var to = +n.getAttribute('data-value'), a = from[i] == null ? to : from[i]; n.textContent = fmt.format(Math.round(a + (to - a) * e)); });
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }
  function confetti(el) {
    if (reduce || !el) return;
    var go = function () {
      var r = el.getBoundingClientRect();
      window.confetti({ particleCount: 50, spread: 60, ticks: 200, gravity: 1.2, decay: 0.94, startVelocity: 30, shapes: ['circle'],
        origin: { x: (r.left + r.width / 2) / innerWidth, y: (r.top + r.height / 2) / innerHeight },
        colors: ['#4A55B8', '#E8A33D', '#9DB87A', '#EE5A3C'] });
    };
    if (window.confetti) return go();
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js';
    s.onload = go; document.head.appendChild(s);
  }
  render();
})();
