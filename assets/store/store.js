/* The Store (myteachersdeck.com/store/, owner 24 Nov 2026). Built by _build/store.py; no libraries.
 *
 *   Apps and plans   the asset deck (deck.js = the suite's facepicker.js) with one card per app; the middle card's plans
 *                    show under it. TeachersDeck Pro and ParentDeck Pro are bought here.
 *   Premium assets   TeachersDeck's Shop items in a grid, read live from the backend (getTeacherStore), with a basket.
 *   Checkout         createOrder { channel:'web' } (backend v2.36.0): the VietQR code with the order code as the transfer
 *                    note. The page polls getOrder; once the owner marks it paid it shows the key (Pro) or the store key
 *                    (Shop items) and a link that opens the web app and switches it on (#redeem=KEY).
 *
 * Orders are remembered in this browser (localStorage td_store_orders: id, secret, what was bought) so a buyer can close
 * the page and come back; the secret only lets this browser read its own order. The store key is remembered too
 * (td_store_key) so later Shop orders add to it. Nothing here decides a price: the server prices every order.
 */
(function () {
  'use strict';
  var LANG = document.documentElement.lang === 'vi' ? 'vi' : 'en';
  var T = {
    en: {
      plans: 'Plans', buy: 'Buy', choose: 'Choose', quote: 'Find out more', yours: 'Yours', add: 'Add', added: 'In basket', remove: 'Remove',
      all: 'All', themes: 'Themes', faces: 'Watch & clock faces', docks: 'Docks', features: 'Features',
      basket: 'Basket', items: '{n} items', item: '1 item', checkout: 'Checkout', clear: 'Empty', total: 'Total',
      loading: 'Opening the Shop…', shopFail: 'The Shop could not open. Check your connection and reload the page.',
      email: 'Email for your key and receipt', name: 'Your name (optional)', pay: 'Pay with VietQR', cancel: 'Close',
      emailBad: 'Please enter a valid email: your key is sent there.', keyIn: 'Add to my store key',
      keyHint: 'Shop items go on a store key. You have one, so these are added to it.', keyNew: 'You will get a store key that carries these items to any computer.',
      keyForget: 'Use a new key instead', scan: 'Scan with your banking app', amount: 'Amount', note: 'Transfer note (must stay exactly)',
      copy: 'Copy', copied: 'Copied', account: 'Account', bank: 'Bank', holder: 'Account name',
      wait: 'Waiting for your transfer. We confirm it and your key appears here and in your email. You can close this page: we remember the order in this browser.',
      paid: 'Paid. Thank you!', proKey: 'Your key', storeKey: 'Your store key', open: 'Open {app} with this key', openStore: 'Open TeachersDeck with this key',
      howPro: 'Open the link on the computer you teach with: Pro switches on there. Or in TeachersDeck: Settings → Pro → enter the key.',
      howPd: 'Open the link and sign in: Pro goes on your ParentDeck account and every child you link.',
      howSk: 'Open the link on each computer you use, or in TeachersDeck: Theme → Shop → I have a store key.',
      orders: 'Your orders', pending: 'Waiting for payment', expired: 'Expired', cancelled: 'Cancelled', refunded: 'Refunded', show: 'Show', hide: 'Hide', forget: 'Remove',
      err: 'The order could not be made. Try again in a minute.', errOpen: 'You already have unpaid orders. Pay one or wait for it to expire.',
      errFounding: 'The founding places are all taken. Choose Monthly or Yearly.', errOwned: 'Your store key already has one of these items.',
      errOff: 'Payments are paused just now. Please try again later.', errKey: 'That store key is not known. Check it, or use a new key.',
      per: '{price} {per}', founding: 'Founding', min: 'Minimum order {v}.',
    },
    vi: {
      plans: 'Các gói', buy: 'Mua', choose: 'Chọn', quote: 'Xem thêm', yours: 'Của bạn', add: 'Thêm', added: 'Trong giỏ', remove: 'Bỏ',
      all: 'Tất cả', themes: 'Giao diện', faces: 'Mặt đồng hồ', docks: 'Dock', features: 'Tính năng',
      basket: 'Giỏ hàng', items: '{n} mục', item: '1 mục', checkout: 'Thanh toán', clear: 'Xóa giỏ', total: 'Tổng',
      loading: 'Đang mở cửa hàng…', shopFail: 'Không mở được cửa hàng. Kiểm tra kết nối rồi tải lại trang.',
      email: 'Email nhận mã và biên nhận', name: 'Tên của bạn (không bắt buộc)', pay: 'Thanh toán VietQR', cancel: 'Đóng',
      emailBad: 'Vui lòng nhập email hợp lệ: mã sẽ được gửi đến đó.', keyIn: 'Thêm vào mã cửa hàng của tôi',
      keyHint: 'Các mục trong cửa hàng nằm trên một mã cửa hàng. Bạn đã có mã, nên các mục này được thêm vào đó.', keyNew: 'Bạn sẽ nhận một mã cửa hàng đưa các mục này đến mọi máy tính.',
      keyForget: 'Dùng mã mới', scan: 'Quét bằng ứng dụng ngân hàng', amount: 'Số tiền', note: 'Nội dung chuyển khoản (giữ nguyên)',
      copy: 'Sao chép', copied: 'Đã sao chép', account: 'Số tài khoản', bank: 'Ngân hàng', holder: 'Tên tài khoản',
      wait: 'Đang chờ chuyển khoản. Chúng tôi xác nhận rồi mã hiện ở đây và trong email của bạn. Bạn có thể đóng trang: đơn được ghi nhớ trong trình duyệt này.',
      paid: 'Đã thanh toán. Cảm ơn bạn!', proKey: 'Mã của bạn', storeKey: 'Mã cửa hàng của bạn', open: 'Mở {app} với mã này', openStore: 'Mở TeachersDeck với mã này',
      howPro: 'Mở đường liên kết trên máy tính bạn dạy: Pro bật trên máy đó. Hoặc trong TeachersDeck: Cài đặt → Pro → nhập mã.',
      howPd: 'Mở đường liên kết và đăng nhập: Pro vào tài khoản ParentDeck của bạn và mọi con bạn liên kết.',
      howSk: 'Mở đường liên kết trên mỗi máy bạn dùng, hoặc trong TeachersDeck: Giao diện → Cửa hàng → Tôi có mã cửa hàng.',
      orders: 'Đơn của bạn', pending: 'Chờ thanh toán', expired: 'Hết hạn', cancelled: 'Đã hủy', refunded: 'Đã hoàn tiền', show: 'Xem', hide: 'Ẩn', forget: 'Xóa',
      err: 'Chưa tạo được đơn. Thử lại sau một phút.', errOpen: 'Bạn đang có đơn chưa thanh toán. Thanh toán một đơn hoặc chờ đơn hết hạn.',
      errFounding: 'Đã hết suất sáng lập. Hãy chọn Theo tháng hoặc Theo năm.', errOwned: 'Mã cửa hàng của bạn đã có một trong các mục này.',
      errOff: 'Thanh toán đang tạm dừng. Vui lòng thử lại sau.', errKey: 'Không tìm thấy mã cửa hàng này. Kiểm tra lại hoặc dùng mã mới.',
      per: '{price} {per}', founding: 'Sáng lập', min: 'Đơn tối thiểu {v}.',
    },
  }[LANG];
  var REDEEM = { teachersdeck: 'https://teacher.myteachersdeck.com/#redeem=', parentdeck: 'https://parent.myteachersdeck.com/#redeem=' };
  var APP_NAME = { teachersdeck: 'TeachersDeck', parentdeck: 'ParentDeck' };
  var ORDERS_LS = 'td_store_orders', KEY_LS = 'td_store_key', EMAIL_LS = 'td_store_email', POLL_MS = 10000;

  function $(s, r) { return (r || document).querySelector(s); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function fmt(s, o) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k] != null ? o[k] : ''; }); }
  function vnd(n) { return Number(n).toLocaleString(LANG === 'vi' ? 'vi-VN' : 'en-US').replace(/,/g, LANG === 'vi' ? '.' : ',') + '₫'; }
  function lsGet(k, d) { try { var v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }
  function lsSet(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: the page still works, it just forgets */ } }
  function cleanKey(k) { var s = String(k || '').trim().toUpperCase().replace(/\s+/g, ''); return /^SK-[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{4}$/.test(s) ? s : null; }

  /* ---------- the backend: wherever myteachersdeck.com/backend.json says it is (Google or the standby server) ---------- */
  var basePromise = null;
  function base() {
    if (!basePromise) basePromise = fetch('/backend.json', { cache: 'no-store' }).then(function (r) { return r.json(); })
      .then(function (j) { if (!j || !/^https:\/\//.test(j.functions || '')) throw new Error('no backend'); return j.functions.replace(/\/$/, ''); });
    return basePromise;
  }
  function call(fn, body) {
    return base().then(function (b) {
      return fetch(b + '/' + fn, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok) { var e = new Error(j.error || ('HTTP ' + r.status)); e.status = r.status; e.code = j.code; throw e; }
        return j;
      });
    });
  }

  /* ================= Apps and plans: the deck ================= */
  var APPS = [];
  try { APPS = JSON.parse(($('#store-apps') || {}).textContent || '[]'); } catch (e) { APPS = []; }
  var planBox = null, deckApi = null, chosenPlan = {};

  function appArt(a) {
    var c = (a.art && a.art[2]) || 'indigo';
    return '<span class="st-appart st-' + c + '"><b>' + esc(a.art ? a.art[0] : 'Pro') + '</b><i>' + esc(a.art ? a.art[1] : a.name) + '</i></span>';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function showPlans(a) {
    if (!planBox) return;
    planBox.innerHTML = '';
    var h = el('h3', 'st-plan-name', a.name); planBox.appendChild(h);
    planBox.appendChild(el('p', 'st-plan-sub', a.sub));
    if (a.plans && a.plans.length) {
      var list = el('div', 'st-plan-list'); list.setAttribute('role', 'radiogroup'); list.setAttribute('aria-label', T.plans);
      var pick = chosenPlan[a.key] == null ? 1 : chosenPlan[a.key];
      a.plans.forEach(function (p, i) {
        var b = el('button', 'st-plan'); b.type = 'button'; b.setAttribute('role', 'radio'); b.setAttribute('aria-checked', i === pick ? 'true' : 'false');
        b.appendChild(el('span', 'st-plan-l', p.label));
        b.appendChild(el('span', 'st-plan-p', fmt(T.per, { price: vnd(p.price), per: p.per })));
        if (p.note) b.appendChild(el('span', 'st-plan-n', p.note));
        b.addEventListener('click', function () { chosenPlan[a.key] = i; showPlans(a); var again = planBox.querySelectorAll('.st-plan')[i]; if (again) again.focus(); });
        list.appendChild(b);
      });
      planBox.appendChild(list);
      var go = el('button', 'btn primary st-plan-buy', T.buy + ' · ' + vnd(a.plans[pick].price));
      go.type = 'button';
      go.addEventListener('click', function () { var p = a.plans[pick]; openCheckout({ kind: 'pro', app: a, plan: p }); });
      planBox.appendChild(go);
      if (a.how) planBox.appendChild(el('p', 'note st-plan-how', a.how));
    } else if (a.link) {
      var l = el('a', 'btn primary st-plan-buy', a.link.text);
      if (a.link.goto) { l.href = '#apps-plans'; l.addEventListener('click', function (e) { e.preventDefault(); if (deckApi) deckApi.update(deckOptions(), ''); moveDeckTo(a.link.goto); }); }
      else l.href = a.link.href;
      planBox.appendChild(l);
    }
  }
  function deckOptions() {
    return APPS.map(function (a) { return { key: a.key, name: a.name, group: a.group, badge: a.badge, html: appArt(a) }; });
  }
  var atKey = 'teachersdeck';
  function moveDeckTo(key) {   // the inline deck has no "go to" call: redraw it with that card in the middle
    var host = $('[data-store-apps]'); if (!host) return;
    atKey = key; buildDeck(host);
    var a = APPS.filter(function (x) { return x.key === key; })[0]; if (a) showPlans(a);
  }
  function buildDeck(host) {
    host.innerHTML = '';
    var deckHost = el('div', 'st-deck'); host.appendChild(deckHost);
    planBox = el('div', 'st-planbox'); planBox.setAttribute('aria-live', 'polite'); host.appendChild(planBox);
    deckApi = window.FacePicker.inline(deckHost, {
      lang: LANG, title: T.plans, options: deckOptions(), current: '', at: atKey,
      pickLabel: function (o) { var a = APPS.filter(function (x) { return x.key === o.key; })[0]; return a && a.plans ? T.choose : T.quote; },
      onMove: function (o) { var a = APPS.filter(function (x) { return x.key === o.key; })[0]; if (a) { atKey = a.key; showPlans(a); } },
      onPick: function (key) {
        var a = APPS.filter(function (x) { return x.key === key; })[0]; if (!a) return;
        showPlans(a);
        var f = planBox.querySelector('[aria-checked="true"]') || planBox.querySelector('.st-plan-buy'); if (f) f.focus();
      },
    });
  }

  /* ================= Premium assets: the grid ================= */
  var CATALOG = [], PREVIEWS = {}, OWNED = {}, MIN = 0, basket = {}, filter = 'all';
  var KIND_LABEL = { theme: T.themes, face: T.faces, dock: T.docks, feature: T.features };

  function artFor(item) {
    var art = el('div', 'st-art st-art-' + item.kind);
    var pv = PREVIEWS[item.sku], first = pv && pv.items && pv.items[0];
    var SC = window.StoreCore, FP = window.FacePicker;
    if (item.kind === 'theme' && first && SC) { art.style.background = SC.themeBackground(first, false); art.appendChild(el('span', 'fp-mock')); }
    else if (item.kind === 'face' && first && first.svg && SC) { art.innerHTML = SC.scopeSvg(first.svg, 'st' + item.sku.replace(/[^a-z0-9]/g, '') + '-'); }   // validated by the backend's StoreCore before it is served
    else if (item.kind === 'dock' && first && FP) { art.innerHTML = FP.dockArt(first.style, first.swatch); }
    else if (item.kind === 'feature') { art.innerHTML = '<svg viewBox="0 0 64 48" aria-hidden="true"><rect x="4" y="4" width="56" height="36" rx="4" fill="#fff" stroke="currentColor" stroke-width="2"/><path d="M12 30c6-12 10-12 14-4s8 8 14-6" fill="none" stroke="#4A55B8" stroke-width="3" stroke-linecap="round"/><path d="M40 30l10-10" stroke="#EE5A3C" stroke-width="3" stroke-linecap="round"/><rect x="26" y="40" width="12" height="5" rx="2" fill="currentColor"/></svg>'; }
    else if (first && first.swatch) { var d = el('span', 'fp-dot'); d.style.background = first.swatch; art.appendChild(d); }
    return art;
  }
  function renderGrid() {
    var host = $('[data-store-assets]'); if (!host) return;
    host.innerHTML = '';
    var kinds = ['theme', 'face', 'dock', 'feature'].filter(function (k) { return CATALOG.some(function (i) { return i.kind === k; }); });
    var chips = el('div', 'st-chips'); chips.setAttribute('role', 'group'); chips.setAttribute('aria-label', T.items.replace('{n} ', ''));
    ['all'].concat(kinds).forEach(function (k) {
      var c = el('button', 'st-chip', k === 'all' ? T.all : KIND_LABEL[k]); c.type = 'button';
      c.setAttribute('aria-pressed', filter === k ? 'true' : 'false');
      c.addEventListener('click', function () { filter = k; renderGrid(); var again = host.querySelector('.st-chip[aria-pressed="true"]'); if (again) again.focus(); });
      chips.appendChild(c);
    });
    host.appendChild(chips);
    var grid = el('div', 'st-grid');
    CATALOG.filter(function (i) { return filter === 'all' || i.kind === filter; }).forEach(function (item) {
      var card = el('article', 'st-item');
      card.appendChild(artFor(item));
      var body = el('div', 'st-body');
      body.appendChild(el('h3', null, item.name[LANG] || item.name.en));
      if (item.blurb) body.appendChild(el('p', null, item.blurb[LANG] || item.blurb.en));
      card.appendChild(body);
      var foot = el('div', 'st-foot');
      foot.appendChild(el('span', 'st-price', vnd(item.price)));
      var b = el('button', 'st-add'); b.type = 'button';
      if (OWNED[item.sku]) { b.textContent = T.yours; b.disabled = true; card.classList.add('owned'); }
      else {
        var on = !!basket[item.sku];
        b.textContent = on ? T.added : T.add; b.setAttribute('aria-pressed', on ? 'true' : 'false');
        b.setAttribute('aria-label', (on ? T.remove : T.add) + ': ' + (item.name[LANG] || item.name.en));
        b.addEventListener('click', function () {
          if (basket[item.sku]) delete basket[item.sku]; else basket[item.sku] = item;
          renderGrid(); renderBasket();
          var again = host.querySelector('[data-sku="' + item.sku + '"] .st-add'); if (again) again.focus();
        });
      }
      card.dataset.sku = item.sku;
      foot.appendChild(b);
      card.appendChild(foot);
      grid.appendChild(card);
    });
    host.appendChild(grid);
    if (MIN) host.appendChild(el('p', 'note', fmt(T.min, { v: vnd(MIN) })));
  }
  function loadShop() {
    var host = $('[data-store-assets]'); if (!host) return;
    host.innerHTML = ''; host.appendChild(el('p', 'note', T.loading));
    var key = cleanKey(lsGet(KEY_LS, null));
    call('getTeacherStore', key ? { storeKey: key } : {}).then(function (r) {
      CATALOG = (r.catalog || []).filter(function (i) { return i.tier === 'paid'; });
      PREVIEWS = r.previews || {}; MIN = r.minOrder || 0; OWNED = {};
      (r.owned || []).forEach(function (s) { OWNED[s] = true; });
      if (key && r.known === false) lsSet(KEY_LS, null);
      renderGrid(); renderBasket();
    }, function () { host.innerHTML = ''; host.appendChild(el('p', 'note', T.shopFail)); });
  }

  /* ---------- the basket bar ---------- */
  var bar = null;
  function renderBasket() {
    var skus = Object.keys(basket);
    if (!bar) {
      bar = el('div', 'st-bar'); bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', T.basket);
      document.body.appendChild(bar);
    }
    bar.hidden = !skus.length;
    document.documentElement.classList.toggle('st-has-bar', !!skus.length);
    if (!skus.length) return;
    var total = skus.reduce(function (s, k) { return s + basket[k].price; }, 0);
    bar.innerHTML = '';
    bar.appendChild(el('span', 'st-bar-n', skus.length === 1 ? T.item : fmt(T.items, { n: skus.length })));
    bar.appendChild(el('b', 'st-bar-t', vnd(total)));
    var clear = el('button', 'st-bar-clear', T.clear); clear.type = 'button';
    clear.addEventListener('click', function () { basket = {}; renderGrid(); renderBasket(); });
    var go = el('button', 'btn primary st-bar-go', T.checkout); go.type = 'button';
    go.disabled = total < MIN;
    go.addEventListener('click', function () { openCheckout({ kind: 'items', skus: skus.slice(), lines: skus.map(function (k) { return basket[k]; }), total: total }); });
    bar.appendChild(clear); bar.appendChild(go);
  }

  /* ================= Checkout ================= */
  var dlg = null, current = null, pollTimer = 0;
  function dialog() {
    if (dlg) return dlg;
    dlg = el('dialog', 'st-dlg');
    dlg.setAttribute('aria-labelledby', 'st-dlg-h');
    dlg.addEventListener('close', function () { clearTimeout(pollTimer); renderOrders(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    document.body.appendChild(dlg);
    return dlg;
  }
  function summaryOf(spec) {
    if (spec.kind === 'pro') return spec.app.name + ' · ' + spec.plan.label;
    return spec.lines.map(function (i) { return i.name[LANG] || i.name.en; }).join(', ');
  }
  function openCheckout(spec) {
    var d = dialog(); d.innerHTML = '';
    current = spec;
    var head = el('div', 'st-dlg-head');
    head.appendChild(el('h2', null, T.checkout)).id = 'st-dlg-h';
    var x = el('button', 'st-x', '×'); x.type = 'button'; x.setAttribute('aria-label', T.cancel); x.addEventListener('click', function () { d.close(); });
    head.appendChild(x); d.appendChild(head);
    var sum = el('div', 'st-sum');
    if (spec.kind === 'pro') {
      sum.appendChild(row(spec.app.name + ' · ' + spec.plan.label, vnd(spec.plan.price)));
    } else spec.lines.forEach(function (i) { sum.appendChild(row(i.name[LANG] || i.name.en, vnd(i.price))); });
    sum.appendChild(row(T.total, vnd(spec.kind === 'pro' ? spec.plan.price : spec.total), true));
    d.appendChild(sum);
    var form = el('form', 'st-form'); form.noValidate = true;
    var em = field(form, T.email, 'email', 'email'); em.value = lsGet(EMAIL_LS, '') || ''; em.required = true;
    var nm = field(form, T.name, 'text', 'name');
    var key = spec.kind === 'items' ? cleanKey(lsGet(KEY_LS, null)) : null, keyNote = null;
    if (spec.kind === 'items') {
      keyNote = el('p', 'note', key ? T.keyHint + ' ' + key : T.keyNew);
      form.appendChild(keyNote);
      if (key) {
        var forget = el('button', 'st-link', T.keyForget); forget.type = 'button';
        forget.addEventListener('click', function () { key = null; keyNote.textContent = T.keyNew; forget.remove(); });
        form.appendChild(forget);
      }
    }
    var msg = el('p', 'st-msg'); msg.setAttribute('role', 'alert'); msg.hidden = true; form.appendChild(msg);
    var go = el('button', 'btn primary st-pay', T.pay); go.type = 'submit'; form.appendChild(go);
    form.addEventListener('submit', function (e) {
      e.preventDefault(); msg.hidden = true;
      var email = em.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.textContent = T.emailBad; msg.hidden = false; em.focus(); return; }
      go.disabled = true;
      var body = spec.kind === 'pro'
        ? { channel: 'web', product: spec.app.product, cycle: spec.plan.cycle, founding: !!spec.plan.founding, email: email, name: nm.value.trim() }
        : { channel: 'web', product: 'items', app: 'teachersdeck', skus: spec.skus, email: email, name: nm.value.trim(), storeKey: key || undefined };
      call('createOrder', body).then(function (r) {
        lsSet(EMAIL_LS, email);
        var o = { id: r.id, secret: r.secret, token: r.token, amount: r.amount, what: summaryOf(spec), product: spec.kind === 'pro' ? spec.app.product : 'items', createdAt: Date.now(), status: 'pending' };
        var all = lsGet(ORDERS_LS, []); all.unshift(o); lsSet(ORDERS_LS, all.slice(0, 12));
        if (spec.kind === 'items') { basket = {}; renderGrid(); renderBasket(); }
        showPay(o, r);
      }, function (er) {
        msg.textContent = er.code === 'too-many-open' ? T.errOpen : er.code === 'founding-full' ? T.errFounding : er.code === 'owned' ? T.errOwned
          : er.code === 'payments-off' ? T.errOff : er.code === 'no-key' ? T.errKey : T.err;
        if (er.code === 'no-key') lsSet(KEY_LS, null);
        msg.hidden = false; go.disabled = false;
      });
    });
    d.appendChild(form);
    if (!d.open) d.showModal();
    (em.value ? go : em).focus();
  }
  function row(a, b, strong) { var r = el('div', 'st-row' + (strong ? ' st-row-total' : '')); r.appendChild(el('span', null, a)); r.appendChild(el('b', null, b)); return r; }
  function field(form, label, type, name) {
    var l = el('label', 'st-field'); l.appendChild(el('span', null, label));
    var i = el('input'); i.type = type; i.name = name; i.autocomplete = name === 'email' ? 'email' : 'name';
    l.appendChild(i); form.appendChild(l); return i;
  }
  function copyBtn(text) {
    var b = el('button', 'st-copy', T.copy); b.type = 'button';
    b.addEventListener('click', function () {
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { b.textContent = T.copied; setTimeout(function () { b.textContent = T.copy; }, 1500); }, function () { /* the text stays selectable */ });
    });
    return b;
  }

  /* step 2: the VietQR code; step 3 (paid): the key and the link */
  function showPay(o, info) {
    var d = dialog(); d.innerHTML = '';
    var head = el('div', 'st-dlg-head'); head.appendChild(el('h2', null, o.what)).id = 'st-dlg-h';
    var x = el('button', 'st-x', '×'); x.type = 'button'; x.setAttribute('aria-label', T.cancel); x.addEventListener('click', function () { d.close(); });
    head.appendChild(x); d.appendChild(head);
    var body = el('div', 'st-paybody'); d.appendChild(body);
    if (!d.open) d.showModal();
    paintPay(body, o, info);
    poll(o, body);
  }
  function paintPay(body, o, info) {
    body.innerHTML = '';
    if (info && info.status === 'paid') { paintPaid(body, o, info); return; }
    var q = info && info.qrUrl;
    if (q && /^https:\/\/img\.vietqr\.io\//.test(q)) { var im = el('img', 'st-qr'); im.alt = 'VietQR'; im.src = q; body.appendChild(el('p', 'st-scan', T.scan)); body.appendChild(im); }
    body.appendChild(row(T.amount, vnd(o.amount), true));
    var tok = el('div', 'st-token'); tok.appendChild(el('span', null, T.note)); var tb = el('b', null, o.token); tok.appendChild(tb); tok.appendChild(copyBtn(o.token));
    body.appendChild(tok);
    var b = (info && info.bank) || {};
    if (b.account) {
      var bk = el('div', 'st-bank');
      if (b.accountName) bk.appendChild(row(T.holder, b.accountName));
      var acc = row(T.account, b.account); acc.appendChild(copyBtn(b.account)); bk.appendChild(acc);
      if (b.bankName) bk.appendChild(row(T.bank, b.bankName));
      body.appendChild(bk);
    }
    var w = el('p', 'note st-wait', T.wait); w.setAttribute('aria-live', 'polite'); body.appendChild(w);
  }
  function paintPaid(body, o, info) {
    body.innerHTML = '';
    body.appendChild(el('p', 'st-paid', T.paid));
    var isItems = o.product === 'items';
    var key = isItems ? info.storeKey : info.key;
    if (!key) return;
    if (isItems) lsSet(KEY_LS, key);
    var box = el('div', 'st-key');
    box.appendChild(el('span', null, isItems ? T.storeKey : T.proKey));
    box.appendChild(el('code', null, key));
    box.appendChild(copyBtn(key));
    body.appendChild(box);
    var app = isItems ? 'teachersdeck' : o.product;
    var a = el('a', 'btn primary st-open', isItems ? T.openStore : fmt(T.open, { app: APP_NAME[app] || 'TeachersDeck' }));
    a.href = (REDEEM[app] || REDEEM.teachersdeck) + encodeURIComponent(key); a.target = '_blank'; a.rel = 'noopener';
    body.appendChild(a);
    body.appendChild(el('p', 'note', isItems ? T.howSk : app === 'parentdeck' ? T.howPd : T.howPro));
    if (isItems) loadShop();   // the grid now shows them as yours
  }
  function poll(o, body) {
    clearTimeout(pollTimer);
    var tick = function () {
      call('getOrder', { id: o.id, secret: o.secret }).then(function (r) {
        saveStatus(o.id, r);
        if (!dlg || !dlg.open) return;
        if (r.status === 'paid') { paintPaid(body, o, r); return; }
        if (r.status !== 'pending' || r.expired) { body.innerHTML = ''; body.appendChild(el('p', 'note', T[r.expired ? 'expired' : r.status] || r.status)); return; }
        if (!body.querySelector('.st-qr') && r.qrUrl) paintPay(body, o, r);
        pollTimer = setTimeout(tick, POLL_MS);
      }, function () { if (dlg && dlg.open) pollTimer = setTimeout(tick, POLL_MS * 2); });
    };
    tick();
  }
  function saveStatus(id, r) {
    var all = lsGet(ORDERS_LS, []), changed = false;
    all.forEach(function (o) {
      if (o.id !== id) return;
      var st = r.expired ? 'expired' : r.status;
      if (o.status !== st) { o.status = st; changed = true; }
      var k = o.product === 'items' ? r.storeKey : r.key;
      if (k && o.key !== k) { o.key = k; changed = true; }
    });
    if (changed) lsSet(ORDERS_LS, all);
  }

  /* ---------- "Your orders": what this browser bought, so nobody loses a key by closing the page ---------- */
  function renderOrders() {
    var box = $('#st-orders'); if (!box) return;
    var all = lsGet(ORDERS_LS, []);
    box.hidden = !all.length; box.innerHTML = '';
    if (!all.length) return;
    box.appendChild(el('h3', null, T.orders));
    var ul = el('ul', 'st-olist');
    all.forEach(function (o) {
      var li = el('li', 'st-o st-o-' + (o.status || 'pending'));
      li.appendChild(el('span', 'st-o-what', o.what));
      li.appendChild(el('span', 'st-o-tok', o.token));
      var st = o.status === 'paid' ? (o.key || T.paid) : (T[o.status] || T.pending);
      li.appendChild(el('span', 'st-o-st', st));
      var open = el('button', 'st-link', T.show); open.type = 'button';
      open.addEventListener('click', function () {
        call('getOrder', { id: o.id, secret: o.secret }).then(function (r) { saveStatus(o.id, r); showPay(o, r); }, function () { showPay(o, null); });
      });
      li.appendChild(open);
      if (o.status !== 'pending') {
        var rm = el('button', 'st-link', T.forget); rm.type = 'button';
        rm.addEventListener('click', function () { lsSet(ORDERS_LS, lsGet(ORDERS_LS, []).filter(function (x) { return x.id !== o.id; })); renderOrders(); });
        li.appendChild(rm);
      }
      ul.appendChild(li);
    });
    box.appendChild(ul);
  }
  function refreshOrders() {   // one look at every unfinished order when the page opens
    var all = lsGet(ORDERS_LS, []).filter(function (o) { return o.status === 'pending' || (o.status === 'paid' && !o.key); });
    if (!all.length) { renderOrders(); return; }
    Promise.all(all.map(function (o) {
      return call('getOrder', { id: o.id, secret: o.secret }).then(function (r) { saveStatus(o.id, r); }, function (e) { if (e.status === 404) saveStatus(o.id, { status: 'cancelled' }); });
    })).then(renderOrders, renderOrders);
  }

  function start() {
    var host = $('[data-store-apps]');
    if (host && window.FacePicker && APPS.length) buildDeck(host);
    if (APPS.length) showPlans(APPS[0]);
    loadShop();
    refreshOrders();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
