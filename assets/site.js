/* TeachersDeck Suite site scripts: floating cards, page-view counter, theme toggle */
/* Floating cards on scroll (skipped when the visitor prefers reduced motion) */
(function(){
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches&&!/[?&]motion=on/.test(location.search))return;
 var items=[].slice.call(document.querySelectorAll('main>.wrap.hero,main>section>.wrap,.cards>*,.flow li,.priv li')).filter(function(el){return !el.closest('[data-story],[data-pv]')});
 if(!items.length)return;
 document.documentElement.classList.add('fl-on');
 var boxN=0;
 var data=items.map(function(el){
  var sibs=[].slice.call(el.parentNode.children),i=sibs.indexOf(el);
  var box=el.matches('main>.wrap.hero,main>section>.wrap');
  if(box){boxN++;return{el:el,y:0,rise:160,speed:120,bob:30+(boxN%3)*3,ph:boxN*2.1};}
  return{el:el,y:0,rise:24+(i%4)*8,speed:6+(i%3)*5};
 });
 var vh=window.innerHeight,ticking=false;
 function clamp(v,a,b){return v<a?a:v>b?b:v}
 function frame(){
  ticking=false;
  var sy=window.pageYOffset,sc=window.innerWidth<700?0.6:1;
  for(var k=0;k<data.length;k++){
   var d=data[k],r=d.el.getBoundingClientRect(),top=r.top-d.y;
   if(top>vh*1.4||top+r.height<-vh*0.6){ // far off-screen: park it at its start/end state
    var parked=top>0?d.rise:0;
    if(d.y!==parked||top>0){d.el.style.transform=top>0?'translate3d(0,'+parked+'px,0)':'';d.el.style.opacity=top>0?0:'';d.y=parked}
    continue;
   }
   var t=clamp((vh*0.96-top)/(vh*0.38),0,1),e=1-Math.pow(1-t,3);
   var center=(top+r.height/2-vh/2)/vh;
   var y=(1-e)*d.rise+clamp(center,-1,1)*d.speed*sc+(d.bob?Math.sin(sy*0.005+d.ph)*d.bob*sc*e:0);
   d.y=y;
   d.el.style.transform='translate3d(0,'+y.toFixed(1)+'px,0)';
   d.el.style.opacity=e.toFixed(3);
  }
 }
 function req(){if(!ticking){ticking=true;requestAnimationFrame(frame)}}
 window.addEventListener('scroll',req,{passive:true});
 window.addEventListener('resize',function(){vh=window.innerHeight;req()});
 window.addEventListener('load',req);
 frame();
})();
(function(){
 var el=document.getElementById('hitcount');if(!el)return;
 /* The shown count merges GoatCounter's record (331 page views, 25-30 Oct 2026) with the visits Abacus counted after
    GoatCounter was switched off (Abacus 315 on 30 Oct, minus GoatCounter's 160 visits it overlapped = 155): 486 then,
    Abacus + 170 from here on (one less, for a test visit counted while checking this change). */
 var BASE=170;
 var counted=false;try{counted=sessionStorage.getItem('td_hit')==='1'}catch(e){}
 var tries=[
  {u:'https://abacus.jasoncameron.dev/'+(counted?'get':'hit')+'/teachersdeck-suite/visits',k:'value'}
 ];
 (function next(i){
  if(i>=tries.length){el.textContent='–';return}
  fetch(tries[i].u).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){
   var n=d&&d[tries[i].k];
   if(typeof n!=='number')throw 0;
   el.textContent=(n+BASE).toLocaleString('en-US');
   try{sessionStorage.setItem('td_hit','1')}catch(e){}
  }).catch(function(){next(i+1)});
 })(0);
})();
/* Light / dark theme: follows the device setting until the visitor picks one */
(function(){
 var root=document.documentElement,btn=document.querySelector('.theme'),meta=document.querySelector('meta[name="theme-color"]');
 function sync(){
  var dark=root.getAttribute('data-theme')==='dark';
  if(meta)meta.setAttribute('content',dark?'#0D1117':'#F3F5FC');
  if(btn){btn.setAttribute('aria-pressed',dark?'true':'false');btn.setAttribute('aria-label',dark?btn.dataset.light:btn.dataset.dark);btn.title=btn.getAttribute('aria-label')}
 }
 if(btn)btn.addEventListener('click',function(){
  var dark=root.getAttribute('data-theme')!=='dark';
  if(dark)root.setAttribute('data-theme','dark');else root.removeAttribute('data-theme');
  try{localStorage.setItem('td_theme',dark?'dark':'light')}catch(e){}
  sync();
 });
 var mq=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)');
 if(mq&&mq.addEventListener)mq.addEventListener('change',function(e){
  var saved=null;try{saved=localStorage.getItem('td_theme')}catch(x){}
  if(saved)return;
  if(e.matches)root.setAttribute('data-theme','dark');else root.removeAttribute('data-theme');
  sync();
 });
 sync();
})();
/* "Try the live demo": open the demo in its own window, like the demo page's Play button.
   If the browser blocks pop-ups, the link opens normally in a new tab. */
document.addEventListener('click',function(e){
 var a=e.target.closest&&e.target.closest('a[data-demo-window]');
 if(!a||e.metaKey||e.ctrlKey||e.shiftKey||e.button!==0)return;
 var w=Math.min(1440,screen.availWidth-40),h=Math.min(900,screen.availHeight-60);
 var win=window.open(a.href,'demo-'+a.getAttribute('data-demo-window'),'popup=yes,width='+w+',height='+h+',left='+Math.round((screen.availWidth-w)/2)+',top='+Math.round((screen.availHeight-h)/2));
 if(win){e.preventDefault();try{win.focus()}catch(x){}}
});
/* Live demo bento (home page): each app card's small window loads that app's real demo, scaled down.
   Desktop: hovering the card for a moment loads it; everywhere: the play button loads it. Clicking a
   loaded preview opens the full demo window. Nothing loads until asked, and never on Save-Data. */
(function(){
 var boxes=document.querySelectorAll('.live[data-src]'); if(!boxes.length)return;
 var vi=document.documentElement.lang==='vi', LOADING=vi?'Đang tải…':'Loading…';
 var hoverOK=window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches;
 var saveData=navigator.connection&&navigator.connection.saveData;
 function fit(box){var f=box.querySelector('iframe');if(!f)return;var w=box.querySelector('.live-view').clientWidth;f.style.transform='scale('+(w/1280)+')'}
 function load(box){
  if(box.classList.contains('on'))return; box.classList.add('on');
  var view=box.querySelector('.live-view'), btn=view.querySelector('.live-play');
  btn.querySelector('span').textContent=LOADING; btn.disabled=true;
  var f=document.createElement('iframe');
  f.src=box.getAttribute('data-src'); f.title=box.getAttribute('data-title'); f.tabIndex=-1; f.setAttribute('aria-hidden','true');
  f.width=1280; f.height=800; f.setAttribute('allow','autoplay \'none\'; microphone \'none\'; camera \'none\'');
  f.addEventListener('load',function(){box.classList.add('ready');setTimeout(function(){btn.remove()},300)});
  view.appendChild(f); fit(box);
  var open=document.createElement('a'); open.className='live-open'; open.href=box.getAttribute('data-src'); open.target='_blank'; open.rel='noopener';
  open.setAttribute('data-demo-window',box.getAttribute('data-live')); open.setAttribute('aria-label',box.querySelector('.live-bar a').textContent);
  view.appendChild(open);
 }
 var io=('IntersectionObserver' in window)&&!saveData?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);load(e.target)}})},{rootMargin:'200px 0px'}):null;
 boxes.forEach(function(box){
  box.querySelector('.live-play').addEventListener('click',function(){load(box)});
  if(io&&box.hasAttribute('data-autoload'))io.observe(box);
  if(hoverOK&&!saveData){var t,card=box.closest('.card,.tile')||box;
   card.addEventListener('mouseenter',function(){t=setTimeout(function(){load(box)},350)});
   card.addEventListener('mouseleave',function(){clearTimeout(t)});}
 });
 window.addEventListener('resize',function(){boxes.forEach(fit)});
})();
/* Phones: take the language pill and theme switch out of the bottom dock and put them in the header bar */
(function(){
 var bar=document.querySelector('header .bar'),dock=document.querySelector('.dk-in');
 if(!bar||!dock||!window.matchMedia)return;
 var lang=dock.querySelector('.lang'),theme=dock.querySelector('.theme'),mq=matchMedia('(max-width:760px)');
 if(!lang||!theme)return;
 function place(){
  if(mq.matches){bar.appendChild(lang);bar.appendChild(theme);document.documentElement.classList.add('dk-split')}
  else{dock.appendChild(lang);dock.appendChild(theme);document.documentElement.classList.remove('dk-split')}
 }
 place();
 if(mq.addEventListener)mq.addEventListener('change',place);else mq.addListener(place);
})();
/* "How they work together" scroll story: on wide screens the steps stay pinned while the section scrolls,
   and the screen on the right follows the active step. Phones and no-JS keep the plain cards. */
(function(){
 var sec=document.querySelector('#connect[data-story]'); if(!sec||!window.matchMedia)return;
 var track=sec.querySelector('.cs-track'), steps=[].slice.call(sec.querySelectorAll('.flow li')), bar=sec.querySelector('.cs-prog i');
 var mq=matchMedia('(min-width:900px)'), cur=-1, ticking=false;
 function setStep(i){ if(i===cur)return; cur=i; sec.setAttribute('data-step',i+1);
  steps.forEach(function(li,k){ if(k===i)li.setAttribute('aria-current','step'); else li.removeAttribute('aria-current'); }); }
 function update(){ ticking=false;
  if(!mq.matches){ sec.classList.remove('cs-on'); return; }
  sec.classList.add('cs-on');
  var r=track.getBoundingClientRect(), total=Math.max(1,track.offsetHeight-window.innerHeight*0.8), p=Math.min(1,Math.max(0,(-r.top+window.innerHeight*0.1)/total));
  setStep(Math.min(steps.length-1,Math.floor(p*steps.length))); if(bar)bar.style.height=(p*100).toFixed(1)+'%';
 }
 function req(){ if(!ticking){ticking=true;requestAnimationFrame(update)} }
 steps.forEach(function(li,k){ li.tabIndex=0;
  function go(){ if(!sec.classList.contains('cs-on'))return; var total=track.offsetHeight-window.innerHeight*0.8;
   var y=window.pageYOffset+track.getBoundingClientRect().top+window.innerHeight*0.1+total*(k+0.5)/steps.length; window.scrollTo({top:y,behavior:'smooth'}); }
  li.addEventListener('click',go); li.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){e.preventDefault();go()} });
 });
 setStep(0);
 window.addEventListener('scroll',req,{passive:true}); window.addEventListener('resize',req);
 if(mq.addEventListener)mq.addEventListener('change',req); update();
})();
/* "Built carefully" section: three variants, one picked at random by the inline script in the section (?pv=a|b|c forces one).
   a: promises tick in beside a shield that locks; b: "who sees what" role tabs; c: cards that flip to the full promise. */
(function(){
 var s=document.querySelector('#privacy[data-pv]'); if(!s)return;
 var v=s.getAttribute('data-pv'), still=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
 if((v==='a'||v==='c')&&!still&&'IntersectionObserver' in window){
  s.classList.add('pv-arm');
  var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ s.classList.add('pv-go'); io.disconnect(); } },{threshold:.3});
  io.observe(s.querySelector('.priv'));
 }
 if(v==='b'){
  var tabs=[].slice.call(s.querySelectorAll('.pv-roles [role=tab]'));
  function pick(t,focus){ tabs.forEach(function(x){ var on=x===t; x.setAttribute('aria-selected',on?'true':'false'); x.tabIndex=on?0:-1;
   document.getElementById(x.getAttribute('aria-controls')).hidden=!on; }); if(focus)t.focus(); }
  tabs.forEach(function(t,i){ t.addEventListener('click',function(){pick(t)});
   t.addEventListener('keydown',function(e){ var n=null,k=e.key;
    if(k==='ArrowRight'||k==='ArrowDown')n=tabs[(i+1)%tabs.length]; if(k==='ArrowLeft'||k==='ArrowUp')n=tabs[(i+tabs.length-1)%tabs.length];
    if(k==='Home')n=tabs[0]; if(k==='End')n=tabs[tabs.length-1]; if(n){e.preventDefault();pick(n,true)} }); });
 }
 if(v==='c'){
  [].slice.call(s.querySelectorAll('.priv li')).forEach(function(li){ li.tabIndex=0;
   li.addEventListener('click',function(){ li.classList.toggle('pv-flip'); });
   li.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); li.classList.toggle('pv-flip'); } }); });
 }
})();
/* Counts clicks on contact and demo links as Google Analytics events (window.tdTrack in analytics.js), for the HQ funnel.
   Only the kind of link is counted ("click-contact-zalo", "click-demo"…): no names, numbers or addresses. */
(function(){
 var rules=[[/^https?:\/\/(www\.)?zalo\.me\//i,'contact-zalo'],[/^mailto:/i,'contact-email'],[/^tel:/i,'contact-phone'],
  [/[?&]demo=1|\/demo\/?(\?|#|$)/i,'demo'],[/\/try\/?(\?|#|$)/i,'try'],[/\/order\/?(\?|#|$)/i,'order'],[/\/quote\/?(\?|#|$)/i,'quote'],
  [/^https?:\/\/chromewebstore\.google\.com\//i,'webstore']];
 document.addEventListener('click',function(e){
  var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(!a)return;
  var h=a.getAttribute('href')||'',abs=a.href||'';
  for(var i=0;i<rules.length;i++){
   if(rules[i][0].test(h)||rules[i][0].test(abs)){
    if(window.tdTrack)window.tdTrack(rules[i][1]);
    return;
   }
  }
 },true);
})();
