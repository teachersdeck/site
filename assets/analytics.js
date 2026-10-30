/* Site analytics: Cloudflare Web Analytics (cookieless) + standard Google Analytics 4.
   Replaces GoatCounter (2026-10-30). Disclosed in /student-privacy/ ("Website analytics").
   IDs: GA4 property 561096420 (stream "TeachersDeck apps"), Cloudflare Web Analytics site myteachersdeck.com (teachersdeck@gmail.com). */
(function(){
 var CF_TOKEN='a14b03f707e24d71968e3a60a96a3608';   // Cloudflare dashboard → Web Analytics → myteachersdeck.com → JS snippet "token"
 var GA_ID='G-M8LJNJ2D3P';                 // GA4 → Admin → Data streams → Measurement ID

 if(CF_TOKEN.indexOf('CLOUDFLARE')!==0){
  var cf=document.createElement('script');cf.defer=true;cf.src='https://static.cloudflareinsights.com/beacon.min.js';
  cf.setAttribute('data-cf-beacon',JSON.stringify({token:CF_TOKEN}));document.head.appendChild(cf);
 }

 window.dataLayer=window.dataLayer||[];
 window.gtag=window.gtag||function(){dataLayer.push(arguments)};
 if(GA_ID.indexOf('G-XXXX')!==0){
  var ga=document.createElement('script');ga.async=true;ga.src='https://www.googletagmanager.com/gtag/js?id='+GA_ID;document.head.appendChild(ga);
  gtag('js',new Date());
  gtag('config',GA_ID,{allow_google_signals:false,allow_ad_personalization_signals:false});
 }

 /* Tracked link clicks (site.js calls this): only the kind of link, never names, numbers or addresses */
 window.tdTrack=function(kind){ try{gtag('event','click_'+kind.replace(/-/g,'_'),{link_kind:kind})}catch(_){} };
})();
