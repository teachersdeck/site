/* A day at kindergarten (home page, Preschool section): the six moments step through on their own and the phone beside
   them shows the app at that moment. A tap (or Enter) on a moment jumps to it; the button pauses. It only moves while the
   section is on screen and the tab is visible, and it never moves by itself for visitors who ask for reduced motion.
   All the words are in the page (English and Vietnamese); this only plays them. Styles: .kdp in site.css. */
(function () {
  var box = document.querySelector('.kdp');
  if (!box) return;
  var STEP_MS = 3600;
  var lis = [].slice.call(box.querySelectorAll('.kd-day li'));
  var scenes = [].slice.call(box.querySelectorAll('.kdp-scene'));
  var appEl = box.querySelector('.kdp-bar b'), timeEl = box.querySelector('.kdp-bar em'), btn = box.querySelector('.kdp-pause');
  var locale = box.getAttribute('data-locale') || 'en-US';
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var k = 0, timer = 0, ticks = [], paused = false, visible = false, first = true;

  box.classList.add('live');
  if (still) box.classList.add('still');
  box.style.setProperty('--kdp-t', STEP_MS + 'ms');
  lis.forEach(function (li) { li.setAttribute('tabindex', '0'); });
  if (!still) btn.hidden = false;

  function stopTicks() { ticks.forEach(clearInterval); ticks = []; }
  function every(ms, fn) { ticks.push(setInterval(fn, ms)); }

  // the numbers on each screen count up (or down) while it shows; reduced motion shows them as written in the page
  function run(sc) {
    if (still) return;
    var c = sc.querySelector('[data-count]');
    if (c) { var n = 0, to = +c.getAttribute('data-count'); c.textContent = '0'; every(380, function () { if (n < to) c.textContent = ++n; }); }
    var t = sc.querySelector('[data-timer]');
    if (t) { var left = +t.getAttribute('data-timer'); every(100, function () { left = Math.max(0, left - 6); t.textContent = Math.floor(left / 60) + ':' + ('0' + left % 60).slice(-2); }); }
    var picks = sc.querySelectorAll('.kdp-pick span');
    if (picks.length) {
      var spin = 0, last = [].indexOf.call(picks, sc.querySelector('.kdp-pick .kdp-hit'));
      every(140, function () {
        [].forEach.call(picks, function (p) { p.classList.remove('kdp-hit'); });
        picks[spin < 14 ? spin % picks.length : last].classList.add('kdp-hit');
        spin++;
      });
    }
    var m = sc.querySelector('[data-money]');
    if (m) { var sum = 0, goal = +m.getAttribute('data-money'); m.textContent = '0'; every(60, function () { sum = Math.min(goal, sum + goal / 30); m.textContent = Math.round(sum).toLocaleString(locale); }); }
  }

  function show(i) {
    clearTimeout(timer); stopTicks(); k = i; first = false;
    lis.forEach(function (li, j) {
      li.classList.remove('on'); li.removeAttribute('aria-current');
      if (j === i) { void li.offsetWidth; li.classList.add('on'); li.setAttribute('aria-current', 'step'); }
    });
    scenes.forEach(function (sc) { sc.classList.remove('on'); });
    var sc = scenes[i]; void sc.offsetWidth; sc.classList.add('on');
    appEl.textContent = sc.getAttribute('data-app');
    var tm = lis[i].querySelector('time'); timeEl.textContent = tm ? tm.textContent : '';
    run(sc);
    schedule();
  }
  function schedule() {
    clearTimeout(timer);
    if (!still && !paused && visible && !document.hidden) timer = setTimeout(function () { show((k + 1) % lis.length); }, STEP_MS);
  }

  box.querySelector('.kd-day').addEventListener('click', function (e) {
    var li = e.target.closest && e.target.closest('li[data-k]'); if (li) show(+li.getAttribute('data-k'));
  });
  box.querySelector('.kd-day').addEventListener('keydown', function (e) {
    var li = e.target.closest && e.target.closest('li[data-k]');
    if (li && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); show(+li.getAttribute('data-k')); }
  });
  btn.addEventListener('click', function () {
    paused = !paused;
    box.classList.toggle('paused', paused);
    btn.textContent = box.getAttribute(paused ? 'data-play' : 'data-pause');
    if (paused) clearTimeout(timer); else show((k + 1) % lis.length);
  });
  document.addEventListener('visibilitychange', schedule);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible && first) { first = false; show(0); } else schedule();
    }, { threshold: 0.3 }).observe(box);
  } else { visible = true; show(0); }
  if (still && first) show(0);
})();
