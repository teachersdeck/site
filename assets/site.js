/* TeachersDeck Suite site scripts: floating cards, page-view counter, theme toggle */
/* Floating cards on scroll (skipped when the visitor prefers reduced motion) */
(function(){
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches&&!/[?&]motion=on/.test(location.search))return;
 var items=[].slice.call(document.querySelectorAll('main>.wrap.hero,main>section>.wrap,.cards>*,.flow li,.priv li'));
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
 var counted=false;try{counted=sessionStorage.getItem('td_hit')==='1'}catch(e){}
 var tries=[
  {u:'https://abacus.jasoncameron.dev/'+(counted?'get':'hit')+'/teachersdeck-suite/visits',k:'value'}
 ];
 (function next(i){
  if(i>=tries.length){el.textContent='–';return}
  fetch(tries[i].u).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){
   var n=d&&d[tries[i].k];
   if(typeof n!=='number')throw 0;
   el.textContent=n.toLocaleString('en-US');
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
