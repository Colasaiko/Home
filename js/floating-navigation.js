(() => {
  const nav = document.querySelector('.site-floating-nav');
  if (!nav || nav.dataset.initialized) return;
  nav.dataset.initialized = 'true';
  const fab = nav.querySelector('[data-floating-toggle]');
  const menu = nav.querySelector('.site-floating-menu');
  const back = nav.querySelector('[data-floating-back]');
  const home = nav.querySelector('.site-floating-controls a');
  const dialog = document.createElement('dialog');
  dialog.className = 'site-floating-dialog';
  dialog.id = 'site-floating-dialog';
  dialog.setAttribute('aria-labelledby', 'site-floating-dialog-title');
  const heading = menu.querySelector('.site-floating-title');
  heading.id = 'site-floating-dialog-title';
  heading.textContent = '想去哪里？';
  const close = document.createElement('button');
  close.type = 'button'; close.className = 'site-floating-close';
  close.setAttribute('aria-label', '关闭快捷导航');
  close.innerHTML = '<span aria-hidden="true">✦</span><span>收起</span>';
  const hint = document.createElement('p');
  hint.className = 'site-floating-hint';
  hint.textContent = '点泡泡前往';
  const shortcuts = document.createElement('div');
  shortcuts.className = 'site-floating-shortcuts';
  back.append(document.createTextNode('返回上一页'));
  home.append(document.createTextNode('返回首页'));
  shortcuts.append(back, home);
  menu.querySelector('a').remove();
  heading.after(hint, shortcuts); menu.prepend(close);
  menu.querySelectorAll(':scope > a').forEach(link => link.remove());
  shortcuts.remove();
  const siteRoot = new URL('.', home.href);
  const iconPaths = {
    back: '<path d="m12 5-7 7 7 7M5 12h15"/>',
    home: '<path d="m3 10 9-7 9 7M5 9v12h5v-7h4v7h5V9"/>',
    tags: '<path d="M3 3h7l11 11-7 7L3 10Z"/><circle cx="7.5" cy="7.5" r="1"/>',
    star: '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3l-5.6 2.9 1.1-6.2L3 9.6l6.2-.9Z"/>',
    grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    compare: '<path d="M4 7h16m-4-4 4 4-4 4M20 17H4m4-4-4 4 4 4"/>',
    book: '<path d="M12 5C8 2 3 3 3 3v17s5-1 9 2c4-3 9-2 9-2V3s-5-1-9 2Zm0 0v17"/>',
    tools: '<path d="m14 7 3 3 4-4a6 6 0 0 1-8 8L6 21a2 2 0 0 1-3-3l7-7a6 6 0 0 1 8-8Z"/>',
    download: '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
    settings: '<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="10" cy="18" r="2"/>',
    code: '<path d="m8 5-6 7 6 7m8-14 6 7-6 7m-3-17-2 20"/>',
    activity: '<path d="M2 12h5l3-8 4 16 3-8h5"/>',
    shield: '<path d="m12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6Z"/><path d="m8 12 3 3 5-6"/>',
    lock: '<rect x="4" y="10" width="16" height="12" rx="2"/><path d="M7 10V7a5 5 0 0 1 10 0v3m-5 5v3"/>',
    globe: '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6h14M5 18h14"/>',
    network: '<rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M12 8v5M5 16v-3h14v3"/>',
    chip: '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9" y="9" width="6" height="6" rx="1"/><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4"/>',
    chat: '<path d="M21 14a3 3 0 0 1-3 3H8l-5 4V6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3Z"/><path d="M7 8h10M7 12h6"/>',
    image: '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="2"/><path d="m3 17 6-6 4 4 3-3 5 5"/>',
    bookmark: '<path d="M6 3h12v19l-6-4-6 4Z"/>',
    news: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 7h10M7 11h4m-4 4h4m4-4h2m-2 4h2M7 18h10"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9 8a3 3 0 0 1 6 0c0 2-3 2-3 5m0 3h.01"/>',
    document: '<path d="M14 2H5v20h14V7Zm0 0v5h5M8 11h8m-8 4h8m-8 4h5"/>',
    cloud: '<path d="M6 19a5 5 0 1 1 0-10 7 7 0 0 1 13-1 5.5 5.5 0 0 1-1 11Z"/>',
    wind: '<path d="M3 7h12a3 3 0 1 0-3-3M2 12h17a3 3 0 1 1-3 3M4 17h6a3 3 0 1 1-3 3"/>',
    cat: '<path d="m4 10 1-7 5 4h4l5-4 1 7v5c0 8-16 8-16 0Z"/><path d="M8 13h.01M16 13h.01m-6 4 2 1 2-1M1 15l5 1m12 0 5-1"/>',
    sunset: '<path d="M2 17h20M5 21h14M7 17a5 5 0 0 1 10 0M12 2v4M3 7l3 3m15-3-3 3"/>',
    crown: '<path d="m3 5 5 5 4-7 4 7 5-5-2 14H5Zm2 17h14"/>',
    firefly: '<ellipse cx="12" cy="14" rx="4" ry="7"/><path d="M9 8 6 5m9 3 3-3M8 11l-5-2m13 2 5-2M8 16l-5 2m13-2 5 2M9 16h6"/>',
    bolt: '<path d="m14 2-10 12h7l-1 8 10-12h-7Z"/>',
    next: '<path d="m9 4 8 8-8 8"/>',
    previous: '<path d="m15 4-8 8 8 8"/>'
  };
  const labelIcons = {
    '返回上一页':'back','返回首页':'home','前一组':'previous','后一组':'next',
    '品牌与选购':'tags','主推品牌':'star','品牌总库':'grid','全部品牌':'grid','品牌对比':'compare','选购指南':'book',
    '套餐与资料':'document','实测与追踪':'activity','优惠详情':'tags',
    '客户端工具':'tools','客户端下载':'download','配置与隐私':'settings','IP 与编码':'code','连通性检查':'activity',
    '网络与隐私':'shield','网络研究':'globe','隐私检查':'lock','GFW 排查':'activity','协议总览':'network','协议文章':'book',
    'Shadowsocks':'shield','Trojan':'lock','VLESS / XTLS':'code','VLESS Reality':'shield','IPLC / IEPL':'network','Hysteria / TUIC':'bolt','SNI 与 TLS':'lock','机场审计':'document','DNS 与 DoH':'globe','中转与直连':'network',
    'AI 指南':'chip','AI 入门':'chip','提问方法':'chat','ChatGPT':'chat','Claude':'chat','图片生成':'image','API 部署':'code',
    '专题与资源':'grid','主题目录':'grid','资源书签':'bookmark','资讯来源':'news','FAQ 总入口':'help'
  };
  const brandIcons = {weifeng:'wind',feimao:'cat',muguang:'sunset',dalao:'crown',firefly:'firefly',lingmao:'cat',shanyue:'bolt',wuyou:'shield',kuajie:'globe'};
  const categoryTones = {'品牌与选购':'brands','客户端工具':'tools','网络与隐私':'security','AI 指南':'ai','专题与资源':'resources','FAQ 总入口':'faq'};
  function makeIcon(entry) {
    const slug = entry.children?.[0]?.path?.match(/brands\/([^/]+)\//)?.[1];
    const name = labelIcons[entry.label] || brandIcons[slug] || (entry.children ? 'cloud' : 'document');
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox','0 0 24 24');
    svg.setAttribute('fill','none'); svg.setAttribute('stroke','currentColor');
    svg.setAttribute('stroke-width','1.7'); svg.setAttribute('stroke-linecap','round'); svg.setAttribute('stroke-linejoin','round');
    svg.innerHTML = iconPaths[name];
    return svg;
  }
  const parent = document.createElement('button');
  parent.type = 'button'; parent.className = 'site-floating-parent';
  parent.textContent = '← 上一圈'; parent.hidden = true;
  menu.append(parent);
  const rootEntries = [{label:'返回上一页',icon:'←',element:back}, {label:'返回首页',icon:'⌂',element:home}, ...(window.siteFloatingPages || [])];
  const levels = [{label:'想去哪里？',entries:rootEntries,page:0}];
  function render() {
    menu.querySelectorAll('.site-floating-bubble').forEach(bubble => bubble.remove());
    const level = levels[levels.length - 1];
    const paginated = level.entries.length > 8;
    const pageSize = paginated ? 6 : 8;
    const pages = Math.ceil(level.entries.length / pageSize);
    const entries = level.entries.slice(level.page * pageSize, (level.page + 1) * pageSize);
    if (paginated) {
      entries.push({label:'前一组',icon:'‹',action:() => {level.page = (level.page - 1 + pages) % pages; render();}});
      entries.push({label:'后一组',icon:'›',action:() => {level.page = (level.page + 1) % pages; render();}});
    }
    heading.textContent = level.label + (paginated ? ` · ${level.page + 1}/${pages}` : '');
    hint.textContent = levels.length === 1 ? '点分类展开' : '点泡泡选择';
    parent.hidden = levels.length === 1;
    entries.forEach((entry, index) => {
      const bubble = entry.element || document.createElement(entry.path ? 'a' : 'button');
      if (bubble.tagName === 'BUTTON') bubble.type = 'button';
      if (entry.path) bubble.href = new URL(entry.path, siteRoot).href;
      bubble.setAttribute('aria-label', entry.label);
      bubble.title = entry.title || entry.label;
      if (entry.children) {bubble.setAttribute('aria-expanded','false'); bubble.setAttribute('aria-label', entry.label + '，展开分类');}
      bubble.className = 'site-floating-bubble';
      const angle = (index * 360 / entries.length - 90) * Math.PI / 180;
      bubble.style.setProperty('--dx',Math.cos(angle).toFixed(4));
      bubble.style.setProperty('--dy',Math.sin(angle).toFixed(4));
      bubble.style.setProperty('--delay',`${index * 30}ms`);
      bubble.style.setProperty('--float-delay',`${-index * .45}s`);
      const inner = document.createElement('span'); inner.className = 'site-floating-bubble-inner';
      const icon = document.createElement('span'); icon.className = 'site-floating-bubble-icon';
      icon.setAttribute('aria-hidden','true'); icon.append(makeIcon(entry));
      bubble.dataset.tone = categoryTones[entry.label] || level.tone || 'navigation';
      const text = document.createElement('span'); text.textContent = /^FireFly 萤火虫$/i.test(entry.label) ? 'Firefly' : entry.label;
      inner.append(icon,text); bubble.replaceChildren(inner); menu.append(bubble);
      if (!entry.element) bubble.addEventListener('click', () => {
        if (entry.children) {levels.push({label:entry.label,entries:entry.children,page:0,tone:categoryTones[entry.label] || level.tone}); render(); close.focus({preventScroll:true});}
        else if (entry.action) {entry.action(); close.focus({preventScroll:true});}
      });
    });
  }
  parent.addEventListener('click', () => {levels.pop(); render(); parent.hidden ? close.focus({preventScroll:true}) : parent.focus({preventScroll:true});});
  render();
  menu.hidden = false; dialog.append(menu); nav.append(dialog);
  const label = document.createElement('span'); label.textContent = '导航'; fab.append(label);
  fab.setAttribute('aria-controls', dialog.id); fab.setAttribute('aria-haspopup', 'dialog');
  fab.title = '点击快速导航，拖动调整位置';
  let previousPage = '';
  try {
    const current = location.origin + location.pathname;
    const last = sessionStorage.getItem('site-floating-last-page');
    if (last && last !== current) sessionStorage.setItem('site-floating-previous-page', last);
    previousPage = sessionStorage.getItem('site-floating-previous-page') || '';
    sessionStorage.setItem('site-floating-last-page', current);
  } catch (_) {}
  let savedStyle, savedY = 0;
  function unlock() {
    if (!savedStyle) return;
    document.body.style.cssText = savedStyle.body;
    document.documentElement.style.overflow = savedStyle.overflow;
    savedStyle = null;
    window.scrollTo({top: savedY, left: 0, behavior: 'instant'});
    fab.setAttribute('aria-expanded', 'false'); fab.focus({preventScroll: true});
  }
  function open() {
    if (dialog.open) return;
    window.siteRadio?.collapse?.();
    savedY = window.scrollY;
    savedStyle = {body: document.body.style.cssText, overflow: document.documentElement.style.overflow};
    const gutter = innerWidth - document.documentElement.clientWidth;
    const padding = parseFloat(getComputedStyle(document.body).paddingRight) || 0;
    Object.assign(document.body.style, {position: 'fixed', top: `${-savedY}px`, width: '100%', overflow: 'hidden', boxSizing: 'border-box', paddingRight: `${padding + gutter}px`});
    document.documentElement.style.overflow = 'hidden';
    dialog.showModal(); fab.setAttribute('aria-expanded', 'true'); close.focus({preventScroll: true});
  }
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', unlock);
  dialog.addEventListener('click', event => {
    if (event.target === dialog || event.target === menu) dialog.close();
  });
  dialog.addEventListener('click', event => { if (event.target.closest('a')) { dialog.close(); unlock(); } });
  back.addEventListener('click', () => {
    dialog.close(); unlock();
    if (window.siteRadioGoBack) { window.siteRadioGoBack(); return; }
    if (history.length > 1 && (previousPage || document.referrer)) history.back();
    else location.assign(back.dataset.home);
  });
  let drag, dragged = false;
  function position(x, y) {
    const left = Math.max(12, Math.min(x, innerWidth - fab.offsetWidth - 12));
    const top = Math.max(12, Math.min(y, innerHeight - fab.offsetHeight - 12));
    Object.assign(nav.style, {left: `${left}px`, top: `${top}px`, right: 'auto', bottom: 'auto'});
    return {x: left / innerWidth, y: top / innerHeight};
  }
  try {
    const stored = JSON.parse(localStorage.getItem('site-floating-position'));
    if (stored && Number.isFinite(stored.x) && Number.isFinite(stored.y)) position(stored.x * innerWidth, stored.y * innerHeight);
  } catch (_) {}
  fab.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    dragged = false;
    const rect = fab.getBoundingClientRect();
    drag = {id: event.pointerId, x: event.clientX, y: event.clientY, left: rect.left, top: rect.top};
    fab.setPointerCapture(event.pointerId);
  });
  fab.addEventListener('pointermove', event => {
    if (!drag || event.pointerId !== drag.id) return;
    const dx = event.clientX - drag.x, dy = event.clientY - drag.y;
    if (Math.hypot(dx, dy) > 6) dragged = true;
    if (dragged) { nav.classList.add('is-dragging'); position(drag.left + dx, drag.top + dy); }
  });
  function endDrag(event) {
    if (!drag || event.pointerId !== drag.id) return;
    if (dragged) {
      const rect = fab.getBoundingClientRect();
      try { localStorage.setItem('site-floating-position', JSON.stringify(position(rect.left, rect.top))); } catch (_) {}
    }
    drag = null; nav.classList.remove('is-dragging');
  }
  fab.addEventListener('pointerup', endDrag); fab.addEventListener('pointercancel', endDrag);
  fab.addEventListener('click', event => {
    if (dragged && event.detail !== 0) { dragged = false; return; }
    open();
  });
  window.addEventListener('resize', () => {
    if (!nav.style.left) return;
    const rect = fab.getBoundingClientRect(); position(rect.left, rect.top);
  });
  window.addEventListener('pageshow', () => { if (dialog.open) dialog.close(); unlock(); });
})();
