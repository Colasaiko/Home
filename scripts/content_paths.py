"""Render contextual, crawlable reading paths without changing authored brand data."""
from pathlib import Path
import html
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'topic/tuijianjichang/'
SEC = 'topic/cybersecurity/'
DEST = {
    'brands': (BASE + 'index.html', '按用途比较主推品牌'),
    'catalog': (BASE + 'brands/index.html', '查看全部品牌资料'),
    'faq': (BASE + 'faq/index.html', '按问题查找 FAQ'),
    'privacy': (SEC + 'privacy.html', '理解订阅、DNS 与浏览器隐私'),
    'gfw': (SEC + 'gfw-monitor.html', '区分封锁、节点故障与本地问题'),
    'protocol': (SEC + 'protocols.html', '看懂协议与线路的区别'),
    'api': ('api.html', '检查配置与测试结果'),
    'status': ('status.html', '对照浏览器连通性与请求耗时'),
    'client': ('clients.html', '选择适合设备的客户端'),
    'tools': ('tools.html', '核对出口 IP 与订阅编码'),
    'timeout': ('FAQ/ClashVergeAllTimeout.html', 'Clash 全部超时的排查顺序'),
    'dns': ('FAQ/ClashDNSFailed.html', 'DNS 失败如何逐步定位'),
    'hy2': ('FAQ/WhatIsHysteria2.html', 'Hysteria2 是什么，如何检查兼容'),
    'mac': ('FAQ/ClashForMac.html', 'Mac 上如何选择 Clash 客户端'),
    'quota': ('FAQ/MonthlyAirportTraffic.html', '每月流量怎么估算'),
    'ai': ('FAQ/GrokNotOpening.html', 'AI 网站打不开怎么判断原因'),
    'rules': ('FAQ/ClashRulesVsGlobal.html', '规则模式与全局模式怎么选择'),
    'weifeng': (BASE + 'brands/weifeng/index.html', '微风网络的套餐与线路资料'),
    'firefly': (BASE + 'brands/firefly/index.html', 'Firefly 的套餐与协议资料'),
}
# Every description explains the dependency, rather than repeating link titles.
PROFILES = {
 'ai-start': ('AI 网站打不开？按这个顺序继续看', '先查连接与具体报错。确认是网络服务的问题以后，再比较品牌。', [('ai','如果 Grok 打不开，先按文章里的步骤核对报错与访问条件。'),('status','记录网页请求是否完成，帮助区分连接失败与应用提示。'),('brands','需要调整网络服务时，核对主推品牌的套餐、线路与设备条件。')]),
 'overview': ('从需求开始，把选购、配置与验证接起来', '先明确设备和用途，再核对套餐；能够连接以后，还需要确认隐私设置与实际任务表现。', [('brands','先比较流量、计费周期与线路资料，再决定哪一项值得进一步核对。'),('client','品牌提供订阅，客户端负责读取配置，两者需要匹配。'),('privacy','连接成功之后，继续检查订阅保管、DNS 和浏览器的暴露范围。')]),
 'brand': ('看完品牌资料，购买和使用前还要核对什么？', '套餐表解决价格与用量问题；线路名称不能替代配置验证，也不能单独证明隐私保护。', [('protocol','分清 IPLC/IEPL 线路与 VLESS、Trojan 等协议，避免按名称推断全部兼容性。'),('api','拿到配置后先查格式，再理解 DNS 和 WebRTC 的测试边界。'),('privacy','订阅链接相当于访问凭据，继续了解转换服务、出口 IP 和浏览器隐私。'),('client','按自己的系统核对客户端来源和导入方式，别照搬另一种设备的教程。')]),
 'buy': ('决定套餐之前，把需求与使用成本核对完整', '价格只是起点。设备兼容、每月流量、测试条件和订阅保管，都会影响购买后的使用体验。', [('quota','按视频、AI、下载等任务估算流量，结合倍率和重置周期再看套餐。'),('catalog','回到完整品牌资料，核对套餐条件和实际提供的配置。'),('privacy','购买后不要公开订阅链接；了解第三方转换会接触哪些信息。')]),
 'client': ('软件装好之后，继续核对配置、分流和隐私', '客户端安装成功不代表订阅能够解析，也不代表所有应用已经经过代理。', [('api','用配置检查区分 YAML 结构错误与运行时连接失败。'),('rules','先理解规则与全局模式，按应用任务验证实际出口。'),('privacy','系统代理和 TUN 的覆盖范围不同，要结合 DNS 与浏览器实测。'),('brands','客户端不是节点服务；需要订阅时按格式与用途核对品牌资料。')]),
 'connection': ('从连接问题继续定位到网络层和配置层', '先保留报错与日志，再做同节点、不同网络或不同应用的对照；一次只改变一个条件。', [('status','记录目标请求是否完成与耗时，作为对照证据，而不是解锁结论。'),('gfw','判断是否只有特定网络、协议或时段失败，避免把全部超时直接归因于封锁。'),('api','核对配置结构与订阅格式，区分配置没有加载和节点无法建立连接。')]),
 'dns': ('DNS 排查完成后，还需要验证哪些地方？', '域名解析、代理路由和浏览器设置是不同环节，修改一项以后还要复测原来的任务。', [('protocol','理解 DNS、DoH 与代理协议的分工，知道加密解析解决哪一段问题。'),('privacy','核对解析器和 WebRTC 候选地址，避免把单次测试当作全部应用的隐私保证。'),('status','复测同一目标，保留修改前后的结果。')]),
 'protocol': ('从协议原理走到配置与实际选购', '理解协议以后，要核对客户端版本、传输条件和品牌提供的实际订阅；协议名称不是可用性保证。', [('hy2','用 Hysteria2 的例子理解协议支持与 UDP 网络条件。'),('api','核对配置字段和格式，解析通过后再看客户端日志。'),('gfw','出现超时后用网络对照定位，不凭协议名字推断是否被封锁。'),('brands','带着协议、设备与线路需求回到主推品牌资料，逐项核对。')]),
 'privacy': ('隐私检查之后，把配置证据和故障原因对上', '先知道信息流向谁，再决定使用哪种工具。测试结果应结合当前网络、客户端和浏览器解释。', [('api','查看本地配置检查、第三方订阅转换与 WebRTC 测试各自的边界。'),('dns','DNS 解析失败时按步骤查原因，不用“隐私泄漏”代替具体诊断。'),('protocol','区分加密传输、线路类型和流量接管，理解各自保护的范围。'),('brands','返回品牌资料核对服务条件；价格和专线标注都不能替代隐私验证。')]),
 'api': ('配置与测试做完，如何解释结果？', '工具负责收集有限的证据。没有收集到候选地址、YAML 能解析或网页请求完成，都不等于所有隐私与连接问题已经解决。', [('privacy','先确认订阅凭据、第三方服务与测试地址的暴露范围。'),('client','格式正确仍无法导入时，核对平台、内核版本与协议支持。'),('gfw','格式正常但连接失败时，继续做网络、节点与时段对照。'),('brands','确认需要调整服务后，再比较实际线路与套餐条件。')]),
 'gfw': ('有了故障记录，再决定下一步', '同一症状可能来自服务故障、DNS、网络路径或访问限制。记录比一张固定的协议“健康度”图更有用。', [('timeout','全部节点超时时先查订阅、配额与本地网络。'),('protocol','进一步理解传输层、协议与线路，明确对照哪些变量。'),('privacy','分享日志前去掉订阅 URL、token、密码和个人地址。'),('brands','确认服务侧问题后再比较备用品牌，避免盲目换购。')]),
 'status': ('把请求结果放回实际使用场景', '这里的耗时属于浏览器请求，不是线路带宽、ICMP 延迟或账户解锁证明；需要结合目标应用复测。', [('gfw','失败时区分本地网络、目标服务与访问限制。'),('ai','网页能够请求但 AI 仍不能使用时，继续检查平台报错与账号条件。'),('brands','比较品牌时保存同时间、同设备、同任务的测试结果。')]),
 'tools': ('知道数据含义以后，再用结果定位问题', 'Base64 是编码；IP 归属查询是第三方返回的信息。两者都不能单独证明节点安全或目标平台可用。', [('privacy','了解查询服务收到的信息，保管好解码后的节点凭据。'),('api','从编码内容继续核对配置结构，优先使用品牌提供的原生订阅。'),('brands','把出口和使用需求带回品牌资料，核对服务条件。')]),
 'ai': ('AI 使用问题还关联哪些配置与品牌条件？', '先区分访问失败、平台提示、账号条件和用量问题，再考虑更换节点或套餐。', [('status','用请求结果辅助判断连通性，不能据此推断账户权限。'),('rules','检查目标域名是否经过预期规则，验证实际出口。'),('weifeng','把当前 AI 任务与品牌资料对照，实际可用性仍需用自己的任务验证。'),('firefly','继续比较其他配置与套餐，避免只看宣传中的解锁标签。')]),
 'ip': ('看懂出口 IP 后，继续检查路由和隐私', '归属标签和平台判定可能不同，同一 IP 的结果也受时间与任务影响。', [('tools','查看当前出口与归属查询，并留意查询请求会到第三方服务。'),('privacy','检查浏览器与 DNS 的信息流向，出口改变并不等于完全匿名。'),('brands','按目标用途核对品牌提供的线路与测试条件。')]),
 'mac': ('Mac 配置之后，验证路由与兼容性', '先确认软件来源、系统版本和配置支持，再验证浏览器以外的应用是否按预期连接。', [('mac','核对 Mac 客户端选择，区分旧项目名称与当前开发者版本。'),('api','检查配置结构，避免把语法错误当成品牌节点失效。'),('privacy','理解 TUN、DNS 与浏览器测试的范围，不凭模式名称判断安全。')]),
}

def choose(path, text):
    relative = path.relative_to(ROOT).as_posix()
    if relative == 'topic/ai/index.html':
        return 'ai-start'
    exact = {'api.html':'api','tools.html':'tools','status.html':'status','clients.html':'client', SEC+'index.html':'overview',SEC+'privacy.html':'privacy',SEC+'gfw-monitor.html':'gfw',SEC+'protocols.html':'protocol'}
    if relative in exact:
        return exact[relative]
    if relative.startswith(SEC+'protocols/'):
        return 'dns' if path.stem == '9' else 'protocol'
    if relative in ('brands.html',BASE+'index.html',BASE+'brands/index.html'):
        return 'brand'
    if re.fullmatch(re.escape(BASE)+r'brands/[^/]+/index.html',relative):
        return 'brand'
    heading = re.search(r'<h1\b[^>]*>(.*?)</h1>', text, re.S|re.I)
    title = re.sub('<[^>]+>', '', heading.group(1)) if heading else ''
    question = re.search(r'<h[23]\b[^>]*class="faq-q"[^>]*>(.*?)</h[23]>',text,re.S|re.I)
    if question:
        title = re.sub('<[^>]+>', '', question.group(1))
    source = ROOT/BASE/'faq/faq-articles.json'
    if not hasattr(choose, 'categories'):
        choose.categories = {(source.parent/a['url']).resolve(): a['category'] for a in json.loads(source.read_text(encoding='utf-8'))}
    cat = choose.categories.get(path, '')
    if re.search(r'DNS|DoH|解析失败',title,re.I): return 'dns'
    if re.search(r'隐私|泄漏|审计|分享订阅',title): return 'privacy'
    if re.search(r'ChatGPT|GPT|Grok|AI|人工智能',title,re.I) or cat == 'ai': return 'ai'
    if re.search(r'超时|timeout|连接失败|打不开|断线|连不上',title,re.I) or cat in ('connection','outage','latency','speed','congestion'): return 'connection'
    if re.search(r'Mac|macOS',title,re.I): return 'mac'
    if re.search(r'IPLC|IEPL|Hysteria|Trojan|VLESS|VMess|协议|专线|中转',title,re.I) or cat in ('concept','line','selfhost'): return 'protocol'
    if cat in ('ip','region') or re.search(r'原生 IP|住宅 IP|出口 IP',title): return 'ip'
    if cat in ('quota','reset','multiplier','billing','price','coupon','trial','select') or re.search(r'套餐|流量|优惠|多少钱|月付|年付|试用|退款|付款|支付',title): return 'buy'
    if cat in ('start','subscription','import','client','importfail','compat') or re.search(r'Clash|TUN|客户端|导入|订阅|sing.?box',title,re.I): return 'client'
    if relative.startswith(BASE+'brands/'): return 'brand'
    if relative.startswith(SEC): return 'protocol'
    return 'overview'

def add_content_paths(text, path):
    path = Path(path).resolve()
    if path.name in ('test_old.html','test_curr.html') or re.search(r'<meta[^>]+http-equiv=["\']refresh',text,re.I):
        return text
    text = re.sub(r'<!-- Contextual reading assets -->.*?<!-- End contextual reading assets -->\s*', '', text, flags=re.S)
    text = re.sub(r'<!-- Contextual reading path -->.*?<!-- End contextual reading path -->\s*', '', text, flags=re.S)
    text = re.sub(r'<!-- Brand verification context -->.*?<!-- End brand verification context -->\s*', '', text, flags=re.S)
    # The home page already has topic and tool navigation; keep its footer concise.
    if path == ROOT / 'index.html':
        return text
    profile = choose(path,text)
    title,intro,entries = PROFILES[profile]
    def link(target): return html.escape(Path(os.path.relpath(ROOT/target,path.parent)).as_posix(),quote=True)
    cards = []
    for key,reason in entries:
        target,label = DEST[key]
        if (ROOT/target).resolve() == path: continue
        cards.append(f'<div class="content-path-card"><a href="{link(target)}">{html.escape(label)} →</a><p>{html.escape(reason)}</p></div>')
    block = f'<!-- Contextual reading path -->\n<section class="content-paths" id="continue-reading" data-reading-profile="{profile}" aria-labelledby="continue-reading-title"><p class="content-path-kicker">把这个问题与下一步接起来</p><h2 id="continue-reading-title">{title}</h2><p>{intro}</p><div class="content-path-grid">'+''.join(cards)+'</div></section>\n<!-- End contextual reading path -->\n'
    assets = f'<!-- Contextual reading assets -->\n<link rel="stylesheet" href="{link("css/content-paths.css")}?v=20261010-3">\n<!-- End contextual reading assets -->\n'
    text = text.replace('</head>', assets+'</head>',1)
    relative = path.relative_to(ROOT).as_posix()
    if re.fullmatch(re.escape(BASE)+r'brands/[^/]+/index.html', relative):
        text = text.replace('<main class="catalog">','<main class="catalog" data-brand-reading>',1)
        # Place the connection beside service facts, before the longer review.
        service = re.search(r'<h2>服务资料</h2>\s*<ul>.*?</ul>', text, re.S)
        if service:
            facts = re.sub('<[^>]+>', '', service.group())
            chapter = SEC+'protocols/5.html' if re.search('IPLC|IEPL',facts,re.I) else SEC+'protocols.html'
            label = '专线与共享套餐的区别' if chapter.endswith('/5.html') else '协议与线路的区别'
            context = '<!-- Brand verification context -->\n<aside class="guide-note reading-guide" aria-label="把品牌资料与配置隐私核对起来"><p>这些服务资料可以帮助比较套餐，但还要核对设备上的表现。先看 <a href="'+link(chapter)+'">'+label+'</a>，再用 <a href="'+link('api.html')+'">配置检查</a>理解格式与测试结果；连接成功以后，继续检查 <a href="'+link(SEC+'privacy.html')+'">订阅保管、DNS 和浏览器隐私</a>。</p></aside>\n<!-- End brand verification context -->\n'
            text = text[:service.end()]+context+text[service.end():]
    # Keep paths inside content, before related FAQs or the end of the main article.
    if relative == 'topic/index.html':
        text = text.replace('<!-- Topic reading next steps -->',block+'<!-- Topic reading next steps -->',1) if '<!-- Topic reading next steps -->' in text else text.replace('</main>',block+'</main>',1)
    elif relative == 'topic/ai/index.html':
        text = text.replace('<!-- AI access next steps -->',block+'<!-- AI access next steps -->',1) if '<!-- AI access next steps -->' in text else text.replace('</main>',block+'</main>',1)
    elif '<section class="faq-reading">' in text:
        text = text.replace('<section class="faq-reading">',block+'<section class="faq-reading">',1)
    elif question := re.search(r'<h[23]\b[^>]*class="faq-q"',text):
        pagination = re.search(r'<div class="pagination">',text)
        if pagination:
            text = text[:pagination.start()]+block+text[pagination.start():]
        else:
            text = text.replace('</article>',block+'</article>',1)
    elif re.search(r'<article\b[^>]*class="brand-card"', text):
        grid = re.search(r'<section\b[^>]*class="brand-grid"[^>]*>',text)
        if grid:
            text = text[:grid.start()]+block+text[grid.start():]
        else:
            text = text.replace('</main>',block+'</main>',1)
    elif '</article>' in text:
        text = text.replace('</article>',block+'</article>',1)
    elif '</main>' in text:
        text = text.replace('</main>',block+'</main>',1)
    else:
        position = text.find('<!-- Shared floating navigation -->')
        if position < 0: position = text.find('</body>')
        text = text[:position]+block+text[position:]
    return text
