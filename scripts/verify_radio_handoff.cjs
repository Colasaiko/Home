const assert=require('node:assert/strict');
const {chromium}=require(process.argv[2]+'/playwright');
function wave(){const n=8000*60*2,b=Buffer.alloc(44+n);b.write('RIFF');b.writeUInt32LE(36+n,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(8000,24);b.writeUInt32LE(16000,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n,40);return b;}
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const results=[];
 for(const width of [320,390,1280])for(const file of ['index.html','api.html']){
   const page=await browser.newPage({viewport:{width,height:900}});
   let documents=0;
   await page.addInitScript(()=>{if(window.parent!==window)Object.defineProperty(window,'frameElement',{get:()=>null});});
   await page.route('**/*',async route=>{
     const request=route.request(),url=new URL(request.url());
     if(url.hostname==='api.injahow.cn')return route.fulfill({status:200,contentType:'audio/wav',body:wave()});
     if(url.hostname!=='127.0.0.1')return route.abort();
     if(request.resourceType()==='document'&&++documents===2)await new Promise(resolve=>setTimeout(resolve,500));
     return route.continue();
   });
   await page.goto('http://127.0.0.1:8765/'+file);
   if(file==='index.html'){
     await page.locator('#playBtn').scrollIntoViewIfNeeded();
     await page.waitForFunction(()=>getComputedStyle(document.querySelector('.section')).opacity==='1');
   }else{
     await page.locator('#subInput').fill('https://example.invalid/private-test-subscription');
     await page.locator('#configInput').fill('proxies: []');
     await page.locator('.site-radio-toggle').click();
   }
   await page.waitForFunction(()=>!getComputedStyle(document.getElementById('background')).backgroundImage.startsWith('cross-fade('));
   const before=await page.evaluate(()=>({y:scrollY,background:getComputedStyle(document.getElementById('background')).backgroundImage,playTop:document.getElementById('playBtn')?.getBoundingClientRect().top}));
   await page.locator(file==='index.html'?'#playBtn':'.site-radio-play').click();
   await page.waitForSelector('iframe[data-site-radio-frame]',{state:'attached'});
   assert.equal(await page.locator('iframe').evaluate(e=>e.style.visibility),'hidden','Keep the new document hidden while loading');
   assert.equal(await page.locator('#site-radio-original').isVisible(),true,'The old page remains visible during playback startup');
   assert.equal(await page.locator('.site-radio-toggle').count(),1);
   await page.waitForFunction(()=>!document.getElementById('site-radio-original'));
   const after=await page.evaluate(()=>{
     const child=document.querySelector('iframe').contentWindow,doc=child.document;
     return {y:child.scrollY,background:getComputedStyle(doc.getElementById('background')).backgroundImage,playTop:doc.getElementById('playBtn')?.getBoundingClientRect().top,icons:document.querySelectorAll('.site-radio-toggle').length+doc.querySelectorAll('.site-radio-toggle').length,innerAudio:doc.querySelectorAll('#site-radio-audio').length,playing:window.siteRadio.state().playing,sub:doc.getElementById('subInput')?.value,config:doc.getElementById('configInput')?.value,profileOpacity:doc.querySelector('.profile-section')?child.getComputedStyle(doc.querySelector('.profile-section')).opacity:null};
   });
   assert.equal(after.icons,1);assert.equal(after.innerAudio,0);assert.equal(after.playing,true);assert.equal(after.background,before.background);
   assert.ok(Math.abs(after.y-before.y)<=2,`Scroll jumped at ${width}: ${before.y} -> ${after.y}`);
   if(file==='index.html'){assert.ok(Math.abs(after.playTop-before.playTop)<=2,`Layout moved at ${width}: ${before.playTop} -> ${after.playTop}`);assert.equal(after.profileOpacity,'1');}
   else{assert.equal(after.sub,'https://example.invalid/private-test-subscription');assert.equal(after.config,'proxies: []');}
   results.push({file,width,icons:after.icons,scrollPreserved:true,backgroundPreserved:true});
   await page.close();
 }
 console.log(JSON.stringify(results));await browser.close();
})();
