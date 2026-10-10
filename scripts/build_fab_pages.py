"""Build grouped FAB destinations from public pages; FAQ has one entry."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def page(path, label=None, icon='◦'):
    source = ROOT / path
    assert source.exists(), path
    if label is None:
        text = source.read_text(encoding='utf-8-sig')
        heading = re.search(r'<h1\b[^>]*>(.*?)</h1>', text, re.S | re.I)
        title = heading or re.search(r'<title>(.*?)</title>', text, re.S | re.I)
        label = html.unescape(re.sub('<[^>]+>', '', title.group(1))).strip().split('|')[0].strip()
    return {'label': label, 'path': path, 'icon': icon}


def main():
    base = 'topic/tuijianjichang/'
    brand_root = ROOT / base / 'brands'
    featured = ['weifeng', 'feimao', 'muguang', 'dalao', 'firefly', 'lingmao', 'shanyue', 'wuyou', 'kuajie']
    brands = []
    for source in sorted(brand_root.glob('*.md'), key=lambda p: (featured.index(p.stem) if p.stem in featured else 99, p.stem)):
        slug = source.stem
        if not (brand_root / slug / 'index.html').exists():
            continue
        match = re.search(r'^name:\s*(.+)$', source.read_text(encoding='utf-8-sig'), re.M)
        name = match.group(1).strip().strip('"\'') if match else slug
        children = [page(base + f'brands/{slug}/index.html', '套餐与资料', '▦'), page(base + f'brands/{slug}/latest.html', '实测与追踪', '⌁')]
        offer = base + f'brands/{slug}/offer/index.html'
        if (ROOT / offer).exists():
            children.append(page(offer, '优惠详情', '◇'))
        brands.append({'label': name, 'icon': '✦', 'children': children})
    protocols = []
    compact = {'1':'Shadowsocks','2':'Trojan','3':'VLESS / XTLS','4':'VLESS Reality',
               '5':'IPLC / IEPL','6':'Hysteria / TUIC','7':'SNI 与 TLS',
               '8':'机场审计','9':'DNS 与 DoH','10':'中转与直连'}
    for p in sorted((ROOT / 'topic/cybersecurity/protocols').glob('*.html'), key=lambda p: int(p.stem)):
        entry = page(p.relative_to(ROOT).as_posix())
        # Use the first topic name for compact bubbles; keep the full page title as a tooltip.
        entry['title'] = entry['label']
        entry['label'] = compact.get(p.stem, entry['label'])
        protocols.append(entry)
    groups = [
        {'label': '品牌与选购', 'icon': '✦', 'children': [page(base+'index.html','主推品牌'), page(base+'brands/index.html','品牌总库'), page(base+'comparison.html','品牌对比','⇄'), page('brands.html','选购指南'), {'label':'全部品牌','icon':'▦','children':brands}]},
        {'label': '客户端工具', 'icon': '⚙', 'children': [page('clients.html','客户端下载'),page('api.html','配置与隐私'),page('tools.html','IP 与编码'),page('status.html','连通性检查')]},
        {'label': '网络与隐私', 'icon': '◇', 'children': [page('topic/cybersecurity/index.html','网络研究'),page('topic/cybersecurity/privacy.html','隐私检查'),page('topic/cybersecurity/gfw-monitor.html','GFW 排查'),page('topic/cybersecurity/protocols.html','协议总览'),{'label':'协议文章','icon':'⌁','children':protocols}]},
        {'label': 'AI 指南', 'icon': '✧', 'children': [page('topic/ai/'+p+'.html',label) for p,label in [('index','AI 入门'),('prompt','提问方法'),('chatgpt','ChatGPT'),('claude','Claude'),('midjourney','图片生成'),('api-deploy','API 部署')]]},
        {'label': '专题与资源', 'icon': '▦', 'children': [page('topic/index.html','主题目录'),page('bookmarks.html','资源书签'),page('news.html','资讯来源')]},
        page(base+'faq/index.html','FAQ 总入口','?')
    ]
    (ROOT/'js/floating-navigation-pages.js').write_text('window.siteFloatingPages = '+json.dumps(groups,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    print(f'Built grouped FAB destinations: {len(brands)} brands, {len(protocols)} protocol articles, tools and AI pages.')


if __name__ == '__main__':
    main()
