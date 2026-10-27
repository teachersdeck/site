/* Home page extras: the before-and-after slider (#compare) and the plan finder (#plans). EN/VI, no dependencies.
   Plan finder prices mirror _build/pricing.py (TeachersDeck Pricing Sheet); change both together. */
(function () {
  var vi = (document.documentElement.lang || '').indexOf('vi') === 0;

  /* ---- Before and after: the stage is drawn at 1000 x 520 and scaled to fit; the range input moves the divide ---- */
  var ba = document.querySelector('#compare .ba');
  if (ba) {
    var stage = ba.querySelector('.ba-stage'), range = ba.querySelector('.ba-range');
    var fit = function () { stage.style.setProperty('--k', (ba.clientWidth / 1000).toFixed(4)); };
    range.addEventListener('input', function () { ba.style.setProperty('--pos', range.value + '%'); ba.classList.add('moved'); });
    window.addEventListener('resize', fit); fit();
  }

  /* ---- Plan finder ---- */
  var sec = document.getElementById('plans');
  if (!sec) return;
  sec.hidden = false;
  var L = vi ? {
    year: 'một năm', quote: 'Báo giá', reqQuote: 'Yêu cầu báo giá', orderPro: 'Đặt mua Pro', orderPlat: 'Đặt mua cho ClassIn hoặc Canvas',
    pro: 'TeachersDeck Pro', proWhy: 'Mọi tiện ích, Cloud Class cho học sinh và phụ huynh, và báo cáo tiến bộ.',
    founding: 'Giáo viên sáng lập: 100 giáo viên đầu tiên chỉ trả 1.300.000 VND mỗi năm.', free: 'Hoặc bắt đầu miễn phí với các tiện ích hằng ngày. Không cần tài khoản.',
    plat: 'TeachersDeck cho ClassIn hoặc Canvas', platWhy: 'TeachersDeck trên bảng ClassIn, hoặc mở từ mọi khóa học Canvas.', demo: 'Dùng thử bản demo miễn phí trước. Không cần tài khoản.',
    custom: 'Gói Suite theo yêu cầu', customWhy: 'Hơn 40 giáo viên hoặc 900 học sinh: chúng tôi gửi báo giá bằng văn bản.',
    suiteWhy: function (t, s) { return 'Tối đa ' + t + ' giáo viên và ' + s + ' học sinh, kèm TeachersDeck Pro cho mọi giáo viên cùng StudentDeck, ParentDeck và AdminDeck.'; },
    seats: function (x, n) { return 'Cộng phí chỗ hằng năm: 100.000 VND mỗi học sinh (' + x + ' cho ' + n + ' học sinh) và 500.000 VND mỗi phụ huynh liên kết.'; },
    noSeats: 'Không thu phí chỗ cho học sinh hay phụ huynh.',
    pilot: 'Dùng thử miễn phí 30 ngày. Tham gia qua chương trình thí điểm, gói của bạn được giảm 30% trong 12 tháng đầu.'
  } : {
    year: 'a year', quote: 'Quote', reqQuote: 'Request a quote', orderPro: 'Order Pro', orderPlat: 'Order for ClassIn or Canvas',
    pro: 'TeachersDeck Pro', proWhy: 'Every widget, Cloud Class for students and parents, and progress reports.',
    founding: 'Founding Teacher: the first 100 teachers pay 1,300,000 VND a year.', free: 'Or start free with the everyday widgets. No account needed.',
    plat: 'TeachersDeck for ClassIn or Canvas', platWhy: 'TeachersDeck on your ClassIn board, or launched from any Canvas course.', demo: 'Try the free live demo first. No account needed.',
    custom: 'A custom Suite plan', customWhy: 'More than 40 teachers or 900 students: we send a written quote.',
    suiteWhy: function (t, s) { return 'Up to ' + t + ' teachers and ' + s + ' students, with TeachersDeck Pro for every teacher plus StudentDeck, ParentDeck and AdminDeck.'; },
    seats: function (x, n) { return 'Plus yearly seats: 100,000 VND per student (' + x + ' for ' + n + ') and 500,000 VND per parent who links.'; },
    noSeats: 'No seat fees for students or parents.',
    pilot: 'Try it free for 30 days. Join through the pilot and your plan is 30% off for the first 12 months.'
  };
  var TIERS = [['Suite Starter', 8, 150, 15000000], ['Suite Standard', 20, 400, 30000000], ['Suite Growth', 40, 900, 52000000]];
  var QUOTE = 'https://myteachersdeck.com/quote/', ORDER = 'https://myteachersdeck.com/order/';
  var vnd = function (n) { return n.toLocaleString(vi ? 'vi-VN' : 'en-US') + ' VND'; };
  var st = { kind: 'center', where: 'chrome' };
  var $ = function (s) { return sec.querySelector(s); }, out = function (k) { return sec.querySelector('[data-out="' + k + '"]'); };
  var tIn = $('#pf-t'), sIn = $('#pf-s'), res = $('.pf-res');

  function radios(sel, attr, key) {
    var bs = [].slice.call(sec.querySelectorAll(sel + ' [role=radio]'));
    bs.forEach(function (b, i) {
      b.tabIndex = b.getAttribute('aria-checked') === 'true' ? 0 : -1;
      b.addEventListener('click', function () { choose(b); });
      b.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = bs[(i + 1) % bs.length];
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = bs[(i + bs.length - 1) % bs.length];
        if (n) { e.preventDefault(); choose(n); n.focus(); }
      });
    });
    function choose(b) {
      bs.forEach(function (x) { var on = x === b; x.setAttribute('aria-checked', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1; });
      st[key] = b.getAttribute(attr); draw();
    }
  }
  radios('.pf-kinds', 'data-kind', 'kind');
  radios('.pf-where', 'data-where', 'where');
  tIn.addEventListener('input', draw); sIn.addEventListener('input', draw);

  function draw() {
    var t = +tIn.value, s = +sIn.value, plan, why, price, unit = L.year, extras = [], cta = L.reqQuote, href = QUOTE, tone = 'matcha';
    out('t').textContent = t; out('s').textContent = s;
    $('.pf-size').hidden = st.kind === 'solo'; $('.pf-solo').hidden = st.kind !== 'solo';
    if (st.kind === 'solo') {
      if (st.where === 'chrome') { plan = L.pro; why = L.proWhy; price = vnd(2100000); cta = L.orderPro; href = ORDER; tone = 'amber'; extras = [L.founding, L.free]; }
      else { plan = L.plat; why = L.platWhy; price = vnd(1250000); cta = L.orderPlat; href = ORDER; tone = 'coral'; extras = [L.demo]; }
    } else {
      var fit = null;
      for (var i = 0; i < TIERS.length; i++) if (t <= TIERS[i][1] && s <= TIERS[i][2]) { fit = TIERS[i]; break; }
      if (fit) { plan = fit[0]; why = L.suiteWhy(fit[1], fit[2]); price = vnd(fit[3]); }
      else { plan = L.custom; why = L.customWhy; price = L.quote; unit = ''; tone = 'indigo'; }
      extras.push(st.kind === 'intl' || st.kind === 'uni' ? L.seats(vnd(s * 100000), s) : L.noSeats);
      extras.push(L.pilot);
    }
    res.setAttribute('data-tone', tone);
    out('plan').textContent = plan; out('why').textContent = why; out('price').textContent = price; out('unit').textContent = unit;
    var ex = out('extras'); ex.textContent = '';
    extras.forEach(function (x) { var p = document.createElement('p'); p.className = 'pf-x'; p.textContent = x; ex.appendChild(p); });
    var c = out('cta'); c.textContent = cta; c.href = href;
  }
  draw();
})();
