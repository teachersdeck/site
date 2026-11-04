/* A day at kindergarten (home page, Preschool section). The page shows one of three versions per visit, picked by the
   inline script after the block (.kdp[data-v]; ?kday=a|b|c picks one):
     a  the sun crosses the day: a clock runs 07:00 to 17:00 above the cards, and each card lifts as its hour comes
     b  the app at each moment: the moments step through, and a phone shows the app right then
     c  cards that come alive: the cards rise in turn and each plays its own small scene
   A tap (or Enter) on a moment jumps to it in a and b; the button pauses all three. It only moves while the section is
   on screen and the tab is visible, and never by itself for visitors who ask for reduced motion.
   All the words are in the page (English and Vietnamese); this only plays them. Styles: .kdp in site.css. */
(function () {
  var box = document.querySelector('.kdp');
  if (!box) return;
  var v = box.getAttribute('data-v') || 'b';
  var lis = [].slice.call(box.querySelectorAll('.kd-day li'));
  var btn = box.querySelector('.kdp-pause');
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var paused = false, visible = false, started = false;

  box.classList.add('live');
  if (still) box.classList.add('still');
  lis.forEach(function (li, i) { li.style.setProperty('--i', i); if (v !== 'c') li.setAttribute('tabindex', '0'); });
  if (!still) btn.hidden = false;

  function mark(i, done) {
    lis.forEach(function (li, j) {
      var on = j === i;
      if (on && !li.classList.contains('on')) { li.classList.remove('on'); void li.offsetWidth; }
      li.classList.toggle('on', on);
      li.classList.toggle('done', !!done && j < i);
      if (on) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current');
    });
  }

  /* ---------- a: the sun crosses the day ---------- */
  function makeA() {
    var DAY_MS = 11000, REST_MS = 2200;
    var sun = box.querySelector('.kda-sun'), fill = box.querySelector('.kda-fill'),
        clock = box.querySelector('.kda-clock'), night = box.querySelector('.kda-night');
    var hours = lis.map(function (li) { var t = (li.querySelector('time') || {}).textContent || '0:0', m = t.split(':'); return +m[0] + (+m[1] || 0) / 60; });
    var from = 7, to = 17, p = 0, raf = 0, last = 0, rest = 0, cur = -2;
    function draw() {
      var hour = from + p * (to - from), hh = Math.floor(hour), mm = Math.floor((hour - hh) * 12) * 5;
      sun.style.left = (4 + p * 92) + '%';
      sun.style.bottom = (8 + Math.sin(p * Math.PI) * 26) + 'px';
      fill.style.width = (p * 100) + '%';
      night.style.opacity = Math.max(0, (p - 0.7) / 0.3);
      clock.textContent = (hh < 10 ? '0' : '') + hh + ':' + (mm < 10 ? '0' : '') + mm;
      var c = -1; hours.forEach(function (h, k) { if (hour >= h - 1e-6) c = k; });
      if (c !== cur) { cur = c; mark(c, true); }
    }
    function frame(now) {
      var dt = last ? now - last : 0; last = now;
      if (rest > 0) { rest -= dt; if (rest <= 0) { p = 0; cur = -2; } }
      else { p = Math.min(1, p + dt / DAY_MS); if (p >= 1) rest = REST_MS; }
      draw();
      raf = requestAnimationFrame(frame);
    }
    return {
      run: function () { if (!raf) { last = 0; raf = requestAnimationFrame(frame); } },
      stop: function () { cancelAnimationFrame(raf); raf = 0; },
      jump: function (i) { p = Math.max(0, Math.min(1, (hours[i] - from) / (to - from))); rest = 0; draw(); },
      first: function () { draw(); }
    };
  }

  /* ---------- b: the app at each moment ---------- */
  function makeB() {
    var STEP_MS = 3600;
    var scenes = [].slice.call(box.querySelectorAll('.kdp-scene'));
    var appEl = box.querySelector('.kdp-bar b'), timeEl = box.querySelector('.kdp-bar em');
    var locale = box.getAttribute('data-locale') || 'en-US';
    var k = 0, timer = 0, ticks = [], going = false;
    box.style.setProperty('--kdp-t', STEP_MS + 'ms');
    function stopTicks() { ticks.forEach(clearInterval); ticks = []; }
    function every(ms, fn) { ticks.push(setInterval(fn, ms)); }
    // the numbers on each screen count up (or down) while it shows; reduced motion shows them as written in the page
    function count(sc) {
      if (still) return;
      var c = sc.querySelector('[data-count]');
      if (c) { var n = 0, cto = +c.getAttribute('data-count'); c.textContent = '0'; every(380, function () { if (n < cto) c.textContent = ++n; }); }
      var t = sc.querySelector('[data-timer]');
      if (t) { var left = +t.getAttribute('data-timer'); every(100, function () { left = Math.max(0, left - 6); t.textContent = Math.floor(left / 60) + ':' + ('0' + left % 60).slice(-2); }); }
      var picks = sc.querySelectorAll('.kdp-pick span');
      if (picks.length) {
        var spin = 0, end = [].indexOf.call(picks, sc.querySelector('.kdp-pick .kdp-hit'));
        every(140, function () {
          [].forEach.call(picks, function (q) { q.classList.remove('kdp-hit'); });
          picks[spin < 14 ? spin % picks.length : end].classList.add('kdp-hit'); spin++;
        });
      }
      var m = sc.querySelector('[data-money]');
      if (m) { var sum = 0, goal = +m.getAttribute('data-money'); m.textContent = '0'; every(60, function () { sum = Math.min(goal, sum + goal / 30); m.textContent = Math.round(sum).toLocaleString(locale); }); }
    }
    function show(i) {
      clearTimeout(timer); stopTicks(); k = i;
      mark(i, false);
      scenes.forEach(function (sc) { sc.classList.remove('on'); });
      var sc = scenes[i]; void sc.offsetWidth; sc.classList.add('on');
      appEl.textContent = sc.getAttribute('data-app');
      var tm = lis[i].querySelector('time'); timeEl.textContent = tm ? tm.textContent : '';
      count(sc);
      if (going) timer = setTimeout(function () { show((k + 1) % lis.length); }, STEP_MS);
    }
    return {
      run: function () { if (!going) { going = true; clearTimeout(timer); timer = setTimeout(function () { show((k + 1) % lis.length); }, STEP_MS); } },
      stop: function () { going = false; clearTimeout(timer); },
      jump: function (i) { show(i); },
      first: function () { show(0); }
    };
  }

  /* ---------- c: cards that come alive ---------- */
  function makeC() {
    return {
      run: function () { box.classList.remove('paused'); },
      stop: function () { box.classList.add('paused'); },
      jump: function () {},
      first: function () { box.classList.add('play'); }
    };
  }

  var mode = v === 'a' ? makeA() : v === 'c' ? makeC() : makeB();

  function go() {
    if (!started) { started = true; mode.first(); }
    if (!still && !paused && visible && !document.hidden) mode.run();
    else mode.stop();
  }

  box.querySelector('.kd-day').addEventListener('click', function (e) {
    var li = e.target.closest && e.target.closest('li[data-k]');
    if (li && v !== 'c') { started = true; mode.jump(+li.getAttribute('data-k')); go(); }
  });
  box.querySelector('.kd-day').addEventListener('keydown', function (e) {
    var li = e.target.closest && e.target.closest('li[data-k]');
    if (li && v !== 'c' && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); started = true; mode.jump(+li.getAttribute('data-k')); go(); }
  });
  btn.addEventListener('click', function () {
    paused = !paused;
    box.classList.toggle('paused', paused);
    btn.textContent = box.getAttribute(paused ? 'data-play' : 'data-pause');
    if (paused) mode.stop(); else go();
  });
  document.addEventListener('visibilitychange', go);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible || started) go(); }, { threshold: 0.3 }).observe(box);
  } else { visible = true; go(); }
  if (still) go();
})();
