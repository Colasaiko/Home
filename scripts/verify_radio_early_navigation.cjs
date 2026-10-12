const assert=require('node:assert/strict');
const {chromium}=require(process.argv[2]+'/playwright');
function audio(){const n=8000*60*2,b=Buffer.alloc(44+n);b.write('RIFF');b.writeUInt32LE(36+n,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(8000,24);b.writeUInt32LE(16000,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n,40);return b;}
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:900},reducedMotion:'reduce'});
 let popups=0;page.on('popup',()=>popups++);
 let firstDocument=true,delayed=false;
 await page.route('**/*',async route=>{
   const request=route.request(),url=new URL(request.url());
   if(url.hostname==='api.injahow.cn')return route.fulfill({status:200,contentType:'audio/wav',body:audio()});
   if(url.hostname!=='127.0.0.1')return route.abort();
   if(request.resourceType()==='document'){
     if(firstDocument)firstDocument=false;
     else if(!delayed){delayed=true;await new Promise(resolve=>setTimeout(resolve,2000));}
   }
   return route.continue();
 });
 await page.goto('http://127.0.0.1:8765/index.html');
 await page.locator('.site-radio-toggle').click();await page.locator('.site-radio-play').click();
 await page.waitForFunction(()=>!!document.getElementById('site-radio-original'));
 await page.evaluate(()=>{window.originalAudio=document.getElementById('site-radio-audio');});
 await page.locator('.site-radio-close').click();
 if(process.argv[3]==='blank')await page.locator('#site-radio-original a[href="./topic/tuijianjichang/index.html"]').evaluate(link=>link.target='_blank');
 await page.locator('#site-radio-original a[href="./topic/tuijianjichang/index.html"]').click();
 await page.waitForURL('**/topic/tuijianjichang/index.html');
 await page.waitForFunction(()=>document.querySelector('iframe')?.contentDocument?.querySelector('h1')&&!document.getElementById('site-radio-original'));
 const result=await page.evaluate(()=>({sameAudio:window.originalAudio===document.getElementById('site-radio-audio'),playing:window.siteRadio.state().playing,path:location.pathname,innerPath:document.querySelector('iframe').contentWindow.location.pathname,icons:document.querySelectorAll('.site-radio-toggle').length+document.querySelector('iframe').contentDocument.querySelectorAll('.site-radio-toggle').length}));
 assert.equal(result.sameAudio,true);assert.equal(result.playing,true);assert.equal(result.icons,1);assert.equal(result.path,result.innerPath);
 assert.equal(popups,0,'Site links keep the existing player tab');
 console.log(JSON.stringify(result));await browser.close();
})();
