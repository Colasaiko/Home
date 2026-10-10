"""Render the FAQ library as UTF-8 static HTML.

Initial run reads the existing index. Later runs read faq-articles.json.
Manual HTML edits are protected by output hashes; --force explicitly overwrites them.
"""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from copy import deepcopy
import argparse
import hashlib
import html
import json
import re
import os

from faq_content import WORKFLOWS, specs
from faq_connections import BRANDS, related_numbers, brand_context
from site_navigation import add_navigation

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'topic/tuijianjichang/faq'
SOURCE = FOLDER / 'faq-articles.json'
MANIFEST = FOLDER / 'article-output-hashes.json'


class IndexQuestions(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.rows = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        url = dict(attrs).get('href', '')
        if tag == 'a' and url.endswith('.html') and '/' not in url:
            self.active, self.url, self.text = True, url, []

    def handle_data(self, text):
        if self.active:
            self.text.append(text)

    def handle_endtag(self, tag):
        if tag == 'a' and self.active:
            self.rows.append({'url': self.url, 'title': ''.join(self.text).strip()})
            self.active = False


def client_for(title):
    for name in ['Shadowrocket', 'Quantumult X', 'Clash Verge', 'Clash Meta',
                 'Mihomo', 'v2rayNG', 'v2rayN', 'sing-box', 'Hiddify', 'Surge', 'Stash', 'Clash']:
        if name.lower() in title.lower():
            return name
    return '所用客户端'


CLIENT_SOURCES = {
    'Clash': ('Clash Verge Rev 快速入门', 'https://www.clashverge.dev/guide/quickstart.html'),
    'Clash Verge': ('Clash Verge Rev 快速入门', 'https://www.clashverge.dev/guide/quickstart.html'),
    'Clash Meta': ('Mihomo 官方文档', 'https://wiki.metacubex.one/'),
    'Mihomo': ('Mihomo 官方文档', 'https://wiki.metacubex.one/'),
    'v2rayNG': ('v2rayNG 开发者仓库', 'https://github.com/2dust/v2rayNG'),
    'v2rayN': ('v2rayN 开发者 Wiki', 'https://github.com/2dust/v2rayN/wiki'),
    'sing-box': ('sing-box 配置文档', 'https://sing-box.sagernet.org/configuration/'),
    'Hiddify': ('Hiddify 开发者仓库', 'https://github.com/hiddify/hiddify-app'),
    'Stash': ('Stash 用户文档', 'https://stash.wiki/'),
    'Surge': ('Surge 官方手册', 'https://manual.nssurge.com/'),
    'Quantumult X': ('Quantumult X 开发者资源说明', 'https://github.com/crossutility/Quantumult-X/blob/master/url-scheme.md'),
    'Shadowrocket': ('Shadowrocket 官方商店说明', 'https://apps.apple.com/us/app/shadowrocket/id932747118'),
}
PLATFORM_SOURCES = {
    'Netflix': ('Netflix 关于 VPN 的使用说明', 'https://help.netflix.com/en/node/114701'),
    'YouTube': ('YouTube 视频播放故障排查', 'https://support.google.com/youtube/answer/3037019'),
    'ChatGPT': ('ChatGPT 官方支持地区', 'https://help.openai.com/en/articles/7947663-chatgpt-supported-countries'),
    'Gemini': ('Gemini 官方可用地区与条件', 'https://support.google.com/gemini/answer/13575153'),
    'Claude': ('Claude 官方可用地区', 'https://support.claude.com/en/articles/8461763-where-can-i-access-claude'),
}


OVERRIDES = {
    18: [
        ('确认使用核心还是图形客户端', '先区分自己直接运行 sing-box 核心，还是在手机或电脑上使用带订阅功能的图形应用。核心读取 JSON 配置；图形客户端能导入哪些订阅，应以该应用的说明为准。'),
        ('获取与当前版本匹配的 JSON', '优先使用本人后台明确提供的 sing-box 配置，或由自己控制的工具转换。核对配置版本、出站协议、DNS 和路由，不把 Clash YAML 改成 .json 就当成转换完成。'),
        ('检查配置并启用所需入口', '直接使用核心时，可按官方文档运行 sing-box check -c config.json 检查配置。图形应用则选择并激活配置，确认 VPN 或系统代理权限；先保留原有可用配置再切换。'),
        ('验证请求路径和更新方式', '启动后用真实网页检查连接与规则，再确认后续由哪个应用或流程负责更新节点。解析错误按文档核对字段，连接错误检查日志；不要用不明在线转换器处理私人链接。'),
    ],
    23: [
        ('先查 Android 版本与后台格式', '打开手机系统信息并查看服务后台的客户端说明，记录节点协议与订阅格式。安卓上的 v2rayNG 与电脑的 v2rayN 是不同应用，不能照搬桌面菜单和安装包。'),
        ('比较能维护且能读配置的候选', 'v2rayNG 的开发者仓库提供 Android 版本；Hiddify 提供跨平台客户端。使用 Mihomo 配置时，应选明确支持它的维护中应用。不要把旧 Clash for Android 教程当成所有协议的兼容保证。'),
        ('从开发者渠道安装并导入', '选择与设备架构兼容的官方发布包，或开发者明确提供的商店渠道。复制后台匹配的订阅，更新出节点后选一条启动；确认 Android 的 VPN 授权，关闭另一款同时运行的代理。'),
        ('验证锁屏与切网后的使用', '先测试目标网页，再观察锁屏和 Wi-Fi、移动网络切换后的恢复。后台中断时检查系统省电限制和应用日志，只有定位到兼容问题后才换客户端，不反复重置所有设置。'),
    ],
    132: [
        ('立即重置或撤销旧订阅令牌', '在本人后台查找重置订阅或撤销链接功能，使旧地址不能继续取得配置。如果后台没有该功能，联系官方支持请求撤销；仅修改登录密码或删除帖子未必有效。'),
        ('给本人全部设备换上新地址', '重新复制正确格式的私人订阅，逐台更新手机、电脑和路由器配置，确认节点可用。清理自动更新任务中的旧 URL，避免设备继续请求已经失效的地址。'),
        ('删除公开副本并检查异常', '移除公开帖子、代码库、共享文档和截图中的旧令牌，同时检查近期用量、会话与后台通知。若密码或其他凭据也一同泄露，分别修改相关凭据；不要公开新地址作为“已修复”证明。'),
        ('验证旧链接失效并改变保存方式', '核对旧令牌已撤销，而新地址只有本人设备能够取得。把订阅保存在私人配置或密码管理器中，今后提交报错时隐藏令牌与认证信息，不再上传到陌生转换服务。'),
    ],
    52: [
        ('记录一周真实用量', '从后台记录每天新增用量，注明是否包含视频、下载、会议和云备份。优先用服务后台的计费数，而不是直接拿手机系统统计去推算全部节点消费。'),
        ('换算成一个月的基础需求', '把一周用量除以实际观察天数，再乘预计使用天数。例如 7 天计费 21GB，按 30 天估算约 90GB；这只是你的统计示例，不是所有用户的固定消耗。'),
        ('加入倍率和临时任务余量', '如果统计已经来自后台，不要再次重复乘倍率；如果用实际传输量估算，则需加入节点倍率。另列系统更新、大文件和更高清晰度视频的增量，判断 100GB 是否留有余地。'),
        ('核对重置周期后选档', '确认这 100GB 是每月额度还是固定总量，以及未用额度是否结转。接近上限时可降低视频清晰度或比较加油包，下一周期根据新记录调档，不直接买最大套餐。'),
    ],
    51: [
        ('确认当前节点倍率与统计规则', '从节点标签和后台说明确认倍率，另外核对是否计算上传和下载。不同节点组可能使用不同倍率，未标注时不要直接假定都是 1 倍。'),
        ('代入一次传输的基本公式', '计费流量通常约为实际计费传输量乘倍率。例如实际传输 3GB、倍率 1.5，基本估算为 4.5GB；如果服务使用不同单位或计费规则，应以它的说明重新计算。'),
        ('用小规模传输核对后台增量', '先记录后台已用值，完成可控的传输，等待统计同步后计算差额。上传、协议开销和时间延迟可能影响结果，不用一次对不上就认定扣量错误。'),
        ('把有效额度换算回可传输量', '已知剩余计费额度和固定倍率时，可用额度除以倍率估计还能传多少。例如剩余 20GB、2 倍节点，基础估计约 10GB；切换倍率后重新估算并预留余量。'),
    ],
}


def make_article(number, row, url):
    spec = specs()[number]
    workflow = deepcopy(WORKFLOWS[spec['workflow']])
    title = row['title']
    client = client_for(title)
    service = next((name for name in ['Netflix', 'Disney+', 'YouTube', 'TikTok', 'ChatGPT', 'Gemini', 'Claude'] if name in title),
                   '目标 AI 服务' if spec['workflow'] == 'ai' else '目标平台')
    if '短视频' in title:
        service = '所用短视频平台'
    region = next((name for name in ['香港', '台湾', '日本', '新加坡', '美国'] if name in title), '所需地区')
    audience = next((name for name in ['外贸用户', '留学生', '程序员', '跨境电商'] if name in title), '当前用户')
    page_topic = title.split('页面')[0] + '页面' if '页面' in title else title.split('应该')[0].rstrip('？')
    variables = {'client': client, 'service': service, 'region': region, 'audience': audience, 'page_topic': page_topic}
    steps = OVERRIDES.get(number, workflow['steps'])
    sources = []
    if client in CLIENT_SOURCES:
        sources.append(CLIENT_SOURCES[client])
    if service in PLATFORM_SOURCES:
        sources.append(PLATFORM_SOURCES[service])
    if number == 23:
        sources.extend([CLIENT_SOURCES['v2rayNG'], CLIENT_SOURCES['Hiddify']])
    if spec['workflow'] == 'line' and any(s in title for s in ['IPLC', 'IEPL']):
        sources.append(('运营商关于 IEPL / IPLC 的产品说明', 'https://www.cuguplus.com/product/iepl'))
    return {
        'number': number, 'title': title, 'url': url, 'originalUrl': row['url'],
        'category': spec['workflow'], 'updated': '2026-10-10',
        'why': [spec['reason'], workflow['why']], 'answer': spec['answer'],
        'steps': [{'title': t.format(**variables), 'paragraphs': [p.format(**variables)]} for t, p in steps],
        'check': workflow['check'].format(**variables), 'pitfall': workflow['pitfall'],
        'sources': [{'title': t, 'url': u} for t, u in dict.fromkeys(sources)],
    }


def esc(text):
    return html.escape(str(text), quote=True)


def paragraph(text):
    return '<p>' + esc(text) + '</p>'


def output_path(article):
    path = (FOLDER / article['url']).resolve()
    path.relative_to(ROOT)
    return path


def relative_link(article, target):
    return Path(os.path.relpath(target, output_path(article).parent)).as_posix()


def contextual_brands(article):
    context = article['brandContext']
    tokens = re.split(r'(\{[a-z]+\})', context['text'])
    inline = []
    for token in tokens:
        if re.fullmatch(r'\{[a-z]+\}', token):
            brand = token[1:-1]
            if brand not in BRANDS:
                raise ValueError(f'Unknown featured brand: {brand}')
            href = relative_link(article, ROOT / 'topic/tuijianjichang/brands' / brand / 'index.html')
            inline.append(f'<a href="{esc(href)}">{esc(BRANDS[brand])}</a>')
        else:
            inline.append(esc(token))
    hub = relative_link(article, FOLDER.parent / 'index.html')
    return '<aside class="faq-brand-context" aria-label="结合品牌资料继续核对"><p>' + ''.join(inline) + f'</p><p class="faq-brand-hub"><a href="{esc(hub)}">查看站长精选主推榜，继续比较其他品牌 →</a></p></aside>'


def render(article, articles):
    position = articles.index(article)
    previous = articles[position - 1] if position else None
    following = articles[position + 1] if position + 1 < len(articles) else None
    by_number = {a['number']: a for a in articles}
    links = []
    selected = article['relatedArticles']
    if len({item['number'] for item in selected}) != len(selected):
        raise ValueError('Repeated related article')
    for item in selected:
        if item['number'] == article['number'] or item['number'] not in by_number:
            raise ValueError('Invalid related article')
        target = by_number[item['number']]
        href = relative_link(article, output_path(target))
        links.append(f'<li><a href="{esc(href)}">{esc(target["title"])}</a>{paragraph(item["reason"])}</li>')
    steps = ''
    for i, step in enumerate(article['steps'], 1):
        steps += f'<section id="step-{i}" class="faq-step"><h3>步骤 {i}：{esc(step["title"])}</h3>' + ''.join(paragraph(p) for p in step['paragraphs']) + '</section>'
        if article['brandContext']['afterStep'] == i:
            steps += contextual_brands(article)
    toc = '<li><a href="#why">为什么要了解这个问题</a></li><li><a href="#how">如何处理这个问题</a></li>'
    toc += ''.join(f'<li class="toc-step"><a href="#step-{i}">步骤 {i}：{esc(step["title"])}</a></li>'
                   for i, step in enumerate(article['steps'], 1))
    toc += '<li><a href="#result">完成后怎么判断</a></li>'
    source_block = ''
    if article['sources']:
        toc += '<li><a href="#sources">官方资料与进一步核对</a></li>'
        source_block = '<section id="sources"><h2>官方资料与进一步核对</h2><p>客户端菜单与平台条件可能变化，操作前核对对应开发者或平台说明。</p><ul>'
        source_block += ''.join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])}</a></li>' for s in article['sources'])
        source_block += '</ul></section>'
    def sibling(item, label):
        return f'<a href="{esc(relative_link(article, output_path(item)))}"><small>{label}</small><span>{esc(item["title"])}</span></a>' if item else '<span></span>'
    resource = lambda name: esc(relative_link(article, FOLDER / name))
    step_count = len(article['steps'])
    structured = {'@context': 'https://schema.org', '@type': 'Article', 'headline': article['title'],
                  'description': article['answer'], 'inLanguage': 'zh-CN', 'dateModified': article['updated']}
    structured_json = json.dumps(structured, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(article['title'])} | 原因与解决步骤 | Cola FAQ</title>
  <meta name="description" content="{esc(article['answer'])}">
  <link rel="canonical" href="{esc(output_path(article).name)}">
  <link rel="stylesheet" href="{esc(relative_link(article, ROOT / 'css/style.css'))}">
  <link rel="stylesheet" href="{esc(relative_link(article, FOLDER.parent / 'catalog.css'))}">
  <link rel="stylesheet" href="{resource('faq-article.css')}">
  <script type="application/ld+json">{structured_json}</script>
</head>
<body>
<div id="background"></div>
<main class="catalog faq-page">
  <nav aria-label="面包屑"><a href="{esc(relative_link(article, FOLDER.parent / 'index.html'))}">推荐机场</a> / <a href="{resource('index.html')}">FAQ 知识库</a></nav>
  <article class="panel">
    <header class="faq-heading"><h1>{esc(article['title'])}</h1><p class="faq-meta">更新：{esc(article['updated'])} · 原因说明与 {step_count} 个讲解与处理环节</p></header>
    <div class="faq-layout">
      <aside class="faq-directory"><details open><summary>文章目录</summary><nav aria-label="文章目录"><ul>{toc}</ul></nav></details></aside>
      <div class="article-content faq-body">
        <section id="why"><h2>为什么要了解这个问题？</h2>{''.join(paragraph(p) for p in article['why'])}
        <div class="faq-answer"><strong>直接回答</strong>{paragraph(article['answer'])}</div></section>
        <section id="how"><h2>如何处理这个问题？</h2><p>按下面的顺序操作，每完成一步再进入下一步；已经确认的条件可以直接通过目录跳到对应环节。</p>{steps}</section>
        <section id="result"><h2>完成后怎么判断？</h2>{paragraph(article['check'])}<div class="faq-note"><strong>容易忽略的地方</strong>{paragraph(article['pitfall'])}</div></section>
        {source_block}
        <section class="faq-reading"><h2>与这个问题相关的文章</h2><ul>{''.join(links)}</ul><p><a href="{resource('index.html')}">返回全部 FAQ 问题</a></p></section>
      </div>
    </div>
    <nav class="faq-pagination" aria-label="文章翻页">{sibling(previous, '上一篇')}{sibling(following, '下一篇')}</nav>
  </article>
</main>
<script src="{resource('faq-article.js')}" defer></script>
</body>
</html>
'''


def initial_articles(index):
    parser = IndexQuestions()
    parser.feed(index)
    if len(parser.rows) != 189:
        raise ValueError(f'Expected 189 questions, found {len(parser.rows)}; review the index before authoring.')
    seen = set()
    articles = []
    for number, row in enumerate(parser.rows, 1):
        url = row['url']
        if url in seen:
            url = str(Path(url).with_suffix('')) + f'-{number:03d}.html'
        seen.add(url)
        articles.append(make_article(number, row, url))
    return articles


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--force', action='store_true', help='Explicitly overwrite manually edited generated HTML.')
    options = args.parse_args()
    index = (FOLDER / 'index.html').read_text(encoding='utf-8-sig')
    articles = json.loads(SOURCE.read_text(encoding='utf-8')) if SOURCE.exists() else initial_articles(index)
    if len({a['url'] for a in articles}) != len(articles):
        raise ValueError('Each question must have a unique URL.')
    by_number = {a['number']: a for a in articles}
    for article in articles:
        if 'relatedArticles' not in article:
            article['relatedArticles'] = [{'number': n, 'reason': by_number[n]['answer']} for n in related_numbers(article['number'])]
        if 'brandContext' not in article:
            article['brandContext'] = brand_context(article)
        if not 1 <= article['brandContext']['afterStep'] <= len(article['steps']):
            raise ValueError('Brand context must follow an article step')
    targets = {}
    for article in articles:
        if not article['steps']:
            raise ValueError('Each article must contain ordered content sections.')
        targets[article['url']] = add_navigation(render(article, articles), output_path(article))
    by_title = {a['title']: a for a in articles}
    # Keep the existing search UI, category controls and ordering.
    pattern = r'(<div class="faq-item"(?: data-search="[^"]*")?><a href=")([^"]+)(">(?:<i[^>]*></i>\s*)?)([^<]+)(</a></div>)'
    existing_titles = {html.unescape(m.group(4)).strip() for m in re.finditer(pattern, index)}
    missing = [a for a in articles if a['title'] not in existing_titles]
    if missing:
        additions = ''.join(f'\n            <div class="faq-item" data-search="{esc(" ".join(a.get("searchTerms", [])))}"><a href="{esc(a["url"])}"><i class="fa-solid fa-bolt"></i> {esc(a["title"])}</a></div>' for a in missing)
        index = index.replace('<div class="faq-grid">', '<div class="faq-grid">' + additions + '\n', 1)
    replaced = 0
    def relink(match):
        nonlocal replaced
        title = html.unescape(match.group(4)).strip()
        if title not in by_title:
            raise ValueError(f'Unrecognized question: {title}')
        replaced += 1
        return match.group(1) + by_title[title]['url'] + match.group(3) + match.group(4) + match.group(5)
    index = re.sub(pattern, relink, index)
    if replaced != len(articles):
        raise ValueError(f'Expected {len(articles)} relinked questions, found {replaced}.')
    index = re.sub(r'(?:\d+ 篇新手知识与排障文章|180\+ 新手扫盲与排障指南)', f'{len(articles)} 篇新手知识与排障文章', index)
    index = index.replace('按步骤 1—4 给出处理方法', '按问题需要分步骤给出讲解和处理方法')
    index = index.replace('const text = item.textContent.toLowerCase();', "const text = (item.textContent + ' ' + (item.dataset.search || '')).toLowerCase();")
    if '#协议与 TUN' not in index:
        index = index.replace('<span class="faq-tag" data-filter="clash">', '<span class="faq-tag" data-filter="hysteria|hy2|协议|tun">#协议与 TUN</span>\n                <span class="faq-tag" data-filter="chatgpt|gpt|grok|gemini|claude|ai">#AI 工具</span>\n                <span class="faq-tag" data-filter="clash">', 1)
    targets['index.html'] = add_navigation(index, FOLDER / 'index.html')
    old_hashes = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}
    conflicts = []
    for name in targets:
        path = FOLDER / name
        path.resolve().relative_to(ROOT)
        path.parent.mkdir(parents=True, exist_ok=True)
        if name in old_hashes and path.exists():
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != old_hashes[name] and not options.force:
                conflicts.append(name)
    if conflicts:
        raise RuntimeError('Manual HTML changes detected; preserve them or explicitly use --force: ' + ', '.join(conflicts))
    hashes = {}
    for name, text in targets.items():
        raw = text.encode('utf-8')
        path = FOLDER / name
        if not path.exists() or path.read_bytes() != raw:
            path.write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    SOURCE.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    MANIFEST.write_text(json.dumps(hashes, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(articles)} articles with distinct URLs, variable-length steps, and static directories.')
    print('UTF-8 output; manual edits will be protected on subsequent builds.')


if __name__ == '__main__':
    main()
