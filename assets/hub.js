/* Get the apps (/apps/): counts that the page was opened and which app a visitor picked, for the HQ funnel.
   Only the app, the way in (web, store, zip, demo…) and the device group (phone, tablet, computer) are sent:
   nothing personal. The device group itself is set by the inline script at the top of <main>. */
(function(){
 var root=document.documentElement,group=root.getAttribute('data-dev-group')||'computer';
 function send(name,params){if(window.tdEvent)window.tdEvent(name,params)}
 send('view_apps',{device:group});
 document.addEventListener('click',function(e){
  var a=e.target&&e.target.closest?e.target.closest('.ga-row a[data-way]'):null;if(!a)return;
  send('pick_app',{app:a.closest('.ga-row').getAttribute('data-app'),way:a.getAttribute('data-way'),device:group});
 });
 /* /apps/#parentdeck: open that app's other ways, and the install step a link points to */
 function open(){
  var el=location.hash&&document.getElementById(location.hash.slice(1));if(!el)return;
  var d=el.matches('details')?el:el.querySelector('details');if(d)d.open=true;
 }
 window.addEventListener('hashchange',open);open();
})();
