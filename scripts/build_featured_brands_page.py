"""Build the root featured-brand gateway from existing brand sources."""
import re
from build_brands import ROOT, BRANDS, FEATURED, field, list_field, parse_prices, esc
from site_navigation import add_navigation


def price_value(row):
    return float(re.sub(r'[^0-9.]', '', row['originalPrice']))


def main():
    cards = []
    for slug in FEATURED:
        front = re.split(r'^---\s*$', (BRANDS / (slug + '.md')).read_text(encoding='utf-8-sig'), maxsplit=2, flags=re.M)[1]
        name = field(front, 'name', slug)
        prices = parse_prices(front)
        summaries = []
        for period in ('月付', '年付'):
            options = [row for row in prices if row['period'] == period]
            if options:
                row = min(options, key=price_value)
                summaries.append(f'<span>{period}原价 <strong>{esc(row["originalPrice"])} 起</strong></span>')
        features = list_field(front, 'features')[:3]
        prefix = 'topic/tuijianjichang/brands/' + slug + '/'
        cards.append(f'''<section class="featured-brand" aria-labelledby="brand-{slug}"><p class="brand-kicker">主推品牌</p><h2 id="brand-{slug}">{esc(name)}</h2>
<div class="featured-price">{''.join(summaries)}</div><ul>{''.join('<li>'+esc(feature)+'</li>' for feature in features)}</ul>
<div class="featured-links"><a class="featured-primary" href="{prefix}index.html">查看套餐与品牌资料 →</a><a href="{prefix}latest.html">查看实测报告 →</a><a href="topic/tuijianjichang/comparison.html?select={slug}">与其他品牌对比 →</a></div>
<div class="featured-purchase"><span>购买入口待补充</span></div></section>''')
    text = '''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>主推机场品牌：微风、飞猫、暮光、Firefly 等套餐与实测 | Cola 站长</title>
<meta name="description" content="查看微风、飞猫、暮光、大佬、Firefly、灵猫、闪跃、无忧与跨界九个主推机场品牌，了解月付与年付原价、套餐资料和实测报告，并进入品牌对比页筛选。">
<link rel="stylesheet" href="css/style.css"><link rel="stylesheet" href="css/featured-brands.css?v=20261010-1"></head><body><div id="background"></div><main class="featured-brands-page">
<nav class="featured-breadcrumb" aria-label="面包屑"><a href="index.html">首页</a> / <a href="topic/index.html">主题目录</a> / 主推品牌</nav>
<section class="featured-intro"><p class="brand-kicker">按品牌看资料，按条件做选择</p><h1>九个主推品牌，先看套餐与实测</h1><p>微风、飞猫、暮光、大佬、Firefly、灵猫、闪跃、无忧、跨界。先了解每个品牌的套餐和使用条件，再把感兴趣的品牌放进对比页。</p><div class="featured-top-links"><a href="#featured-list">查看主推品牌 ↓</a><a href="topic/tuijianjichang/comparison.html">进入品牌对比 →</a></div><p class="featured-note">购买跳转入口稍后补充。现在可以查看品牌资料、实测报告和套餐对比。以下显示原价，优惠资格与流量规则在对应品牌详情中查看；年付为一次支付整年金额。</p></section>
<div class="featured-grid" id="featured-list">''' + ''.join(cards) + '''</div>
<section class="featured-next"><h2>看完品牌，下一步怎么选？</h2><ol><li><strong>确定预算和用量。</strong>先选择月付或年付，再核对流量、设备条件和重置规则。</li><li><strong>选几个品牌集中对比。</strong>从品牌卡片进入对比页，当前品牌会自动选中，再勾选其他品牌。</li><li><strong>阅读实测报告。</strong>结合报告的测试时间、节点和你的使用场景判断。</li></ol><a href="topic/tuijianjichang/brands/index.html">查看更多品牌资料 →</a></section>
</main></body></html>'''
    output = ROOT / 'brands.html'
    output.write_text(add_navigation(text, output), encoding='utf-8')
    print('Built root brands page with nine featured brands and pending purchase placeholders.')


if __name__ == '__main__':
    main()
