(() => {
  const toc = document.querySelector('.protocol-toc');
  if (!toc) return;
  const details = toc.querySelector('details');
  const list = toc.querySelector('ul');
  const links = [...toc.querySelectorAll('a[href^="#"]')];
  const sections = links.map(link => document.getElementById(link.hash.slice(1)));
  const smallScreen = window.matchMedia('(max-width: 1000px)');
  // Keep the floating directory outside panels with backdrop-filter.
  document.body.append(toc);
  document.body.classList.add('protocol-reader');
  toc.classList.add('protocol-toc-follow');
  const hint = toc.querySelector('summary span');
  const chapter = hint.textContent.split(' · ')[0];
  const setLayout = () => {
    details.open = !smallScreen.matches;
    hint.textContent = `${chapter} · ${smallScreen.matches ? '点开选择章节' : '随阅读定位章节'}`;
  };
  setLayout();
  smallScreen.addEventListener('change', setLayout);
  let current = -1;
  let scheduled = false;
  function updateCurrent() {
    scheduled = false;
    let next = 0;
    sections.forEach((section, index) => {
      if (section && section.getBoundingClientRect().top <= 40) next = index;
    });
    if (next === current) return;
    if (current >= 0) links[current].removeAttribute('aria-current');
    current = next;
    const link = links[current];
    link.setAttribute('aria-current', 'location');
    if (details.open) {
      const itemBox = link.getBoundingClientRect();
      const listBox = list.getBoundingClientRect();
      if (itemBox.top < listBox.top || itemBox.bottom > listBox.bottom) {
        list.scrollTop += itemBox.top - listBox.top - list.clientHeight / 3;
      }
    }
  }
  window.addEventListener('scroll', () => {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(updateCurrent);
    }
  }, { passive: true });
  links.forEach(link => link.addEventListener('click', () => {
    if (smallScreen.matches) details.open = false;
  }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && smallScreen.matches && details.open) {
      details.open = false;
      toc.querySelector('summary').focus();
    }
  });
  document.querySelector('.protocol-back-toc')?.addEventListener('click', event => {
    event.preventDefault();
    details.open = true;
    toc.querySelector('summary').focus();
  });
  updateCurrent();
})();
