/* Pricing page: "Build your price". Prices mirror _build/pricing.py (Pricing Sheet v3):
   TeachersDeck Pro 240,000 VND a month or 2,100,000 a year (Founding Teacher 1,300,000 a year); ClassIn/Canvas 1,250,000 a year;
   ParentDeck Pro 30,000 a month or 300,000 a year per child, 2nd child 30% off, 3rd and more 50% off, Founding Family 30% off year one;
   campus plans by teachers and students, extra teacher 90,000 a month; volume discounts 10/15/20% from 4/10/25 campuses, +5% for two
   years; pilot founding rate 30% off the monthly price for 12 months (up to 3 campuses); seats for international schools and
   universities: 100,000 per student, 500,000 per linked parent. */
(function () {
  var box = document.querySelector('.calc.bp'); if (!box) return;
  box.hidden = false;
  var vi = box.getAttribute('data-lang') === 'vi', L = JSON.parse(box.getAttribute('data-l'));
  var SUITE = [['Suite Starter', 8, 150, 1500000, 15000000], ['Suite Standard', 20, 400, 3000000, 30000000], ['Suite Growth', 40, 900, 5200000, 52000000]];
  var TD = [['TeachersDeck Starter', 8, 1e9, 800000, 8000000], ['TeachersDeck Standard', 20, 1e9, 1800000, 18000000], ['TeachersDeck Growth', 40, 1e9, 3200000, 32000000]];
  var st = {}, q = function (s) { return box.querySelector(s); }, o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
  var num = function (n) { return Math.round(n).toLocaleString(vi ? 'vi-VN' : 'en-US'); }, vnd = function (n) { return num(n) + ' VND'; };

  [].slice.call(box.querySelectorAll('.bp-chips')).forEach(function (g) {
    var k = g.getAttribute('data-k'), bs = [].slice.call(g.querySelectorAll('[role=radio]'));
    bs.forEach(function (b, i) {
      if (b.getAttribute('aria-checked') === 'true') st[k] = b.getAttribute('data-v');
      b.tabIndex = b.getAttribute('aria-checked') === 'true' ? 0 : -1;
      b.addEventListener('click', function () { bs.forEach(function (x) { x.setAttribute('aria-checked', x === b ? 'true' : 'false'); x.tabIndex = x === b ? 0 : -1; }); st[k] = b.getAttribute('data-v'); draw(); });
      b.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = bs[(i + 1) % bs.length];
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = bs[(i + bs.length - 1) % bs.length];
        if (n) { e.preventDefault(); n.click(); n.focus(); }
      });
    });
  });
  [].slice.call(box.querySelectorAll('input')).forEach(function (i) { i.addEventListener('input', draw); i.addEventListener('change', draw); });

  function draw() {
    var who = st.who, show = who === 'teacher' ? 'teacher teacher-' + st.product : who;
    [].slice.call(box.querySelectorAll('.bp-f[data-show]')).forEach(function (f) {
      var on = f.getAttribute('data-show').split(' ').some(function (x) { return show.split(' ').indexOf(x) >= 0; });
      f.hidden = !on;
    });
    ['bp-k', 'bp-c', 'bp-t', 'bp-s', 'bp-p'].forEach(function (id) { o(id).textContent = num(+q('#' + id).value); });
    var camp = q('.bp-camp'); camp.textContent = camp.getAttribute(who === 'uni' ? 'data-b' : 'data-a');
    var rows = [], total = 0, note = '', cta = L.cta_q, href = 'https://myteachersdeck.com/quote/';
    var add = function (a, v, cls) { rows.push([a, v, cls]); total += v; };

    if (who === 'teacher') {
      cta = L.cta_o; href = 'https://myteachersdeck.com/order/';
      if (st.product === 'platform') add(L.plat, 1250000);
      else if (q('#bp-ft').checked) add(L.proF, 1300000);
      else if (st.bill === 'month') add(L.pro + ' · ' + L.monthly.replace('{v}', vnd(240000)), 240000 * 12);
      else add(L.pro, 2100000);
    } else if (who === 'family') {
      cta = L.cta_o; href = 'https://myteachersdeck.com/order/';
      var k = +q('#bp-k').value, base = st.bill === 'month' ? 30000 * 12 : 300000;
      for (var i = 1; i <= k; i++) {
        var d = i === 1 ? 0 : i === 2 ? 30 : 50;
        add(L.child.replace('{n}', i) + (d ? ' · ' + L.sib.replace('{d}', d) : '') + (st.bill === 'month' ? ' · ' + L.monthly.replace('{v}', vnd(30000 * (1 - d / 100))) : ''), base * (1 - d / 100));
      }
      if (q('#bp-ff').checked) add(L.foundF, -total * 0.3, 'sub');
    } else {
      var c = +q('#bp-c').value, t = +q('#bp-t').value, s = +q('#bp-s').value, tiers = st.apps === 'td' ? TD : SUITE, best = null;
      tiers.forEach(function (x) {
        if (s > x[2]) return;
        var extra = Math.max(0, t - x[1]), cost = x[4] + extra * 1080000;
        if (!best || cost < best.cost) best = { x: x, extra: extra, cost: cost };
      });
      if (!best || t > 60) { rows.push([L.custom, null, 'tot']); render(rows, null, '', L.cta_q, href); return; }
      var pilot = q('#bp-fc').checked && c <= 3;
      var planCost = pilot ? best.x[3] * 12 * 0.7 : best.x[4];
      add(L.plan.replace('{n}', c).replace('{plan}', best.x[0]), c * best.x[4]);
      if (pilot) add(L.foundC, -c * (best.x[4] - planCost), 'sub');
      if (best.extra) add(L.extraT.replace('{n}', c * best.extra), c * best.extra * 1080000);
      var d = c >= 25 ? 20 : c >= 10 ? 15 : c >= 4 ? 10 : 0; if (q('#bp-two').checked) d += 5;
      var plansTotal = total;
      if (d) add(L.disc.replace('{d}', d), -plansTotal * d / 100, 'sub');
      if (who === 'intl' || who === 'uni') {
        var ns = c * s, np = +q('#bp-p').value;
        add(L.seatS.replace('{n}', num(ns)), ns * 100000); add(L.seatP.replace('{n}', num(np)), np * 500000);
      } else note = L.noseat;
    }
    render(rows, total, note, cta, href);
  }
  function render(rows, total, note, cta, href) {
    var dl = o('rows'); dl.textContent = '';
    rows.forEach(function (r) {
      var w = document.createElement('div'); if (r[2]) w.className = r[2];
      var dt = document.createElement('dt'); dt.textContent = r[0]; w.appendChild(dt);
      if (r[1] !== null) { var dd = document.createElement('dd'); dd.textContent = (r[1] < 0 ? '− ' : '') + vnd(Math.abs(r[1])); w.appendChild(dd); }
      dl.appendChild(w);
    });
    if (total !== null) {
      var w = document.createElement('div'); w.className = 'tot';
      var dt = document.createElement('dt'); dt.textContent = L.total; var dd = document.createElement('dd'); dd.textContent = vnd(total);
      w.appendChild(dt); w.appendChild(dd); dl.appendChild(w);
      o('per').textContent = L.permonth.replace('{v}', vnd(total / 12)).replace('{u}', '$' + Math.round(total / 26300).toLocaleString('en-US'));
    } else o('per').textContent = '';
    o('note').textContent = note || '';
    var a = o('cta'); a.textContent = cta; a.href = href;
  }
  draw();
})();
