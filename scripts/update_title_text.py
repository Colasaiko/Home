import os

path = r'c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_h1 = '站长精选 · 主推机场榜单'
new_h1 = '2026 机场推荐：全网最靠谱的节点榜单'

old_p = '从晚高峰抗压到全协议流媒体解锁，这里收录了 <span style="color: #fff; font-weight: bold;">微风、飞猫、大佬</span> 等数十家全网最顶尖的海外网络专线。拒绝智商税，只看硬实力。'
new_p = '寻找最靠谱的翻墙节点，拒绝盲目消费。这里为您深度测评并严选全网最稳定、最安全的高性价比机场，助您实现真正的“无感”出海体验。'

if old_h1 in content and old_p in content:
    content = content.replace(old_h1, new_h1)
    content = content.replace(old_p, new_p)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Text updated successfully!")
else:
    print("Could not find the text to replace.")
