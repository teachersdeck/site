/* International schools page: seat-fee calculator. Prices mirror _build/content.py (Pricing Sheet v2):
   campus plans by student count, extra teachers 90,000 VND a month, seats 100,000 VND per student and 500,000 VND
   per parent a year; founding rate = 30% off the monthly campus price for 12 months. */
(function () {
  var box = document.querySelector('.calc'); if (!box) return;
  box.hidden = false;
  var vi = box.getAttribute('data-lang') === 'vi', L = JSON.parse(box.getAttribute('data-l'));
  var TIERS = [['Suite Starter', 8, 150, 1500000, 15000000], ['Suite Standard', 20, 400, 3000000, 30000000], ['Suite Growth', 40, 900, 5200000, 52000000]];
  var EXTRA_T = 90000 * 12, SEAT_S = 100000, SEAT_P = 500000, USD = 26300;
  var f = function (n) { return Math.round(n).toLocaleString(vi ? 'vi-VN' : 'en-US') + ' VND'; };
  var q = function (s) { return box.querySelector(s); }, o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
  function draw() {
    var t = +q('#c-t').value, s = +q('#c-s').value, p = +q('#c-p').value, found = q('#c-f').checked;
    o('t').textContent = t; o('s').textContent = s; o('p').textContent = p;
    var best = null;
    TIERS.forEach(function (x) {
      if (s > x[2]) return;
      var extra = Math.max(0, t - x[1]), plan = (found ? x[3] * 12 * 0.7 : x[4]) + extra * EXTRA_T;
      if (!best || plan < best.plan) best = { name: x[0], extra: extra, plan: plan };
    });
    var dl = o('rows'); dl.textContent = '';
    function row(a, b, cls) { var d = document.createElement('div'); if (cls) d.className = cls; var dt = document.createElement('dt'); dt.textContent = a; var dd = document.createElement('dd'); dd.textContent = b; d.appendChild(dt); d.appendChild(dd); dl.appendChild(d); }
    if (!best) { row(L.plan, L.big); o('usd').textContent = ''; return; }
    var ss = s * SEAT_S, ps = p * SEAT_P, total = best.plan + ss + ps;
    row(L.plan, best.name + (best.extra ? ' + ' + best.extra + ' ' + L.extra : ''), '');
    row('', f(best.plan), 'sub');
    row(L.seat_s + ' (' + s + ' × ' + f(SEAT_S) + ')', f(ss), '');
    row(L.seat_p + ' (' + p + ' × ' + f(SEAT_P) + ')', f(ps), '');
    row(L.total, f(total), 'tot');
    o('usd').textContent = L.usd.replace('{}', '$' + Math.round(total / USD).toLocaleString('en-US'));
  }
  ['#c-t', '#c-s', '#c-p', '#c-f'].forEach(function (s) { q(s).addEventListener('input', draw); q(s).addEventListener('change', draw); });
  draw();
})();
