/*!
 * AgentDeck — the TeachersDeck website assistant, floating chat widget.
 * Plain JavaScript, no dependencies, styles isolated in a shadow root.
 *
 * Embed (before </body>):
 *   <script src="/assets/agentdeck.js" defer
 *           data-endpoint="https://asia-southeast1-teachersdeck-b5720.cloudfunctions.net/agentChat"></script>
 *
 * Optional attributes: data-lang="en|vi" (default: <html lang>), data-open="1" (start open),
 *   data-icon="chat|deck|spark" (button icon, default chat).
 * Colours follow the page's CSS variables (--accent, --surface, --text, ...) with fallbacks,
 * so it matches light and dark themes on myteachersdeck.com automatically.
 */
(function () {
  'use strict';
  if (window.__agentDeckLoaded) return;
  window.__agentDeckLoaded = true;

  var script = document.currentScript || document.querySelector('script[data-endpoint][src*="agentdeck"]');
  var ENDPOINT = script && script.getAttribute('data-endpoint');
  if (!ENDPOINT) { console.warn('[AgentDeck] data-endpoint is missing'); return; }
  var LANG = ((script.getAttribute('data-lang') || document.documentElement.lang || 'en').slice(0, 2) === 'vi') ? 'vi' : 'en';
  var STORE_KEY = 'agentdeck_v1';

  // Button icons (24x24, drawn in the button's text colour). Pick one with data-icon.
  var ICONS = {
    // 1. Speech bubble: instantly reads as "chat".
    chat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01"/></svg>',
    // 2. Deck: the TeachersDeck bento tiles, one tile turned into an AI sparkle.
    deck: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">' +
      '<rect x="3" y="3" width="8" height="8" rx="2.2"/><rect x="3" y="13" width="8" height="8" rx="2.2"/><rect x="13" y="13" width="8" height="8" rx="2.2"/>' +
      '<path d="M17 2.6l1.25 2.9 2.9 1.25-2.9 1.25L17 10.9l-1.25-2.9-2.9-1.25 2.9-1.25z" fill="currentColor" stroke-width="1"/></svg>',
    // 3. Spark: an assistant star with a small companion star.
    spark: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
      '<path d="M10 2.5l1.9 5.6 5.6 1.9-5.6 1.9L10 17.5l-1.9-5.6L2.5 10l5.6-1.9z"/>' +
      '<path d="M18 13.5l1 2.5 2.5 1-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1z"/></svg>',
  };
  var ICON = ICONS[script.getAttribute('data-icon')] || ICONS.chat;

  var T = {
    en: {
      open: 'Chat with AgentDeck, the TeachersDeck assistant', close: 'Close chat', title: 'AgentDeck', subtitle: 'TeachersDeck assistant · AI',
      hello: "Hi! I'm AgentDeck, the TeachersDeck assistant. Ask me about the apps, prices, getting started, or a problem you're having.",
      chips: ['What is TeachersDeck Suite?', 'How much does it cost?', 'Can I try it for free?', 'I need help with an app'],
      placeholder: 'Type your question…', send: 'Send', thinking: 'AgentDeck is typing…',
      privacy: 'AI answers can be wrong. Chats are saved to improve support — please don’t share students’ personal details.',
      error: 'Something went wrong. Please email jerry@myteachersdeck.com or message us on Zalo (0705 247 680).',
      sources: 'From:', reset: 'New chat', lead: 'Sent to the team ✓', ticket: 'Passed to a person ✓',
    },
    vi: {
      open: 'Trò chuyện với AgentDeck, trợ lý TeachersDeck', close: 'Đóng khung chat', title: 'AgentDeck', subtitle: 'Trợ lý TeachersDeck · AI',
      hello: 'Xin chào! Mình là AgentDeck, trợ lý của TeachersDeck. Bạn cứ hỏi về các ứng dụng, giá, cách bắt đầu, hoặc vấn đề bạn đang gặp nhé.',
      chips: ['TeachersDeck Suite là gì?', 'Giá bao nhiêu?', 'Có dùng thử miễn phí không?', 'Mình cần hỗ trợ một ứng dụng'],
      placeholder: 'Nhập câu hỏi của bạn…', send: 'Gửi', thinking: 'AgentDeck đang trả lời…',
      privacy: 'Câu trả lời của AI có thể sai. Cuộc trò chuyện được lưu để cải thiện hỗ trợ — xin đừng chia sẻ thông tin cá nhân của học sinh.',
      error: 'Có lỗi xảy ra. Bạn email jerry@myteachersdeck.com hoặc nhắn Zalo 0705 247 680 nhé.',
      sources: 'Nguồn:', reset: 'Chat mới', lead: 'Đã gửi cho đội ngũ ✓', ticket: 'Đã chuyển cho nhân viên ✓',
    },
  }[LANG];

  // ---------- state (sessionStorage: survives page navigation, not a new tab) ----------
  var state = { open: false, conversationId: null, messages: [] };
  try {
    var saved = JSON.parse(sessionStorage.getItem(STORE_KEY) || 'null');
    if (saved && Array.isArray(saved.messages)) state = saved;
  } catch (e) { /* storage blocked: work in memory */ }
  function save() {
    try { sessionStorage.setItem(STORE_KEY, JSON.stringify({ open: state.open, conversationId: state.conversationId, messages: state.messages.slice(-30) })); } catch (e) {}
  }

  // ---------- safe mini-Markdown: escape first, then links, bold, lists ----------
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function safeUrl(u) { return /^(https?:\/\/|mailto:)/i.test(u) ? u : null; }
  function link(text, url) { return '<a href="' + url + '" target="_blank" rel="noopener">' + text + '</a>'; }
  function inline(s) {
    var out = esc(s);
    var held = [];
    // [text](url)
    out = out.replace(/\[([^\]]{1,200})\]\(([^)\s]{1,500})\)/g, function (m, t, u) {
      var url = safeUrl(u.replace(/&amp;/g, '&'));
      if (!url) return t;
      held.push(link(t, esc(url)));
      return '\u0000' + (held.length - 1) + '\u0000';
    });
    // bare URLs and emails
    out = out.replace(/\bhttps?:\/\/[^\s<]+[^\s<.,;:!?)\]'"]/g, function (u) {
      held.push(link(u, u));
      return '\u0000' + (held.length - 1) + '\u0000';
    });
    out = out.replace(/\b[\w.+-]+@[\w-]+\.[\w.-]+\b/g, function (e) { return link(e, 'mailto:' + e); });
    out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    return out.replace(/\u0000(\d+)\u0000/g, function (m, i) { return held[+i]; });
  }
  function render(md) {
    var lines = String(md).split(/\r?\n/);
    var html = '';
    var list = null;
    lines.forEach(function (line) {
      var m = /^\s*(?:[-*•]|(\d+)[.)])\s+(.*)$/.exec(line);
      if (m) {
        var tag = m[1] ? 'ol' : 'ul';
        if (list !== tag) { if (list) html += '</' + list + '>'; html += '<' + tag + '>'; list = tag; }
        html += '<li>' + inline(m[2]) + '</li>';
        return;
      }
      if (list) { html += '</' + list + '>'; list = null; }
      var h = /^#{1,4}\s+(.*)$/.exec(line);
      if (h) html += '<p><strong>' + inline(h[1]) + '</strong></p>';
      else if (line.trim()) html += '<p>' + inline(line) + '</p>';
    });
    if (list) html += '</' + list + '>';
    return html;
  }

  // ---------- DOM ----------
  var host = document.createElement('div');
  host.id = 'agentdeck';
  document.body.appendChild(host);
  var root = host.attachShadow({ mode: 'open' });
  root.innerHTML =
    '<style>' +
    ':host{all:initial;--a:var(--accent,#4A55B8);--on-a:var(--on-accent,#fff);--sf:var(--surface,#fff);--tx:var(--text,#161C25);' +
    '--mu:var(--muted,#4D5565);--ln:var(--line,rgba(22,28,37,.13));--pg:var(--bg,#F3F5FC);font:15px/1.5 Inter,system-ui,sans-serif;color:var(--tx)}' +
    '*{box-sizing:border-box}' +
    '.fab{position:fixed;right:max(18px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));z-index:2147483000;width:60px;height:60px;border-radius:50%;border:0;cursor:pointer;' +
    'background:var(--a);color:var(--on-a);box-shadow:0 12px 28px -8px rgba(0,0,0,.35);display:grid;place-items:center;transition:transform .15s ease}' +
    '.fab:hover{transform:translateY(-2px)}.fab svg{width:28px;height:28px}.dot svg{width:20px;height:20px}.fab:focus-visible,button:focus-visible,textarea:focus-visible,a:focus-visible{outline:3px solid var(--a);outline-offset:2px}' +
    '.panel{position:fixed;right:max(18px,env(safe-area-inset-right));bottom:calc(max(18px,env(safe-area-inset-bottom)) + 72px);z-index:2147483000;width:380px;max-width:calc(100vw - 24px);' +
    'height:min(600px,calc(100vh - 120px));display:flex;flex-direction:column;background:var(--sf);color:var(--tx);border:1px solid var(--ln);border-radius:22px;overflow:hidden;' +
    'box-shadow:0 30px 60px -24px rgba(0,0,0,.35),0 8px 20px rgba(0,0,0,.08)}' +
    '.panel[hidden]{display:none}' +
    '.head{display:flex;align-items:center;gap:10px;padding:14px 14px 12px 16px;border-bottom:1px solid var(--ln)}' +
    '.dot{width:36px;height:36px;border-radius:12px;background:var(--a);color:var(--on-a);display:grid;place-items:center;font:700 16px Quicksand,Inter,sans-serif;flex:none}' +
    '.who{flex:1;min-width:0}.who b{display:block;font:700 16px Quicksand,Inter,sans-serif}.who span{font-size:12px;color:var(--mu)}' +
    '.icon{border:0;background:transparent;color:var(--mu);cursor:pointer;border-radius:10px;padding:6px 8px;font:500 12px Inter,sans-serif}.icon:hover{background:var(--pg);color:var(--tx)}' +
    '.log{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:var(--pg);overscroll-behavior:contain}' +
    '.msg{max-width:88%;padding:10px 13px;border-radius:16px;word-wrap:break-word;overflow-wrap:anywhere}' +
    '.msg p{margin:0 0 6px}.msg p:last-child{margin:0}.msg ul,.msg ol{margin:4px 0 6px;padding-left:20px}.msg a{color:inherit;text-decoration:underline}' +
    '.bot{align-self:flex-start;background:var(--sf);border:1px solid var(--ln);border-bottom-left-radius:6px}' +
    '.me{align-self:flex-end;background:var(--a);color:var(--on-a);border-bottom-right-radius:6px;white-space:pre-wrap}' +
    '.src{font-size:12px;color:var(--mu);margin-top:6px}.src a{color:var(--mu)}' +
    '.tag{align-self:flex-start;font-size:12px;color:var(--mu);padding:0 4px}' +
    '.chips{display:flex;flex-wrap:wrap;gap:6px}.chip{border:1px solid var(--a);color:var(--a);background:var(--sf);border-radius:999px;padding:6px 12px;font:500 13px Inter,sans-serif;cursor:pointer}' +
    '.chip:hover{background:var(--a);color:var(--on-a)}' +
    '.typing{align-self:flex-start;color:var(--mu);font-size:13px;display:flex;align-items:center;gap:6px}' +
    '.typing i{width:6px;height:6px;border-radius:50%;background:currentColor;animation:b 1s infinite ease-in-out}.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}' +
    '@keyframes b{0%,80%,100%{opacity:.25}40%{opacity:1}}@media (prefers-reduced-motion:reduce){.typing i{animation:none}.fab{transition:none}}' +
    'form{display:flex;gap:8px;padding:10px 12px 6px;border-top:1px solid var(--ln);background:var(--sf)}' +
    'textarea{flex:1;resize:none;border:1px solid var(--ln);border-radius:14px;padding:10px 12px;font:15px/1.4 Inter,system-ui,sans-serif;color:var(--tx);background:var(--pg);max-height:120px}' +
    '.send{border:0;border-radius:14px;padding:0 16px;background:var(--a);color:var(--on-a);font:600 14px Inter,sans-serif;cursor:pointer}.send:disabled{opacity:.5;cursor:default}' +
    '.note{font-size:11px;line-height:1.4;color:var(--mu);padding:2px 14px 10px;background:var(--sf)}' +
    '@media (max-width:520px){.panel{right:0;left:0;bottom:0;top:0;width:auto;max-width:none;height:auto;border-radius:0;border:0}.panel:not([hidden])~.fab{display:none}}' +
    '</style>' +
    '<div class="panel" role="dialog" aria-modal="false" aria-labelledby="td-title" hidden>' +
    '<div class="head"><div class="dot" aria-hidden="true">' + ICON + '</div><div class="who"><b id="td-title"></b><span class="sub"></span></div>' +
    '<button class="icon reset" type="button"></button><button class="icon x" type="button">✕</button></div>' +
    '<div class="log" role="log" aria-live="polite"></div>' +
    '<form><textarea rows="1" maxlength="1000"></textarea><button class="send" type="submit"></button></form>' +
    '<div class="note"></div></div>' +
    '<button class="fab" type="button" aria-expanded="false">' + ICON + '</button>';

  var $ = function (s) { return root.querySelector(s); };
  var panel = $('.panel'), log = $('.log'), form = $('form'), input = $('textarea'), sendBtn = $('.send'), fab = $('.fab');
  $('#td-title').textContent = T.title;
  $('.sub').textContent = T.subtitle;
  $('.reset').textContent = T.reset;
  $('.x').setAttribute('aria-label', T.close);
  $('.note').textContent = T.privacy;
  input.placeholder = T.placeholder;
  input.setAttribute('aria-label', T.placeholder);
  sendBtn.textContent = T.send;
  fab.setAttribute('aria-label', T.open);
  var busy = false;

  function bubble(role, text, extra) {
    var el = document.createElement('div');
    el.className = 'msg ' + (role === 'user' ? 'me' : 'bot');
    if (role === 'user') el.textContent = text;
    else el.innerHTML = render(text);
    if (extra && extra.sources && extra.sources.length) {
      var s = document.createElement('div');
      s.className = 'src';
      s.appendChild(document.createTextNode(T.sources + ' '));
      extra.sources.slice(0, 2).forEach(function (src, i) {
        if (!safeUrl(src.url)) return;
        if (i) s.appendChild(document.createTextNode(' · '));
        var a = document.createElement('a');
        a.href = src.url; a.target = '_blank'; a.rel = 'noopener';
        a.textContent = String(src.title || src.url).split(' › ')[0].slice(0, 60);
        s.appendChild(a);
      });
      el.appendChild(s);
    }
    log.appendChild(el);
    if (extra && (extra.lead || extra.ticket)) {
      var t = document.createElement('div');
      t.className = 'tag';
      t.textContent = extra.lead ? T.lead : T.ticket;
      log.appendChild(t);
    }
  }

  function drawAll() {
    log.innerHTML = '';
    bubble('assistant', T.hello);
    state.messages.forEach(function (m) { bubble(m.role, m.content, m); });
    if (!state.messages.length) {
      var chips = document.createElement('div');
      chips.className = 'chips';
      T.chips.forEach(function (c) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'chip'; b.textContent = c;
        b.addEventListener('click', function () { ask(c); });
        chips.appendChild(b);
      });
      log.appendChild(chips);
    }
    log.scrollTop = log.scrollHeight;
  }

  function setOpen(open, focus) {
    state.open = open;
    panel.hidden = !open;
    fab.setAttribute('aria-expanded', String(open));
    save();
    if (open) { drawAll(); if (focus !== false) setTimeout(function () { input.focus(); }, 30); }
    else if (focus !== false) fab.focus();
  }

  function ask(text) {
    text = String(text || '').trim().slice(0, 1000);
    if (!text || busy) return;
    busy = true;
    sendBtn.disabled = true;
    var chips = root.querySelector('.chips');
    if (chips) chips.remove();
    var history = state.messages.map(function (m) { return { role: m.role, content: m.content }; });
    state.messages.push({ role: 'user', content: text });
    save();
    bubble('user', text);
    var typing = document.createElement('div');
    typing.className = 'typing';
    typing.innerHTML = '<i></i><i></i><i></i><span></span>';
    typing.querySelector('span').textContent = T.thinking;
    log.appendChild(typing);
    log.scrollTop = log.scrollHeight;

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, history: history, conversationId: state.conversationId, lang: LANG, page: location.pathname }),
    })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (data) {
        if (data.conversationId) state.conversationId = data.conversationId;
        var reply = data.reply || T.error;
        var msg = { role: 'assistant', content: reply, sources: data.sources || [], lead: !!data.lead, ticket: !!data.ticket };
        state.messages.push(msg);
        typing.remove();
        bubble('assistant', reply, msg);
      })
      .catch(function () {
        typing.remove();
        bubble('assistant', T.error);
      })
      .then(function () {
        busy = false;
        sendBtn.disabled = false;
        save();
        log.scrollTop = log.scrollHeight;
        input.focus();
      });
  }

  fab.addEventListener('click', function () { setOpen(!state.open); });
  $('.x').addEventListener('click', function () { setOpen(false); });
  $('.reset').addEventListener('click', function () {
    if (busy) return;
    state.messages = []; state.conversationId = null; save(); drawAll(); input.focus();
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value;
    input.value = '';
    input.style.height = '';
    ask(v);
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit')); }
  });
  input.addEventListener('input', function () { input.style.height = ''; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; });
  root.addEventListener('keydown', function (e) { if (e.key === 'Escape' && state.open) setOpen(false); });

  // Public hook so any button on the site can open the assistant: window.AgentDeck.open('question')
  window.AgentDeck = {
    open: function (q) { setOpen(true); if (q) ask(q); },
    close: function () { setOpen(false); },
  };

  if (state.open || script.getAttribute('data-open') === '1') setOpen(true, false);
})();
