/* Home page "Try it right here": a working timer, name picker and noise meter (EN/VI). No dependencies.
   The playground is hidden in the markup and only shown once this script runs. */
(function () {
  var root = document.getElementById('playground');
  if (!root) return;
  var vi = (document.documentElement.lang || '').indexOf('vi') === 0;
  var L = vi
    ? { start: 'Bắt đầu', pause: 'Tạm dừng', again: 'Chạy lại', quiet: 'Lớp đang yên lặng', loud: 'Hơi ồn rồi', tooLoud: 'Ồn quá, nói nhỏ lại', mic: 'Dùng micrô của tôi', micOff: 'Tắt micrô', micNo: 'Không mở được micrô. Hãy kéo thanh trượt để thử.' }
    : { start: 'Start', pause: 'Pause', again: 'Again', quiet: 'Nice and quiet', loud: 'Getting loud', tooLoud: 'Too loud, voices down', mic: 'Use my microphone', micOff: 'Stop microphone', micNo: 'The microphone could not be opened. Drag the slider to try it.' };
  var $ = function (s) { return root.querySelector(s); };
  root.hidden = false;

  /* Tabs */
  var tabs = [].slice.call(root.querySelectorAll('[role=tab]'));
  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    $('.pg-title').textContent = '· ' + tab.querySelector('b').textContent;
    if (focus) tab.focus();
    if (tab.dataset.tab !== 'noise') stopMic();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      var k = e.key, n = null;
      if (k === 'ArrowDown' || k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
      if (k === 'ArrowUp' || k === 'ArrowLeft') n = tabs[(i + tabs.length - 1) % tabs.length];
      if (k === 'Home') n = tabs[0];
      if (k === 'End') n = tabs[tabs.length - 1];
      if (n) { e.preventDefault(); select(n, true); }
    });
  });

  /* Timer */
  var total = 300, left = 300, iv = null;
  var timeEl = $('.pg-time'), progEl = $('.pg-prog i'), mainBtn = $('[data-act=toggle]');
  function drawTimer() {
    var m = Math.floor(left / 60), s = left % 60;
    timeEl.textContent = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    timeEl.classList.toggle('done', left === 0);
    progEl.style.width = (100 * left / total) + '%';
    mainBtn.textContent = iv ? L.pause : (left === 0 ? L.again : L.start);
  }
  function stopTimer() { clearInterval(iv); iv = null; }
  $('[data-act=toggle]').addEventListener('click', function () {
    if (iv) { stopTimer(); drawTimer(); return; }
    if (left === 0) left = total;
    iv = setInterval(function () {
      left = Math.max(0, left - 1);
      if (left === 0) stopTimer();
      drawTimer();
    }, 1000);
    drawTimer();
  });
  $('[data-act=add]').addEventListener('click', function () { total += 60; left += 60; drawTimer(); });
  $('[data-act=reset]').addEventListener('click', function () { stopTimer(); total = left = 300; drawTimer(); });
  drawTimer();

  /* Name picker: every name once before anyone is picked twice */
  var chips = [].slice.call(root.querySelectorAll('.pg-names span'));
  var names = chips.map(function (c) { return c.textContent; });
  var used = [], roll = null, nameEl = $('.pg-name');
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function drawNames(current) {
    chips.forEach(function (c) {
      c.classList.toggle('used', used.indexOf(c.textContent) >= 0 && c.textContent !== current);
      c.classList.toggle('on', c.textContent === current);
    });
  }
  $('[data-act=pick]').addEventListener('click', function () {
    clearTimeout(roll);
    if (used.length >= names.length) used = [];
    var pool = names.filter(function (n) { return used.indexOf(n) < 0; });
    var pick = pool[Math.floor(Math.random() * pool.length)];
    var step = still ? 12 : 0;
    nameEl.setAttribute('aria-busy', 'true');
    (function tick() {
      step++;
      if (step < 12) {
        nameEl.textContent = names[Math.floor(Math.random() * names.length)];
        nameEl.classList.add('rolling');
        roll = setTimeout(tick, 40 + step * 18);
      } else {
        used.push(pick);
        nameEl.textContent = pick;
        nameEl.classList.remove('rolling');
        nameEl.removeAttribute('aria-busy');
        drawNames(pick);
      }
    })();
  });
  $('[data-act=over]').addEventListener('click', function () {
    clearTimeout(roll); used = []; nameEl.textContent = '?'; nameEl.classList.remove('rolling'); drawNames(null);
  });

  /* Noise meter: the slider, or the visitor's microphone if they choose it (measured locally, never recorded) */
  var range = $('#pg-level'), zoneEl = $('.pg-zone'), bars = [].slice.call(root.querySelectorAll('.pg-bars i'));
  var micBtn = $('[data-act=mic]'), stream = null, ctx = null, raf = null;
  function drawNoise(lv) {
    var z = lv < 45 ? 'quiet' : lv < 75 ? 'loud' : 'tooLoud';
    zoneEl.textContent = L[z];
    root.setAttribute('data-zone', z);
    bars.forEach(function (b, i) {
      var wave = 0.55 + 0.45 * Math.abs(Math.sin(i * 1.7 + 0.6));
      b.style.height = Math.max(4, Math.round(lv * wave)) + '%';
    });
  }
  range.addEventListener('input', function () { drawNoise(+range.value); });
  function stopMic() {
    if (!stream) return;
    cancelAnimationFrame(raf);
    stream.getTracks().forEach(function (t) { t.stop(); });
    if (ctx) ctx.close();
    stream = ctx = null;
    range.disabled = false;
    micBtn.textContent = L.mic;
    micBtn.setAttribute('aria-pressed', 'false');
    drawNoise(+range.value);
  }
  micBtn.addEventListener('click', function () {
    if (stream) { stopMic(); return; }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) { zoneEl.textContent = L.micNo; return; }
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (s) {
      stream = s;
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      var an = ctx.createAnalyser();
      an.fftSize = 1024;
      ctx.createMediaStreamSource(s).connect(an);
      var buf = new Float32Array(an.fftSize), smooth = 0;
      range.disabled = true;
      micBtn.textContent = L.micOff;
      micBtn.setAttribute('aria-pressed', 'true');
      (function loop() {
        an.getFloatTimeDomainData(buf);
        var sum = 0;
        for (var i = 0; i < buf.length; i++) sum += buf[i] * buf[i];
        var db = 20 * Math.log10(Math.sqrt(sum / buf.length) || 1e-8);
        var lv = Math.max(0, Math.min(100, (db + 60) * 2));
        smooth = smooth * 0.8 + lv * 0.2;
        range.value = Math.round(smooth);
        drawNoise(smooth);
        raf = requestAnimationFrame(loop);
      })();
    }).catch(function () { zoneEl.textContent = L.micNo; });
  });
  drawNoise(+range.value);
  window.addEventListener('pagehide', stopMic);
})();
