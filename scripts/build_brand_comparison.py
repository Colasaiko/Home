"""Build a comparison from existing brand Markdown without changing sources."""
import re
from pathlib import Path
from build_brands import ROOT, BRANDS, FEATURED, esc, field, list_field, parse_prices, block
from site_navigation import add_navigation

# Lowest one-time packages explicitly described in the existing brand articles.
ONE_TIME_TRAFFIC = {'weifeng': '270GB 总量', 'firefly': '100GB 总量',
                    'muguang': '150GB 总量', 'lingmao': '100GB 总量',
                    'shanyue': '100GB 总量', 'wuyou': '100GB 总量',
                    'kuajie': '300GB 总量'}


def amount(row):
    value = re.sub(r'[^0-9.]', '', row['originalPrice'])
    return float(value) if value else float('inf')


def traffic(front, row):
    if row.get('traffic'):
        return row['traffic']
    visual = block(front, 'visualData')
    matches = []
    for item in re.split(r'^\s+- label:\s*', visual, flags=re.M)[1:]:
        label = item.splitlines()[0].strip().strip('"\'')
        display = re.search(r'^\s+display:\s*(.+)$', item, re.M)
        plan = re.search(r'^\s+plan:\s*(.+)$', item, re.M)
        name = plan.group(1).strip().strip('"\'') if plan else label
        value = display.group(1).strip().strip('"\'') if display else ''
        if re.fullmatch(r'\d+(?:\.\d+)?\s*(?:GB|TB)(?:/月)?', value, re.I) and (name == row['name'] or (not plan and name in row['name'])):
            matches.append((len(name), value))
    if matches:
        return max(matches, key=lambda entry: entry[0])[1]
    in_name = re.search(r'(\d+(?:\.\d+)?)\s*(?:GB|G)(?![a-z])', row['name'], re.I)
    return in_name.group(1) + 'GB（套餐名标注）' if in_name else '详见品牌套餐说明'


def main():
    rows = []
    sources = sorted(BRANDS.glob('*.md'), key=lambda p: (FEATURED.index(p.stem) if p.stem in FEATURED else 99, p.stem))
    for source in sources:
        slug = source.stem
        if not (BRANDS / slug / 'index.html').exists():
            continue
        front = re.split(r'^---\s*$', source.read_text(encoding='utf-8-sig'), maxsplit=2, flags=re.M)[1]
        prices = parse_prices(front)
        cells = []
        monthly = None
        for period in ['月付', '年付', '一次性']:
            options = [p for p in prices if p['period'] == period]
            if not options:
                cells.append('<td>未列出该类型套餐</td>')
                continue
            price = min(options, key=amount)
            if period == '月付':
                monthly = amount(price)
            validity = price.get('validity', '有效期详见品牌说明') if period == '一次性' else '流量重置规则详见品牌说明'
            volume = ONE_TIME_TRAFFIC[slug] if period == '一次性' and slug in ONE_TIME_TRAFFIC else traffic(front, price)
            cells.append(f'<td><strong>{esc(price["originalPrice"])}</strong> / {period}<small>{esc(price["name"])}<br>流量：{esc(volume)}<br>{esc(validity)}</small></td>')
        name = field(front, 'name', slug)
        lines = list_field(front, 'lineType') or list_field(front, 'networkArchitecture')
        protocol = list_field(front, 'protocols')
        ai = list_field(front, 'aiSupport')
        featured = slug in FEATURED
        rows.append(f'''<tr data-featured="{str(featured).lower()}" data-monthly="{monthly if monthly is not None else ''}" data-search="{esc(name.lower())}">
<td><label><input type="checkbox" class="pick-brand" aria-label="选择{name}"> 对比</label><h3><a href="brands/{slug}/index.html">{esc(name)}</a></h3>{'<span class="badge">主推品牌</span>' if featured else ''}</td>
{''.join(cells)}<td>{esc(' / '.join(lines) or '详见品牌说明')}<small>协议：{esc(' / '.join(protocol) or '详见配置说明')}</small></td>
<td>{esc(field(front, 'deviceLimit', '详见品牌套餐说明'))}</td><td>{esc(' / '.join(ai) or '详见品牌说明')}<small>按品牌资料列出，具体节点结果见报告。</small></td>
<td><a href="brands/{slug}/index.html">套餐与优惠规则 →</a><br><a href="brands/{slug}/latest.html">查看实测报告 →</a></td></tr>''')
    content = f'''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>机场品牌对比：月付价格、年付套餐、流量与设备限制 | Cola 站长</title><meta name="description" content="横向比较微风、飞猫、暮光、大佬、Firefly 等机场品牌的月付原价、年付金额、一次性流量包、线路与设备限制。按预算筛选或勾选品牌，继续查看套餐详情与实测报告。">
<link rel="stylesheet" href="../../css/style.css"><link rel="stylesheet" href="catalog.css"><link rel="stylesheet" href="comparison.css?v=20261010-2"><script src="comparison.js?v=20261010-2" defer></script></head><body><div id="background"></div><main class="catalog comparison">
<nav aria-label="面包屑"><a href="../../index.html">首页</a> / <a href="../index.html">主题目录</a> / 品牌对比</nav>
<section class="panel"><p class="eyebrow">先比较，再看具体套餐</p><h1>哪个机场品牌适合你？放在一起看</h1><p>先看能接受的付款金额，再看流量、设备和线路。这里收录 {len(rows)} 个品牌，主推品牌排在前面；① 勾选至少 2 个感兴趣的品牌；② 点击「比较已选品牌」；③ 表格只保留这些品牌，逐项比较价格与服务条件。</p><p class="source-note">资料整理日期：2026-10-10。价格来自本站保存的品牌套餐资料，显示各类型最低原价，不自动套用优惠码。月付、年付与一次性列可能是不同套餐；年付金额为一次实际付款金额，不是每月扣款。流量数字请结合套餐的重置说明阅读，未明确的规则在品牌详情核对。</p>
<div class="filters"><label>查找品牌<input id="compare-search" type="search" placeholder="例如：微风、Firefly"></label><label>品牌范围<select id="compare-scope"><option value="all">全部品牌</option><option value="featured">只看主推品牌</option></select></label><label>月付原价预算<select id="compare-budget"><option value="all">不限预算</option><option value="20">每月不超过 ¥20</option><option value="30">每月不超过 ¥30</option><option value="50">每月不超过 ¥50</option></select></label></div>
<p class="source-note">手机上可左右滑动对比表。预算筛选只比较月付原价；只有年付或一次性套餐的品牌不会纳入月付预算结果。</p></section>
<section class="panel" aria-labelledby="table-title"><h2 id="table-title">价格与服务条件对比</h2><div class="comparison-toolbar"><p id="compare-selection" role="status" aria-live="polite">先在表格中勾选至少 2 个品牌，再点击「比较已选品牌」。</p><div class="actions"><button id="compare-selected" type="button" aria-pressed="false" disabled>比较已选品牌（0）</button><button id="compare-reset" type="button">清空筛选与选择</button></div><p id="compare-count" role="status" aria-live="polite">显示 {len(rows)} 个品牌</p></div><div class="table-wrap" tabindex="0" role="region" aria-label="可横向滚动的品牌对比表"><table><caption>同一付款周期内比较价格，再进入品牌详情核对具体流量与优惠。</caption><thead><tr><th scope="col">品牌</th><th scope="col">最低月付原价</th><th scope="col">最低年付原价</th><th scope="col">最低一次性原价</th><th scope="col">线路与协议</th><th scope="col">设备条件</th><th scope="col">AI 使用资料</th><th scope="col">继续了解</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><p id="compare-empty" hidden>没有符合条件的品牌。可以提高预算、清空关键词，或点击「返回品牌列表」。</p></section>
<section class="panel"><h2>看完对比，怎么决定？</h2><ol><li><strong>先定预算。</strong>优先比较相同付款周期，优惠资格在品牌详情确认。</li><li><strong>再看用量。</strong>日常网页、AI、视频与下载的用量不同，月度流量与一次性总量应分别判断。</li><li><strong>核对设备与实际表现。</strong>查看设备条件及品牌实测报告，选择与自己网络和任务相近的测试记录。</li><li><strong>继续完成配置。</strong>购买后选择客户端、导入订阅，再验证访问和隐私设置。</li></ol><div class="card-links"><a href="index.html">主推品牌介绍 →</a><a href="brands/index.html">完整品牌资料 →</a><a href="../../clients.html">按设备选客户端 →</a><a href="../cybersecurity/privacy.html">了解隐私检查 →</a></div></section>
</main></body></html>'''
    output = ROOT / 'topic/tuijianjichang/comparison.html'
    output.write_text(add_navigation(content, output), encoding='utf-8')
    print(f'Built comparison for {len(rows)} brands.')


if __name__ == '__main__':
    main()
