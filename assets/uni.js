/* Universities page: the UniDeck live tour (one preview, four app tabs) and the multi-faculty cost calculator.
   Prices mirror _build/universities.py: faculty plans, 10% / 15% / 20% off from 4 / 10 / 25 faculties, extra 5% for two
   years, seats 100,000 VND per student and 500,000 VND per linked parent a year. */
(function () {
  /* ---- tour ---- */
  var tour = document.querySelector('.utour');
  if (tour) {
    var box = tour.querySelector('.live'), tabs = [].slice.call(tour.querySelectorAll('[role=tab]'));
    var base = 'https://teachersdeck.github.io/demo/unideck/';
    var show = function (b, focus) {
      tabs.forEach(function (x) { var on = x === b; x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1; });
      if (focus) b.focus();
      var app = b.getAttribute('data-app'), name = b.getAttribute('data-name'), src = base + app + '/?demo=1';
      box.setAttribute('data-src', src); box.setAttribute('data-title', name); box.setAttribute('data-live', 'unideck-' + app);
      tour.querySelector('.ut-name').textContent = name;
      [].slice.call(box.querySelectorAll('a')).forEach(function (a) { a.href = src; a.setAttribute('data-demo-window', 'unideck-' + app); });
      var f = box.querySelector('iframe');
      if (f) { box.classList.remove('ready'); f.addEventListener('load', function () { box.classList.add('ready'); }, { once: true }); f.title = name; f.src = src; }
      else { var p = box.querySelector('.live-play'); if (p) p.click(); }
    };
    tabs.forEach(function (b, i) {
      b.addEventListener('click', function () { show(b); });
      b.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = tabs[(i + tabs.length - 1) % tabs.length];
        if (n) { e.preventDefault(); show(n, true); }
      });
    });
  }

  /* ---- calculator ---- */
  var c = document.querySelector('.ucalc'); if (!c) return;
  c.hidden = false;
  var vi = c.getAttribute('data-lang') === 'vi', L = JSON.parse(c.getAttribute('data-l'));
  var q = function (s) { return c.querySelector(s); }, o = function (k) { return c.querySelector('[data-o="' + k + '"]'); };
  var fmt = function (n) { return Math.round(n).toLocaleString(vi ? 'vi-VN' : 'en-US') + ' VND'; };
  var plans = [].slice.call(c.querySelectorAll('.u-plans [role=radio]')), plan = plans.filter(function (b) { return b.getAttribute('aria-checked') === 'true'; })[0];
  plans.forEach(function (b, i) {
    b.tabIndex = b === plan ? 0 : -1;
    var pick = function () { plan = b; plans.forEach(function (x) { x.setAttribute('aria-checked', x === b ? 'true' : 'false'); x.tabIndex = x === b ? 0 : -1; }); draw(); };
    b.addEventListener('click', pick);
    b.addEventListener('keydown', function (e) {
      var n = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = plans[(i + 1) % plans.length];
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = plans[(i + plans.length - 1) % plans.length];
      if (n) { e.preventDefault(); n.click(); n.focus(); }
    });
  });
  function draw() {
    var f = +q('#u-f').value, s = +q('#u-s').value, p = +q('#u-p').value, two = q('#u-two').checked;
    o('f').textContent = f; o('s').textContent = s.toLocaleString(vi ? 'vi-VN' : 'en-US'); o('p').textContent = p.toLocaleString(vi ? 'vi-VN' : 'en-US');
    var d = f >= 25 ? 20 : f >= 10 ? 15 : f >= 4 ? 10 : 0; if (two) d += 5;
    var list = f * +plan.getAttribute('data-price'), plansCost = list * (1 - d / 100), ss = s * 100000, ps = p * 500000, total = plansCost + ss + ps;
    var dl = o('rows'); dl.textContent = '';
    var row = function (a, b, cls) { var w = document.createElement('div'); if (cls) w.className = cls; var dt = document.createElement('dt'); dt.textContent = a; var dd = document.createElement('dd'); dd.textContent = b; w.appendChild(dt); w.appendChild(dd); dl.appendChild(w); };
    row(L.plans.replace('{n}', f) + ' · ' + plan.getAttribute('data-name'), fmt(list));
    if (d) row(L.disc.replace('{d}', d), '− ' + fmt(list - plansCost), 'sub');
    row(L.seat_s + ' (' + s.toLocaleString(vi ? 'vi-VN' : 'en-US') + ' × 100,000)'.replace('100,000', vi ? '100.000' : '100,000'), fmt(ss));
    row(L.seat_p + ' (' + p.toLocaleString(vi ? 'vi-VN' : 'en-US') + ' × ' + (vi ? '500.000' : '500,000') + ')', fmt(ps));
    row(L.total, fmt(total), 'tot');
    o('per').textContent = (f >= 25 ? L.big + ' ' : '') + L.per.replace('{v}', fmt(total / s)).replace('{u}', '$' + Math.round(total / 26300).toLocaleString('en-US'));
  }
  ['#u-f', '#u-s', '#u-p', '#u-two'].forEach(function (s) { q(s).addEventListener('input', draw); q(s).addEventListener('change', draw); });
  draw();
})();
