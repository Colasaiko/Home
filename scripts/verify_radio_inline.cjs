const assert=require('node:assert/strict');const{pathToFileURL}=require('node:url');const{chromium}=require(process.argv[2]+'/playwright');
(async()=>{const browser=await chromium.launch({channel:'chrome',headless:true});for(const mode of ['http','file']){
 const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});const errors=[];context.on('page',p=>p.on('pageerror',e=>errors.push(e.message)));
 await context.route('**/*',route=>{const u=new URL(route.request().url());if(u.protocol==='file:'||u.hostname==='127.0.0.1'||route.request().resourceType()==='media')return route.continue();return route.abort();});
 const page=await context.newPage();const base=mode==='http'?'http://127.0.0.1:8765/':pathToFileURL(process.cwd()+'/').href;
 await page.goto(base+'index.html');assert.equal(await page.locator('.site-radio-toggle').isVisible(),false);
 await page.locator('#playBtn').click();await page.waitForFunction(()=>window.siteRadio?.state().playing&&window.siteRadio.state().duration>0,null,{timeout:30000});
 await page.waitForFunction(()=>!document.getElementById('site-radio-original'));await page.evaluate(()=>window.originalAudio=document.querySelector('#site-radio-audio'));
 assert.equal(await page.locator('.site-radio-toggle').count(),1);assert.equal(await page.frameLocator('iframe').locator('.site-radio-toggle').count(),0);
 const content=()=>page.frameLocator('iframe[data-site-radio-frame]');
 await content().locator('a[href="./topic/tuijianjichang/index.html"]').first().click();await content().locator('a[href="../../api.html"]').first().waitFor();
 await content().locator('a[href="../../api.html"]').first().click();await content().locator('a[href="topic/cybersecurity/privacy.html"]').first().waitFor();
 await content().locator('a[href="topic/cybersecurity/privacy.html"]').first().click();await content().locator('#privacy-record').waitFor();
 const result=await page.evaluate(()=>({playing:window.siteRadio.state().playing,sameAudio:originalAudio===document.querySelector('#site-radio-audio'),time:window.siteRadio.state().time}));assert(result.playing&&result.sameAudio);
 await page.locator('.site-radio-toggle').click();assert.equal(await page.locator('#site-radio-song option').count(),84);await page.locator('.site-radio-close').click();
 assert.equal(context.pages().length,1);assert.deepEqual(errors,[]);console.log(mode,JSON.stringify(result));await context.close();}
 await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
