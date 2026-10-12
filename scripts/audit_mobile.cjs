// Headless checks of local pages; does not control the user's browser.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(path.join(process.argv[2], 'playwright'));
const root = path.resolve(__dirname, '..');
function pagesIn(folder) {
  return fs.readdirSync(folder, {withFileTypes:true}).flatMap(entry => {
    if (['data','.git','node_modules'].includes(entry.name)) return [];
    const full = path.join(folder, entry.name);
    return entry.isDirectory() ? pagesIn(full) : entry.name.endsWith('.html') ? [path.relative(root,full).replaceAll('\\','/')] : [];
  });
}
(async () => {
  const browser = await chromium.launch({headless:true,channel:'chrome'});
  const page = await browser.newPage();
  // Third-party assets are unnecessary for testing the site's own layout.
  await page.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1' ? route.continue() : route.abort());
  const only = process.argv[4]?.split(',');
  const pages = pagesIn(root).sort().filter(file => !only || only.includes(file));
  const widths = (process.argv[3] || '390').split(',').map(Number);
  const results = [];
  for (const width of widths) {
    await page.setViewportSize({width,height:844});
    for (const file of pages) {
      try {
        const source = fs.readFileSync(path.join(root,file),'utf8');
        const refresh = source.match(/http-equiv=["']refresh["'][^>]*content=["'][^"']*url=([^"']+)/i);
        const url = new URL(refresh ? refresh[1].trim() : '', 'http://127.0.0.1:8765/'+file).href;
        await page.goto(url, {waitUntil:'load'});
        await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        const result = await page.evaluate(() => {
          const viewport = document.documentElement.clientWidth;
          const elements = [...document.querySelectorAll('body *')].filter(e => {
            const r=e.getBoundingClientRect();
            return r.width>0 && r.height>0 && getComputedStyle(e).visibility!=='hidden' && !e.closest('.site-floating-dialog,thead') && e.id!=='background';
          });
          const item = e => ({tag:e.tagName,cls:typeof e.className==='string'?e.className:'',id:e.id,width:Math.round(e.getBoundingClientRect().width),scroll:e.scrollWidth,text:e.textContent?.trim().slice(0,60)});
          const wide = elements.filter(e=>e.getBoundingClientRect().width>viewport+2).map(item);
          const inner = elements.filter(e=>e.clientWidth>0 && e.scrollWidth>e.clientWidth+3 && ['auto','scroll','hidden'].includes(getComputedStyle(e).overflowX)).map(item);
          return {viewport,scrollWidth:document.documentElement.scrollWidth,wide:wide.slice(0,10),inner:inner.slice(0,10),url:location.pathname};
        });
        results.push({file,width,...result});
      } catch(error) {results.push({file,width,error:String(error)});}
    }
    console.log(`Checked ${pages.length} pages at ${width}px`);
  }
  const reportPath=path.join(root,'data/mobile-audit-results.json');
  const previous=only ? JSON.parse(fs.readFileSync(reportPath,'utf8')) : null;
  const combined=previous ? previous.results.filter(r=>!results.some(n=>n.file===r.file&&n.width===r.width)).concat(results) : results;
  const failures = combined.filter(r=>r.error||r.scrollWidth>r.viewport+2||r.wide.length||r.inner.length);
  fs.writeFileSync(reportPath,JSON.stringify({pages:previous?.pages||pages.length,widths:previous?.widths||widths,checks:combined.length,failures,results:combined},null,2));
  console.log(JSON.stringify({checks:combined.length,failures:failures.length,examples:failures.slice(0,12)},null,2));
  await browser.close();
})();
