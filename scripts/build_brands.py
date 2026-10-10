"""Build the static brand catalog using preserved Markdown and historical Excel data.

Run: python scripts/build_brands.py
No external packages are required. Existing brand Markdown is never modified.
"""
from pathlib import Path
import html
from html.parser import HTMLParser
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TOPIC = ROOT / 'topic' / 'tuijianjichang'
BRANDS = TOPIC / 'brands'
REFERENCE = json.loads((TOPIC / 'brand_reference.json').read_text(encoding='utf-8'))
ALIASES = {
    'weifeng': '微风网络', 'firefly': 'FireFly 萤火虫', 'kuajie': '跨界云',
    'shanyue': '闪跃', 'wuyou': '无忧链接', 'lingmao': '灵猫', 'bitznet': 'BitzNet',
    'feimao': '飞猫云', 'sogo': 'Sogo云', 'muguang': '暮光加速', 'xingdaomeng': '星岛梦',
    'weitu': '唯兔云', 'guangsu': '光速云', 'u1s1': 'U1S1', 'jilian': '极连云',
    'guangnian': '光年梯', 'yifan': '一翻云', 'ermao': '二猫云', 'edge': '边缘节点',
    'kexin': '可信云', 'sujie': '速界机场', 'kuaili': '快狸', 'feiv': '飞V',
    'tizi': '梯子云', 'wavenet': 'WaveNet', 'lingdong': '灵动云',
    'invisible': '隐形人', 'nanocloud': 'NanoCloud', 'phantom': 'Phantom',
}
PERIODS = [('monthly', '月付'), ('quarterly', '季付'), ('halfYear', '半年付'),
           ('yearly', '年付'), ('oneTime', '一次性')]
FEATURED = ['weifeng', 'feimao', 'muguang', 'dalao', 'firefly', 'lingmao',
            'shanyue', 'wuyou', 'kuajie']
RECOMMENDATION_NAMES = {'weifeng': '微风', 'feimao': '飞猫', 'muguang': '暮光',
                        'firefly': 'Firefly', 'lingmao': '灵猫', 'shanyue': '闪跃',
                        'wuyou': '无忧', 'kuajie': '跨界'}


def esc(value):
    return html.escape(str(value or ''), quote=True)


def scalar(value):
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    return value.strip("'")


def field(front, key, default=''):
    found = re.search(r'^' + re.escape(key) + r':\s*([^\n]*)', front, re.M)
    return scalar(found.group(1)) if found else default


def block(front, key):
    # Some existing documents have invalid YAML under visualData. Read only the
    # requested top-level section, without silently repairing the source files.
    match = re.search(r'^' + re.escape(key) + r':[^\n]*\n((?:[ \t]+[^\n]*\n|\n)*)', front, re.M)
    return match.group(1) if match else ''


def list_field(front, key):
    return [scalar(x) for x in re.findall(r'^  - (.+)$', block(front, key), re.M)]


def parse_prices(front):
    prices = []
    for item in re.split(r'^  - name:\s*', block(front, 'pricing'), flags=re.M)[1:]:
        lines = item.splitlines()
        row = {'name': scalar(lines[0])}
        for line in lines[1:]:
            match = re.match(r'^    (\w+):\s*(.*)$', line)
            if match:
                row[match.group(1)] = scalar(match.group(2))
        if 'originalPrice' not in row and 'price' in row:
            row['originalPrice'] = row['price']
        if 'originalPrice' not in row or 'period' not in row:
            raise ValueError(f'Incomplete price row: {row}')
        prices.append(row)
    return prices


def safe_url(url):
    return url if url.startswith(('https://', 'http://')) else ''


def inline(text):
    text = esc(text)
    def link(match):
        url = html.unescape(match.group(2))
        if not (safe_url(url) or url.startswith(('./', '../', '#', '/'))):
            return match.group(1)
        if url.startswith('/') and not (ROOT / url.lstrip('/').split('#')[0]).exists():
            # Preserve references to topics absent from this site as plain text.
            return match.group(1)
        return f'<a href="{esc(url)}">{match.group(1)}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return text


class SafeHTML(HTMLParser):
    """Preserve content blocks embedded in Markdown without running source code."""
    allowed = {'div', 'span', 'section', 'p', 'h2', 'h3', 'h4', 'h5', 'h6',
               'strong', 'em', 'ul', 'ol', 'li', 'br', 'blockquote', 'code',
               'table', 'thead', 'tbody', 'tr', 'th', 'td', 'a'}

    def __init__(self):
        super().__init__()
        self.output = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'iframe'}:
            self.skip += 1
        elif tag in self.allowed and not self.skip:
            attributes = ''
            if tag == 'a':
                href = next((v for k, v in attrs if k == 'href'), '') or ''
                if safe_url(href) or href.startswith(('./', '../', '#')):
                    attributes = f' href="{esc(href)}"'
            self.output.append(f'<{tag}{attributes}>')

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'iframe'}:
            self.skip = max(0, self.skip - 1)
        elif tag in self.allowed and tag != 'br' and not self.skip:
            self.output.append(f'</{tag}>')

    def handle_data(self, data):
        if not self.skip:
            self.output.append(esc(data))


def markdown(content):
    lines = content.strip().splitlines()
    out, paragraph = [], []
    def flush():
        if paragraph:
            out.append('<p>' + '<br>'.join(inline(x) for x in paragraph) + '</p>')
            paragraph.clear()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush()
            i += 1
            continue
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        if re.match(r'^</?[a-zA-Z][^>]*>', line):
            flush()
            raw = []
            while i < len(lines) and lines[i].strip():
                raw.append(lines[i])
                i += 1
            sanitizer = SafeHTML()
            sanitizer.feed('\n'.join(raw))
            out.append(''.join(sanitizer.output))
            continue
        elif heading:
            flush()
            level = max(2, len(heading.group(1)))
            out.append(f'<h{level}>{inline(heading.group(2))}</h{level}>')
        elif (line.startswith('|') and i + 1 < len(lines)
              and re.match(r'^\s*\|?\s*:?-{3,}', lines[i + 1])):
            flush()
            headers = line.strip('|').split('|')
            out.append('<div class="table-wrap"><table><thead><tr>' +
                       ''.join('<th scope="col">' + inline(c.strip()) + '</th>' for c in headers) +
                       '</tr></thead><tbody>')
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                out.append('<tr>' + ''.join('<td>' + inline(c.strip()) + '</td>'
                           for c in lines[i].strip().strip('|').split('|')) + '</tr>')
                i += 1
            out.append('</tbody></table></div>')
            continue
        elif re.match(r'^(?:[-*]|\d+\.)\s+', line):
            flush()
            ordered = bool(re.match(r'^\d+\.', line))
            tag = 'ol' if ordered else 'ul'
            pattern = r'^\d+\.\s+' if ordered else r'^[-*]\s+'
            out.append(f'<{tag}>')
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                out.append('<li>' + inline(re.sub(pattern, '', lines[i].strip())) + '</li>')
                i += 1
            out.append(f'</{tag}>')
            continue
        elif line.startswith('>'):
            flush()
            out.append('<blockquote>' + inline(line.lstrip('> ')) + '</blockquote>')
        elif re.match(r'^[-*_]{3,}$', line):
            flush()
            out.append('<hr>')
        else:
            paragraph.append(line)
        i += 1
    flush()
    return '\n'.join(out)


def page(title, description, content, depth, canonical='./', noindex=False):
    # file:// previews do not resolve directory indexes like HTTP servers do.
    # Explicit filenames work both locally and on GitHub Pages.
    def directory_index(match):
        url = match.group(2)
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url) and not url.startswith('//'):
            url += 'index.html'
        return match.group(1) + url + match.group(3)
    content = re.sub(r'(<a\b[^>]*\bhref=")([^"]*/)(")', directory_index, content)
    base = '../' * depth
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ''
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
{robots}
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="stylesheet" href="{base}css/style.css">
  <link rel="stylesheet" href="{base}topic/tuijianjichang/catalog.css">
</head>
<body>
  <div id="background"></div>
  <main class="catalog">{content}</main>
</body>
</html>
'''


def write(path, text):
    if path.suffix.lower() == '.html':
        from site_navigation import add_navigation
        text = add_navigation(text, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def price_summary(brand):
    prices = brand['prices']
    summary = []
    for period in ['月付', '年付', '一次性']:
        options = []
        for row in prices:
            number = re.search(r'\d+(?:\.\d+)?', row['originalPrice'])
            if row['period'] == period and number:
                options.append((float(number.group()), row['originalPrice']))
        if options:
            summary.append(f'{period} {min(options)[1]} 起')
    return '；'.join(summary) or '套餐价格见品牌详情'


def card(brand, prefix=''):
    slug, name = brand['slug'], brand['name']
    return f'''<article class="brand-card">
<h2><a href="{prefix}{slug}/">{esc(name)}</a></h2>
<p>{esc('；'.join(brand['features'][:3]) or '套餐、线路与使用资料整理。')}</p>
<p class="price">{esc(price_summary(brand))}</p>
<div class="card-links"><a href="{prefix}{slug}/">价格与资料</a>
<a href="{prefix}{brand['faqRoute']}/">常见问题</a></div></article>'''


def prices_table(prices):
    rows = ''.join(f'<tr><td>{esc(p["name"])}</td><td>{esc(p["period"])}</td>'
                   f'<td>{esc(p["originalPrice"])}</td><td>{esc(p.get("validity") or p.get("deviceLimit") or p.get("note") or "—")}</td></tr>'
                   for p in prices)
    return f'''<div class="table-wrap"><table><caption>项目品牌资料中收录的套餐标价（人民币）</caption>
<thead><tr><th scope="col">套餐</th><th scope="col">付款周期</th><th scope="col">周期总价</th><th scope="col">补充说明</th></tr></thead><tbody>{rows}</tbody></table></div>'''


def old_reference(brand):
    ref = brand['reference']
    if not ref:
        return '<p class="source-note">提供的旧照片表格未收录这个品牌；本页采用项目内已有品牌资料。</p>'
    old_plans = [p for p in REFERENCE['plans'] if p['brand'] == ref['name']]
    headers = ['套餐', '流量标注'] + [p[1] for p in PERIODS] + ['备注']
    rows = []
    for p in old_plans:
        values = [p['plan'], p['traffic']] + [f'¥{p[k]:g}' if isinstance(p[k], (float, int)) else p[k] or '—' for k, _ in PERIODS] + [p['note'] or '—']
        rows.append('<tr>' + ''.join(f'<td>{esc(v)}</td>' for v in values) + '</tr>')
    alias_note = f'<p>表格原品牌名称：{esc(ref["name"])}。该旧名称与项目名称不同，资料关联有待进一步核对。</p>' if brand['slug'] == 'edge' else ''
    description = '<p>' + '<br>'.join(esc(ref['description']).splitlines()) + '</p>'
    return f'''<details class="reference"><summary>旧照片套餐与品牌资料参考（{len(old_plans)} 条）</summary>
<p class="source-note">来源：{esc(REFERENCE['source'])}。原始记录没有核验日期，以下价格、流量和优惠不代表当前可购买条件。空缺表示原表未提供。</p>
{alias_note}{description}
<p>原表优惠记录：{esc(ref['coupon'])}（有效性未核验）。</p>
<div class="table-wrap"><table><caption>旧照片套餐原始记录（价格为对应周期总价）</caption><thead><tr>{''.join('<th scope="col">'+esc(h)+'</th>' for h in headers)}</tr></thead><tbody>{''.join(rows)}</tbody></table></div></details>'''


def main():
    brands = []
    for source in sorted(BRANDS.glob('*.md')):
        raw = source.read_text(encoding='utf-8-sig')
        parts = re.split(r'^---\s*$', raw, maxsplit=2, flags=re.M)
        if len(parts) != 3:
            raise ValueError(f'Missing front matter: {source}')
        front, body = parts[1], parts[2].strip()
        match = re.search(r'^##\s+[^\n]*(?:FAQ|常见问题)[^\n]*$', body, re.M | re.I)
        faq = ''
        if match:
            start = match.start()
            next_heading = re.search(r'^##\s+', body[match.end():], re.M)
            end = match.end() + next_heading.start() if next_heading else len(body)
            faq = body[start:end].strip()
            body = (body[:start] + body[end:]).strip()
        slug = source.stem
        ref = next((r for r in REFERENCE['brands'] if r['name'] == ALIASES.get(slug)), None)
        brand = {'slug': slug, 'name': field(front, 'name', slug),
                 'order': int(field(front, 'order', '999')), 'prices': parse_prices(front),
                 'features': list_field(front, 'features'), 'front': front,
                 'body': body, 'faq': faq, 'reference': ref}
        if not brand['prices']:
            raise ValueError(f'No project prices: {slug}')
        brands.append(brand)
    brands.sort(key=lambda b: (b['order'], b['slug']))
    route_file = TOPIC / 'faq_routes.json'
    routes = json.loads(route_file.read_text(encoding='utf-8')) if route_file.exists() else {}
    next_id = max([int(v.removeprefix('FAQ')) for v in routes.values()] or [0]) + 1
    for brand in brands:
        if brand['slug'] not in routes:
            routes[brand['slug']] = f'FAQ{next_id}'
            next_id += 1
        brand['faqRoute'] = routes[brand['slug']]
    if len(routes.values()) != len(set(routes.values())):
        raise ValueError('Duplicate FAQ routes')
    write(route_file, json.dumps(routes, ensure_ascii=False, indent=2) + '\n')
    for brand in brands:
        name, slug, faq_route = brand['name'], brand['slug'], brand['faqRoute']
        description = f'{name}套餐价格、付款周期、服务资料及独立常见问题。'
        facts = []
        for key, label in [('deviceLimit', '设备限制'), ('speedLimit', '速率说明'),
                           ('ipType', 'IP 类型'), ('nodeMultiplier', '节点倍率')]:
            value = field(brand['front'], key)
            if value:
                facts.append(f'<dt>{label}</dt><dd>{esc(value)}</dd>')
        for key, label in [('protocols', '协议'), ('lineType', '线路'),
                           ('paymentMethods', '支付方式'), ('aiSupport', 'AI 应用'),
                           ('streamingSupport', '流媒体')]:
            values = list_field(brand['front'], key)
            if values:
                facts.append(f'<dt>{label}</dt><dd>{esc("、".join(values))}</dd>')
        content = f'''<nav aria-label="面包屑"><a href="../../index.html">推荐机场</a> / <a href="../">全部品牌</a> / {esc(name)}</nav>
<article class="panel"><h1>{esc(name)}套餐价格与品牌资料</h1>
<p class="source-note">主表来自项目已收录品牌资料，本次未实时核验官网；请以购买时结算页为准。月付、年付及一次性费用分别列示，不把年付折算价当成月付售价。</p>
<p class="price">{esc(price_summary(brand))}</p>
<h2>套餐价格</h2>{prices_table(brand['prices'])}
<h2>服务资料</h2><ul>{''.join('<li>'+esc(f)+'</li>' for f in brand['features'])}</ul>
<dl class="facts">{''.join(facts)}</dl>
<div class="article-body">{markdown(brand['body'])}</div>
<aside class="faq-entry"><h2>{esc(name)}常见问题</h2><p>关于价格、流量及使用规则的完整问答已整理到独立页面。</p>
<a class="button" href="../{faq_route}/">阅读{esc(name)} FAQ</a></aside></article>'''
        write(BRANDS / slug / 'index.html', page(f'{name}套餐价格与资料 | 机场品牌库', description, content, 4))
        original_faq = bool(brand['faq'])
        faq = brand['faq'] or f'''## {name}常见问题

### {name}套餐价格是多少？
项目已收录的标价包括：{price_summary(brand)}。完整付款周期与套餐总价请查看品牌详情页；上述数据未在本次实时核验。

### {name}收录了哪些服务资料？
项目资料记录：{'；'.join(brand['features']) or '具体套餐及付款周期见品牌详情'}。实际服务条件请核对官方购买页面。

### 如何区分周期套餐和一次性套餐？
本品牌详情页为每条套餐列明付款周期。一次性表示对应记录的付款方式，不等同于无限流量；流量有效期按该套餐说明确认。
'''
        write(BRANDS / faq_route / 'content.md', faq + '\n')
        source_note = '本页保留项目原有 FAQ 原文，价格与活动条件未在本次实时核验。' if original_faq else '本页根据项目已收录的套餐与服务字段建立基础 FAQ，后续可补充经核验的具体使用问答。'
        faq_content = f'''<nav aria-label="面包屑"><a href="../">全部品牌</a> / <a href="../{slug}/">{esc(name)}</a> / 常见问题</nav>
<article class="panel"><h1>{esc(name)}常见问题 FAQ</h1><p class="source-note">{source_note}</p>
<p><a href="../{slug}/">查看{esc(name)}完整套餐价格与资料</a></p>
<div class="article-body">{markdown(faq)}</div>
<p><a class="button" href="../{slug}/">返回{esc(name)}品牌详情</a></p></article>'''
        write(BRANDS / faq_route / 'index.html', page(f'{name}常见问题 FAQ | 价格、流量与使用说明', f'{name}常见问题与解答，整理项目已有套餐和使用资料，并链接完整品牌价格页。', faq_content, 4))
    count = len(brands)
    catalog = f'''<nav aria-label="面包屑"><a href="../index.html">返回推荐机场</a> / 全部品牌</nav>
<section class="panel"><h1>全部机场品牌与套餐资料</h1><p>共收录 {count} 个品牌，提供套餐价格、服务资料与独立 FAQ。</p>
<p class="source-note">以下起价来自项目已收录标价，未实时核验；年付和一次性价格均为对应周期总价。</p>
<label for="brand-search">搜索品牌</label><input id="brand-search" type="search" placeholder="输入品牌名称" autocomplete="off">
<p id="search-count" aria-live="polite">显示 {count} 个品牌</p></section>
<section class="brand-grid" aria-label="全部品牌">{''.join(card(b) for b in brands)}</section>
<section class="panel"><h2>品牌 FAQ 索引</h2><ul class="faq-index">{''.join(f'<li><a href="{b["faqRoute"]}/">{esc(b["name"])}常见问题</a></li>' for b in brands)}</ul></section>
<script src="../catalog.js" defer></script>'''
    write(BRANDS / 'index.html', page('全部机场品牌与套餐价格 | 品牌资料库', f'收录{count}个机场品牌的价格、服务资料与常见问题。', catalog, 3))
    by_slug = {b['slug']: b for b in brands}
    def featured_card(slug):
        if slug == 'dalao' and slug not in by_slug:
            return '<article class="brand-card"><h2>大佬</h2><p>品牌资料待补充。</p><p class="source-note">套餐价格与详情入口待确认。</p></article>'
        brand = dict(by_slug[slug])
        brand['name'] = RECOMMENDATION_NAMES.get(slug, brand['name'])
        return card(brand, 'brands/')
    featured = ''.join(featured_card(s) for s in FEATURED[:4])
    team = ''.join(featured_card(s) for s in FEATURED[4:])
    recommendation = f'''<nav aria-label="面包屑"><a href="../index.html">返回专题库</a></nav>
<section class="panel"><h1>推荐机场与品牌资料</h1><p>微风、飞猫、暮光、大佬、Firefly、灵猫、闪跃、无忧、跨界。</p>
<p class="source-note">价格来自项目已收录资料，本次未实时核验官网；实际费用以结算页为准。</p>
</section>
<section class="brand-grid" aria-label="推荐品牌">{featured}{team}</section>
<p><a class="button" href="brands/">查看全部 {count} 个机场品牌</a></p>'''
    write(TOPIC / 'index.html', page('推荐机场 | 套餐价格与品牌资料', '浏览机场套餐、服务资料和完整品牌库，独立 FAQ 解答品牌相关问题。', recommendation, 2))
    # Keep incoming links to the former list working, without duplicating the catalog.
    legacy = '<section class="panel"><h1>全部品牌库已迁移</h1><p>品牌列表与价格资料已集中整理。</p><a class="button" href="brands/">进入全部机场品牌库</a></section><script>location.replace("brands/index.html" + location.hash);</script>'
    write(TOPIC / 'other.html', page('全部品牌库已迁移', '访问全部品牌库。', legacy, 2, 'brands/', True))
    print(f'Built {count} brand pages, {count} FAQ pages, catalog and recommendation page.')
    print(f'Preserved {sum(bool(b["faq"]) for b in brands)} original FAQ sections; generated {sum(not bool(b["faq"]) for b in brands)} basic FAQ frameworks.')


if __name__ == '__main__':
    main()
