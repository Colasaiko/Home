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
      icon.setAttribute('aria-hidden','true'); icon.textContent = entry.icon || '◦';
      const text = document.createElement('span'); text.textContent = entry.label;
      inner.append(icon,text); bubble.replaceChildren(inner); menu.append(bubble);
      if (!entry.element) bubble.addEventListener('click', () => {
        if (entry.children) {levels.push({label:entry.label,entries:entry.children,page:0}); render(); close.focus({preventScroll:true});}
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
