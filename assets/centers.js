/* Language centers page: the live demo tour (TeachersDeck / ParentDeck / AdminDeck tabs driving one preview) and the
   chain cost calculator. Discounts mirror _build/centers.py: 10% from 4 centers, 15% from 10, 20% or better from 25,
   extra 5% for a two-year agreement. */
(function () {
  var tour = document.querySelector('.utour[data-base]');
  if (tour) {
    var base = tour.getAttribute('data-base'), box = tour.querySelector('.live'), tabs = [].slice.call(tour.querySelectorAll('[role=tab]'));
    var show = function (b, focus) {
      tabs.forEach(function (x) { var on = x === b; x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1; });
      if (focus) b.focus();
      var app = b.getAttribute('data-app'), name = b.getAttribute('data-name'), src = base + app + '/?demo=1';
      box.setAttribute('data-src', src); box.setAttribute('data-title', name); box.setAttribute('data-live', app);
      tour.querySelector('.ut-name').textContent = name;
      [].slice.call(box.querySelectorAll('a')).forEach(function (a) { a.href = src; a.setAttribute('data-demo-window', app); });
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

  var c = document.querySelector('.ccalc'); if (!c) return;
  c.hidden = false;
  var vi = c.getAttribute('data-lang') === 'vi', L = JSON.parse(c.getAttribute('data-l'));
  var q = function (s) { return c.querySelector(s); }, o = function (k) { return c.querySelector('[data-o="' + k + '"]'); };
  var fmt = function (n) { return Math.round(n).toLocaleString(vi ? 'vi-VN' : 'en-US') + ' VND'; };
  function draw() {
    var n = +q('#cc-n').value, sel = q('#cc-p'), price = +sel.value, name = sel.options[sel.selectedIndex].text, two = q('#cc-two').checked;
    o('n').textContent = n;
    var d = n >= 25 ? 20 : n >= 10 ? 15 : n >= 4 ? 10 : 0; if (two) d += 5;
    var list = n * price, total = list * (1 - d / 100);
    var dl = o('rows'); dl.textContent = '';
    var row = function (a, b, cls) { var w = document.createElement('div'); if (cls) w.className = cls; var dt = document.createElement('dt'); dt.textContent = a; var dd = document.createElement('dd'); dd.textContent = b; w.appendChild(dt); w.appendChild(dd); dl.appendChild(w); };
    row(L.list.replace('{n}', n).replace('{plan}', name), fmt(list));
    if (d) row(L.disc.replace('{d}', d), '− ' + fmt(list - total), 'sub');
    row(L.total, fmt(total), 'tot');
    var per = L.per.replace('{v}', fmt(total / n / 12)).replace('{u}', '$' + Math.round(total / 26300).toLocaleString('en-US'));
    o('per').textContent = (n >= 25 ? L.big + ' ' : n < 4 ? L.none + ' ' : '') + per;
  }
  ['#cc-n', '#cc-p', '#cc-two'].forEach(function (s) { q(s).addEventListener('input', draw); q(s).addEventListener('change', draw); });
  draw();
})();
