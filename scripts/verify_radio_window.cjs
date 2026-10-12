const assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.argv[2]+'/playwright');
function wav(){const n=8000*60*2,b=Buffer.alloc(44+n);b.write('RIFF');b.writeUInt32LE(36+n,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(8000,24);b.writeUInt32LE(16000,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n,40);return b;}
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 for(const mode of ['http','file']){
 const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
 const errors=[];context.on('page',p=>p.on('pageerror',e=>errors.push(e.message)));
 await context.route('**/*',route=>{const u=new URL(route.request().url());if(u.hostname==='api.injahow.cn'&&process.argv[3]!=='live')return route.fulfill({contentType:'audio/wav',body:wav()});if(u.protocol==='file:'||u.hostname==='127.0.0.1'||(process.argv[3]==='live'&&route.request().resourceType()==='media'))return route.continue();return route.abort();});
 const page=await context.newPage();
 const base=mode==='http'?'http://127.0.0.1:8765/':pathToFileURL(process.cwd()+'/').href;
 await page.goto(base+'index.html');
 const wait=context.waitForEvent('page');await page.locator('#playBtn').click();const radio=await wait;
 await radio.waitForFunction(()=>window.siteRadio?.state().playing&&window.siteRadio.state().duration>0,null,{timeout:30000});
 await radio.evaluate(()=>window.originalAudio=document.querySelector('audio'));
 assert.equal(await radio.locator('option').count(),84);
 await page.locator('a[href="./topic/tuijianjichang/index.html"]').first().click();await page.waitForURL('**/topic/tuijianjichang/index.html');
 await page.locator('a[href="../../api.html"]').first().click();await page.waitForURL('**/api.html');
 await page.reload();
 await page.locator('.site-radio-toggle').click();
 assert.equal(context.pages().length,2,'reuse the same radio window');
 await radio.waitForFunction(()=>window.siteRadio.state().time>.5);
 const state=await radio.evaluate(()=>({playing:window.siteRadio.state().playing,time:window.siteRadio.state().time,sameAudio:originalAudio===document.querySelector('audio')}));
 assert.equal(state.playing,true);assert.equal(state.sameAudio,true);
 assert.equal(await page.locator('iframe[data-site-radio-frame]').count(),0);
 assert.equal(await page.locator('.site-radio-toggle').count(),1);
 await radio.locator('.site-radio-play').click();await radio.waitForFunction(()=>!window.siteRadio.state().playing);
 await radio.locator('.site-radio-play').click();await radio.waitForFunction(()=>window.siteRadio.state().playing);
 for(const width of [320,390,430]){await radio.setViewportSize({width,height:700});assert.equal(await radio.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);}
 assert.deepEqual(errors,[]);console.log(mode,JSON.stringify(state));
 await context.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
