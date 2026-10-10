import os

path = r'c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_header = """    <section class="panel">
        <h1>🌟 站长精选推荐机场主推榜</h1>
        <p>微风、飞猫、暮光、大佬、Firefly、灵猫、闪跃、无忧、跨界。</p>
        <p class="source-note">价格来自项目已收录资料，本次未实时核验官网；实际费用以结算页为准。</p>
    </section>"""

new_header = """    <header class="hero-section" style="text-align: center; margin-bottom: 40px; padding: 50px 20px; background: linear-gradient(145deg, rgba(30,30,30,0.8), rgba(15,15,15,0.95)); border: 1px solid rgba(255,184,0,0.3); border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.6), inset 0 0 20px rgba(255,184,0,0.05); position: relative; overflow: hidden;">
        <!-- Glowing background effect -->
        <div style="position: absolute; top: -50%; left: 50%; transform: translateX(-50%); width: 200px; height: 200px; background: rgba(255,184,0,0.15); filter: blur(80px); border-radius: 50%; z-index: 0;"></div>
        
        <div style="position: relative; z-index: 1;">
            <div style="display: inline-block; padding: 6px 16px; background: rgba(255,184,0,0.1); border: 1px solid rgba(255,184,0,0.4); color: #ffb800; border-radius: 30px; font-size: 0.9rem; font-weight: bold; margin-bottom: 20px; letter-spacing: 1px;">
                <i class="fa-solid fa-crown"></i> 2026 全网硬核严选
            </div>
            
            <h1 style="font-size: 2.8rem; font-weight: 900; margin: 0 0 20px 0; background: linear-gradient(to right, #ffffff, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 2px; text-shadow: 0 5px 15px rgba(0,0,0,0.5);">站长精选 · 主推机场榜单</h1>
            
            <p style="font-size: 1.15rem; color: #b0b0b0; max-width: 700px; margin: 0 auto 20px auto; line-height: 1.8;">
                从晚高峰抗压到全协议流媒体解锁，这里收录了 <span style="color: #fff; font-weight: bold;">微风、飞猫、大佬</span> 等数十家全网最顶尖的海外网络专线。拒绝智商税，只看硬实力。
            </p>
            
            <p class="source-note" style="color: #777; font-size: 0.85rem; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 20px; max-width: 500px; margin: 0 auto;">
                <i class="fa-solid fa-circle-info"></i> 价格档案基于收录快照，实际计费请以官网结算页为准
            </p>
        </div>
    </header>"""

if old_header in content:
    content = content.replace(old_header, new_header)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Hero header successfully upgraded!")
else:
    print("Could not find the exact old header block.")
