(() => {
 if(window.__siteRadioInitialized)return;window.__siteRadioInitialized=true;
 // Links point at folders (xxx/) for crawlers; a file:// preview has no server to serve index.html, so add it on click.
 const localIndex=value=>{const url=new URL(value,location.href);if(url.protocol==='file:'&&url.pathname.endsWith('/'))url.pathname+='index.html';return url.href;};
 if(location.protocol==='file:')window.addEventListener('click',event=>{const a=event.target.closest?.('a[href]');if(!a)return;const fixed=localIndex(a.href);if(fixed!==a.href)a.href=fixed;},true);
 const library=window.siteRadioLibrary||[],songs=library.flatMap(c=>c.songs.map(s=>({...s,category:c.name})));
 if(!songs.length)return;
 const format=seconds=>Number.isFinite(seconds)?`${Math.floor(seconds/60).toString().padStart(2,'0')}:${Math.floor(seconds%60).toString().padStart(2,'0')}`:'00:00';
 const homeURL=localIndex(new URL('../',document.querySelector('script[src*="js/site-radio.js"]').src).href);
 const embedded=window.parent!==window&&window.name==='__site_radio_content__';
 function connectLinks(controller){
 document.addEventListener('click',event=>{
  const a=event.target.closest?.('a[href]');
  if(!a||event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||a.hasAttribute('download'))return;
  const url=new URL(a.href);if(!['http:','https:','file:'].includes(url.protocol))return;
  if(url.origin!==location.origin){if(embedded&&a.target!=='_blank'){event.preventDefault();window.top.location.href=url.href;}return;}
  if(url.pathname===location.pathname&&url.search===location.search){if(!embedded)return;if(url.hash){return;}}
  if(!embedded&&!controller.active())return;
  if(a.target==='_blank')return;
  event.preventDefault();controller.navigate(url.href);
 },true);
 }
  function syncHome(doc, controller) {
    const state = controller.state();
    const setText = (id,text) => {const node=doc.getElementById(id);if(node) node.textContent=text;};
    setText('mTitle',state.song.title); setText('mArtist',state.song.artist);
    setText('currentTime',format(state.time));setText('totalDuration',format(state.duration));
    const progress=doc.getElementById('progressBar');
    if(progress && !doc.defaultView.isSeeking) progress.value=state.duration ? state.time / state.duration * 100 : 0;
    const volume=doc.getElementById('volSlider');if(volume) volume.value=state.volume * 100;
    const cover=doc.getElementById('recordCover');if(cover) cover.classList.toggle('paused',!state.playing);
    const play=doc.getElementById('playBtn');if(play) {play.textContent=state.playing?'❚❚':'▶';play.setAttribute('aria-label',state.playing?'暂停音乐':'播放音乐');}
    doc.querySelectorAll('[id^="song-"]').forEach(node => {
      const chosen=node.id===`song-${state.index}`;
      node.style.color=chosen?'#fff':'#ccc';node.style.fontWeight=chosen?'bold':'normal';node.style.borderLeft=chosen?'3px solid #9b59b6':'none';
    });
    doc.defaultView.currentMusicIdx=state.index;
  }
  function bridgeHome(controller, targetWindow=window) {
    const doc=targetWindow.document;
    const oldAudio=doc.getElementById('h5Player');
    if(oldAudio){oldAudio.pause();oldAudio.removeAttribute('src');oldAudio.load();}
    targetWindow.toggleMusic=()=>controller.toggle();
    targetWindow.playSongFromList=index=>controller.select(index);
    targetWindow.nextMusic=()=>controller.next();targetWindow.prevMusic=()=>controller.previous();
    targetWindow.setVolume=value=>controller.volume(Number(value)/100);
    targetWindow.commitSeek=value=>{controller.seek(Number(value)/100);targetWindow.isSeeking=false;};
    targetWindow.updateSeekTime=value=>{const node=doc.getElementById('currentTime');if(node)node.textContent=format(Number(value)/100*controller.state().duration);};
    syncHome(doc,controller);
  }


 if(embedded){
  document.documentElement.dataset.siteRadioEmbedded='true';
  let state={index:0,song:songs[0],playing:false,time:0,duration:0,volume:.7};
  const send=(command,value)=>window.parent.postMessage({channel:'site-radio-v3',command,value},'*');
  const controller={state:()=>state,toggle:()=>send('toggle'),select:value=>send('select',value),next:()=>send('next'),previous:()=>send('previous'),volume:value=>send('volume',value),seek:value=>send('seek',value),navigate:value=>send('navigate',value),collapse:()=>send('collapse')};
  window.siteRadio=controller;window.siteRadioGoBack=()=>send('back');
  window.addEventListener('message',event=>{if(event.source!==window.parent||event.data?.channel!=='site-radio-v3'||!event.data.state)return;state=event.data.state;syncHome(document,controller);});
  document.addEventListener('DOMContentLoaded',()=>queueMicrotask(()=>{document.body.classList.add('site-radio-ready');bridgeHome(controller);connectLinks(controller);send('ready',location.href);}));
  window.addEventListener('hashchange',()=>send('address',location.href));
  return;
 }
 document.addEventListener('DOMContentLoaded',()=>queueMicrotask(()=>{
 document.body.classList.add('site-radio-ready');
    const audio=document.createElement('audio');audio.id='site-radio-audio';audio.preload='none';
    const widget=document.createElement('aside');widget.className='site-radio';widget.setAttribute('aria-label','私人音乐电台');
    widget.innerHTML=`<button class="site-radio-toggle" aria-label="打开音乐电台" aria-expanded="false" aria-controls="site-radio-panel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 14v-3a9 9 0 0 1 18 0v3"/><rect x="2" y="12" width="5" height="9" rx="2"/><rect x="17" y="12" width="5" height="9" rx="2"/></svg></button>
      <section class="site-radio-panel" id="site-radio-panel" aria-label="音乐播放面板" hidden>
      <div class="site-radio-heading"><h2>私人音乐电台</h2><button class="site-radio-close" aria-label="收起音乐电台">收起</button></div>
      <p class="site-radio-title"></p><p class="site-radio-artist"></p>
      <div class="site-radio-controls"><button data-radio-previous aria-label="上一首">◀</button><button class="site-radio-play" aria-label="播放音乐">▶</button><button data-radio-next aria-label="下一首">▶▶</button></div>
      <label class="site-radio-field" for="site-radio-seek">播放进度</label><input id="site-radio-seek" type="range" min="0" max="100" value="0" step="0.1" disabled><div class="site-radio-time"><span data-radio-time>00:00</span><span data-radio-duration>00:00</span></div>
      <label class="site-radio-field" for="site-radio-volume">音量</label><input id="site-radio-volume" type="range" min="0" max="100" value="70">
      <label class="site-radio-field" for="site-radio-song">选择歌曲 · ${songs.length} 首</label><select id="site-radio-song"></select>
      <p class="site-radio-status" role="status" hidden></p><p class="site-radio-note">收起面板后音乐继续播放，可以浏览站内页面。</p></section>`;
    widget.append(audio);document.body.append(widget);
    const toggle=widget.querySelector('.site-radio-toggle'),panel=widget.querySelector('.site-radio-panel'),play=widget.querySelector('.site-radio-play'),seek=widget.querySelector('#site-radio-seek'),volume=widget.querySelector('#site-radio-volume'),select=widget.querySelector('select'),status=widget.querySelector('.site-radio-status');
    let index=0,seeking=false,frame=null;
    try{const saved=Number(localStorage.getItem('site-radio-volume'));if(localStorage.getItem('site-radio-volume')!==null&&saved>=0&&saved<=1)audio.volume=saved;else audio.volume=.7;}catch(_){audio.volume=.7;}
    let songIndex=0;
    library.forEach(category=>{
      const group=document.createElement('optgroup');group.label=category.name;
      category.songs.forEach(song=>{const option=document.createElement('option');option.value=songIndex++;option.textContent=`${song.name} · ${song.artist}`;group.append(option);});select.append(group);
    });
    function setOpen(open){panel.hidden=!open;toggle.setAttribute('aria-expanded',String(open));}
    function showError(){status.textContent='这首歌暂时无法播放，请换一首或稍后重试。';status.hidden=false;render();}
    function render(){
      const state=controller.state();
      widget.classList.toggle('is-playing',state.playing);

      widget.querySelector('.site-radio-title').textContent=state.song.title;
      widget.querySelector('.site-radio-artist').textContent=state.song.artist;
      play.textContent=state.playing?'❚❚':'▶';play.setAttribute('aria-label',state.playing?'暂停音乐':'播放音乐');
      widget.querySelector('[data-radio-time]').textContent=format(state.time);widget.querySelector('[data-radio-duration]').textContent=format(state.duration);
      seek.disabled=!state.duration;if(!seeking)seek.value=state.duration?state.time/state.duration*100:0;
      volume.value=state.volume*100;select.value=index;
      syncHome(document,controller);
      if(frame)frame.contentWindow.postMessage({channel:'site-radio-v3',state},'*');
    }
    async function start(){
      status.hidden=true;
      if(!audio.getAttribute('src'))audio.src=songs[index].url;
      try{activateShell();await audio.play();widget.hidden=false;render();}catch(error){if(error.name==='NotAllowedError'){status.textContent='浏览器需要你在电台窗口按一次播放按钮。';status.hidden=false;render();}else if(error.name!=='AbortError')showError();}
    }
    const controller={
      state:()=>({index,song:songs[index],playing:!audio.paused&&!audio.error,time:audio.currentTime||0,duration:Number.isFinite(audio.duration)?audio.duration:0,volume:audio.volume}),
      toggle:()=>audio.paused?start():(audio.pause(),render()),
      select:value=>{const next=Number(value);if(!Number.isInteger(next)||next<0||next>=songs.length)return;index=next;audio.src=songs[index].url;start();},
      next:()=>controller.select((index+1)%songs.length),previous:()=>controller.select((index-1+songs.length)%songs.length),
      volume:value=>{audio.volume=Math.min(1,Math.max(0,value));try{localStorage.setItem('site-radio-volume',String(audio.volume));}catch(_){}render();},
      seek:value=>{if(Number.isFinite(audio.duration))audio.currentTime=Math.min(1,Math.max(0,value))*audio.duration;render();},
      collapse:()=>setOpen(false),navigate,back:()=>history.length>1?history.back():navigate(homeURL)
    };
    play.addEventListener('click',()=>controller.toggle());widget.querySelector('[data-radio-previous]').addEventListener('click',()=>controller.previous());widget.querySelector('[data-radio-next]').addEventListener('click',()=>controller.next());
    select.addEventListener('change',()=>controller.select(select.value));volume.addEventListener('input',()=>controller.volume(Number(volume.value)/100));
    seek.addEventListener('input',()=>{seeking=true;widget.querySelector('[data-radio-time]').textContent=format(Number(seek.value)/100*audio.duration);});
    seek.addEventListener('change',()=>{seeking=false;controller.seek(Number(seek.value)/100);});

    ['play','pause','timeupdate','loadedmetadata','durationchange','volumechange'].forEach(event=>audio.addEventListener(event,render));
    audio.addEventListener('error',showError);audio.addEventListener('ended',()=>controller.next());


 function navigate(value,push=true){
  const url=new URL(localIndex(value));if(url.origin!==location.origin)return;
  if(!frame)activateShell();
  if(push&&url.href!==location.href){try{history.pushState({siteRadio:true},'',url.href);}catch(_){}}
  frame.src=url.href;
 }
 function activateShell(){
  if(frame)return;
  const url=location.href,scroll=window.scrollY;
  if(!document.querySelector('base[href]')){const base=document.createElement('base');base.href=url;document.head.prepend(base);}
  const original=document.createElement('div');original.id='site-radio-original';
  [...document.body.childNodes].filter(node=>node!==widget).forEach(node=>original.append(node));document.body.prepend(original);
  frame=document.createElement('iframe');frame.name='__site_radio_content__';frame.className='site-radio-frame-view';frame.title='网站内容';frame.setAttribute('data-site-radio-frame','');frame.setAttribute('allow','autoplay; fullscreen');frame.style.visibility='hidden';frame.src=url;document.body.append(frame);
  function ready(value){
   try{if(value!==frame.contentWindow.location.href)return;}catch(_){if(value!==frame.src)return;}
   if(original.isConnected){
    try{if(value===url){frame.contentWindow.scrollTo(0,scroll);const bg=original.querySelector('#background'),next=frame.contentDocument.getElementById('background');if(bg&&next){next.style.transition='none';next.style.backgroundImage=getComputedStyle(bg).backgroundImage;}}}catch(_){}
    try{if(value===url){const doc=frame.contentDocument;original.querySelectorAll('input,textarea,select').forEach(field=>{const next=field.id&&doc.getElementById(field.id);if(!next||field.type==='file')return;next.value=field.value;if('checked' in next)next.checked=field.checked;});}}catch(_){}
    document.body.classList.add('site-radio-shell');frame.style.visibility='visible';original.remove();
   }
   try{if(value)history.replaceState({siteRadio:true},'',value);}catch(_){}
   try{document.title=frame.contentDocument.title;}catch(_){}
   render();
  }
  window.addEventListener('message',event=>{
   if(event.source!==frame.contentWindow||event.data?.channel!=='site-radio-v3')return;
   const {command,value}=event.data;
   if(command==='ready'){ready(value);return;}
   if(command==='address'){try{history.replaceState({siteRadio:true},'',value);}catch(_){}return;}
   const actions={toggle:()=>controller.toggle(),select:()=>controller.select(value),next:()=>controller.next(),previous:()=>controller.previous(),volume:()=>controller.volume(Number(value)),seek:()=>controller.seek(Number(value)),navigate:()=>navigate(value),collapse:()=>controller.collapse(),back:()=>controller.back()};
   if(Object.hasOwn(actions,command))actions[command]();
  });
  window.addEventListener('popstate',()=>navigate(location.href,false));
 }
 window.siteRadio=controller;window.siteRadioGoBack=()=>controller.back();controller.active=()=>!!frame;
 connectLinks(controller);
 toggle.addEventListener('click',()=>{setOpen(panel.hidden);});
 widget.querySelector('.site-radio-close').addEventListener('click',()=>setOpen(false));
 widget.hidden=!!document.getElementById('playBtn');
 bridgeHome(controller);render();
 }));
})();
