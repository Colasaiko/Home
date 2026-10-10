"""One-time editorial update for the network topic hubs. Existing files are backed up."""
from pathlib import Path
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]

PRIVACY = '''<article class="panel reading-guide">
<h1>机场隐私与防泄漏：从订阅保管到实际验证</h1>
<p>购买套餐只解决访问服务的条件。订阅凭据、客户端接管范围、域名解析和浏览器通信仍需要分别检查。这里帮助你判断信息流向谁，以及一个测试结果能说明什么。</p>
<nav aria-label="隐私检查目录"><a href="#data-flow">信息流向</a> · <a href="#privacy-steps">六步检查</a> · <a href="#privacy-record">结果与记录</a></nav>
<section id="data-flow"><h2>为什么连接成功以后，还要检查隐私？</h2>
<p>代理出口改变，不代表设备完全匿名。HTTPS 保护的是客户端与目标服务之间的加密通信；服务提供者仍可能接触连接元数据，目标平台仍有账号、会话和风控规则。线路标注、价格与宣传中的“无日志”也不能由本页工具独立验证。</p>
<div class="table-scroll"><table><caption>本站工具与信息接收方</caption><thead><tr><th>操作</th><th>信息流向</th><th>结果的边界</th></tr></thead><tbody>
<tr><td>YAML 检查、Base64 编解码</td><td>输入由本页浏览器脚本处理</td><td>格式检查不验证服务安全；解码后可能包含节点密码</td></tr>
<tr><td>使用生成的订阅转换链接</td><td>原订阅 URL 会随转换请求传给 api.v1.mk</td><td>生成链接与实际打开链接不同；优先使用服务原生格式</td></tr>
<tr><td>WebRTC 候选地址测试</td><td>浏览器会联系配置的 STUN 服务</td><td>候选地址不是自动认定的真实宽带地址；空结果也不能证明没有泄漏</td></tr>
<tr><td>出口 IP 查询、外部 DNS 测试</td><td>查询或访问会到第三方服务</td><td>归属、解析器与平台识别结果可能不同</td></tr>
</tbody></table></div>
<p>工具入口是 <a href="../../api.html">配置检查与隐私测试</a> 和 <a href="../../tools.html">IP / Base64 工具箱</a>。先了解数据流向，再决定是否提交内容。</p></section>
<section id="privacy-steps"><h2>如何按顺序检查？</h2><ol>
<li><strong>确认客户端来源与配置格式。</strong>核对开发者渠道、系统版本和服务提供的订阅类型。遇到导入问题，先看 <a href="../../clients.html">客户端选择</a>，再做本地格式检查。</li>
<li><strong>保管订阅凭据。</strong>不公开订阅 URL、token、节点密码或带凭据的二维码。泄漏以后使用服务后台提供的重置方式，并更新自己的设备。转换服务会接触原订阅，不把陌生转换站当作默认必需步骤。</li>
<li><strong>确认应用走哪条路。</strong>系统代理、规则模式和 TUN 的覆盖范围不同。分别验证浏览器和实际应用，结合日志看命中的规则；不要只凭“开启 TUN”判断全部通信已接管。</li>
<li><strong>核对 DNS。</strong>记录客户端 DNS 配置、浏览器安全 DNS 设置及测试返回的解析器。DoH 加密解析请求，不等于所有流量都经过代理；无法解析时按照 <a href="../../FAQ/ClashDNSFailed.html">DNS 故障步骤</a>处理。</li>
<li><strong>解释 WebRTC 结果。</strong>区分私有地址、代理出口和自己已知的公网地址。浏览器权限与网络条件会影响候选收集；没有结果只能说明这次没有收集到证据。</li>
<li><strong>回到实际任务复测。</strong>对照同设备、同时间、同目标的结果，确认修改后的行为。遇到请求失败，继续看 <a href="gfw-monitor.html">网络与节点故障判断</a>，不要用“泄漏”概括所有错误。</li>
</ol></section>
<section id="privacy-record"><h2>完成后留下什么记录？</h2>
<p>保存系统与客户端版本、模式、目标、错误类型、测试时间和修改前后的结果。向别人求助时隐藏凭据与个人地址。下面的清单用于提示遗漏，不是安全评分或匿名证明。</p>
<label><input type="checkbox"> 已确认客户端来源，并记录实际订阅格式</label>
<label><input type="checkbox"> 已保管或重置暴露的订阅凭据</label>
<label><input type="checkbox"> 已验证实际应用的出口与 DNS，而不只看客户端开关</label>
<label><input type="checkbox"> 已解释测试边界，并保留脱敏的对照记录</label>
<p>如果你正在比较 <a href="../tuijianjichang/brands/weifeng/index.html">微风网络</a> 或 <a href="../tuijianjichang/brands/firefly/index.html">Firefly</a>，可以把套餐和协议资料带入这套检查流程。品牌页描述服务条件，这里的验证解释设备与浏览器行为；两部分需要一起看。</p></section>
<h2>继续核对原理</h2><ul>
<li><a href="https://www.rfc-editor.org/rfc/rfc8446" target="_blank" rel="noopener noreferrer">IETF：TLS 1.3 标准</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/address" target="_blank" rel="noopener noreferrer">MDN：WebRTC 候选地址与隐私</a></li>
</ul></article>'''

GFW = '''<article class="panel reading-guide">
<h1>GFW 与节点故障判断：从 DNS、超时到网络对照</h1>
<p>节点打不开，可能涉及域名解析、服务状态、协议兼容、路径限制或目标平台。这个页面提供故障分析流程与公开研究入口，不提供实时监测数据，也不把协议名称换算成固定存活率。</p>
<nav aria-label="故障判断目录"><a href="#gfw-evidence">先收集证据</a> · <a href="#gfw-steps">逐步排查</a> · <a href="#gfw-research">公开研究</a></nav>
<section id="gfw-evidence"><h2>为什么不能看到 timeout 就认定被封锁？</h2>
<p>一次超时只能说明请求未在期限内完成。配额用尽、服务维护、UDP 不通、DNS 失败或客户端配置错误都可能表现相似。判断需要明确失败环节，并与其他条件对照。</p>
<div class="table-scroll"><table><thead><tr><th>观察到的现象</th><th>优先检查</th><th>下一步阅读</th></tr></thead><tbody>
<tr><td>全部节点超时</td><td>订阅是否更新、配额、设备网络、服务公告</td><td><a href="../../FAQ/ClashVergeAllTimeout.html">Clash 全部超时</a></td></tr>
<tr><td>域名解析失败</td><td>客户端日志、DNS 设置、同域名对照</td><td><a href="../../FAQ/ClashDNSFailed.html">DNS 排查</a></td></tr>
<tr><td>仅某个协议或网络失败</td><td>版本支持、TCP/UDP、网络路径差异</td><td><a href="protocols.html">协议与传输原理</a></td></tr>
<tr><td>网页能开，但 AI 提示拒绝</td><td>平台报错、账号、地区条件、实际出口</td><td><a href="../../FAQ/GrokNotOpening.html">AI 访问问题</a></td></tr>
</tbody></table></div></section>
<section id="gfw-steps"><h2>如何按证据逐步排查？</h2><ol>
<li><strong>记录问题边界。</strong>写下时间、网络运营商、系统和客户端版本、节点协议、失败目标及原始报错。隐藏密码和订阅凭据。</li>
<li><strong>检查服务与配置。</strong>核对后台状态、配额和公告，确认配置已经加载。需要结构检查时进入 <a href="../../api.html">配置检测工具</a>；语法正常仍要看运行日志。</li>
<li><strong>区分解析与连接。</strong>DNS 失败和连接超时分开记录。DoH、TLS、UDP 和专线各自处理不同环节，不能互相替代。</li>
<li><strong>只改变一个条件做对照。</strong>同设备同节点切换允许使用的网络，或同网络对比另一条节点。不要同时重装客户端、改 DNS 和换套餐，否则无法知道哪个变化有效。</li>
<li><strong>复测同一任务。</strong>用 <a href="../../status.html">浏览器连通性检查</a>辅助记录请求，再回到原应用确认。浏览器请求完成不代表 AI 账号权限或所有应用可用。</li>
<li><strong>依据结果采取下一步。</strong>本地问题继续排配置；服务侧问题向服务方提供脱敏记录。确需备用服务时再看 <a href="../tuijianjichang/index.html">主推品牌比较</a>，按自己的设备和时段测试。</li>
</ol><p class="guide-note">IPLC/IEPL 描述线路形态，协议描述通信方式。任何名称都不能单独保证连接永远可用、不可观察或完全匿名。</p></section>
<section id="gfw-research"><h2>如何阅读公开研究与测量？</h2>
<p>看清测量日期、地点、网络、测试方法与失败环节。研究发现适用于其测量条件，不能直接推断今天某个品牌的全部节点。OONI 的异常需要进一步核对，不能把单条异常当作最终封锁结论。</p><ul>
<li><a href="https://labs.ooni.io/nettest/web-connectivity/" target="_blank" rel="noopener noreferrer">OONI：Web Connectivity 的 DNS、连接与网页测试方法</a></li>
<li><a href="https://ooni.org/support/interpreting-ooni-data/" target="_blank" rel="noopener noreferrer">OONI：如何解释异常和测量数据</a></li>
<li><a href="https://www.usenix.org/conference/usenixsecurity25/presentation/zohaib" target="_blank" rel="noopener noreferrer">USENIX Security 2025：QUIC 相关网络审查研究</a></li>
</ul><p>使用第三方测量工具前了解其数据收集范围；本站没有替你运行外部测量。</p></section></article>'''

ARTICLES = {
'api.html': '''<article class="seo-article reading-guide"><h2>先检查配置，再解释连接与隐私结果</h2><p>这里提供订阅转换链接生成、浏览器内 YAML 检查、WebRTC 候选地址收集和外部 DNS 测试入口。它们解决不同问题，不能合并为一个品牌安全分数。</p><ol><li>优先使用品牌提供的原生订阅，格式不兼容时先核对 <a href="clients.html">客户端支持</a>。</li><li>使用 YAML 检查确认基础结构；解析通过不保证版本兼容、节点可用或全部规则正确。</li><li>在 <a href="topic/cybersecurity/privacy.html">隐私指南</a>了解测试的数据流向，再选择 DNS 或 WebRTC 检查。</li><li>配置正常但仍失败时，按 <a href="topic/cybersecurity/gfw-monitor.html">故障对照流程</a>定位原因。</li></ol><p>确认服务条件不合适后，再回到 <a href="topic/tuijianjichang/index.html">主推品牌资料</a>比较线路和套餐。</p></article>''',
'tools.html': '''<article class="seo-article reading-guide"><h2>先知道工具处理什么信息</h2><p>Base64 编解码在当前页面的浏览器脚本内完成。Base64 是编码，不是加密；解码后的节点地址、UUID 或密码仍需保管。</p><p>IP 查询会由浏览器向 <code>ipwho.is</code> 发起请求，服务方会收到查询与网络请求信息。归属查询不能证明匿名，也不代表目标平台会采用同一地区或 IP 类型判定。</p><ol><li>查询出口后，结合 <a href="topic/cybersecurity/privacy.html">隐私与 DNS 检查</a>理解结果。</li><li>解析订阅内容后，进入 <a href="api.html">配置结构检查</a>；不公开含凭据的内容。</li><li>比较服务时，回到 <a href="topic/tuijianjichang/brands/index.html">品牌资料库</a>核对条件，并用实际任务测试。</li></ol><p><a href="https://developer.mozilla.org/en-US/docs/Glossary/Base64" target="_blank" rel="noopener noreferrer">MDN：Base64 编码说明</a></p></article>''',
'status.html': '''<article class="seo-article reading-guide"><h2>这个测试可以说明什么？</h2><p>面板记录浏览器发出请求到完成或失败的时间，受 DNS、握手、代理、目标服务与浏览器环境共同影响。它不是 ICMP ping、带宽测速或账户解锁证明。</p><p>请求使用 <code>no-cors</code>，无法读取跨域响应内容和 HTTP 状态。绿色表示请求在较短时间内完成；红色表示请求未完成，需要继续定位。</p><ol><li>记录时间、节点和目标，使用同设备做前后对照。</li><li>失败时继续看 <a href="topic/cybersecurity/gfw-monitor.html">DNS、网络与节点排查</a>。</li><li>请求完成后回到实际应用；AI 报错可参考 <a href="FAQ/GrokNotOpening.html">AI 访问 FAQ</a>。</li><li>比较 <a href="topic/tuijianjichang/index.html">主推品牌</a>时保持任务与时段一致，避免直接按一次耗时排名。</li></ol></article>''',
}

def main():
    targets = list(ARTICLES) + ['topic/cybersecurity/privacy.html','topic/cybersecurity/gfw-monitor.html','brands.html']
    backup = Path(tempfile.mkdtemp(prefix='cross-topic-hubs-before-'))
    for name in targets:
        path = ROOT/name
        saved = backup/name
        saved.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,saved)
        text = path.read_text(encoding='utf-8-sig')
        article = ARTICLES.get(name) or (PRIVACY if name.endswith('privacy.html') else GFW if name.endswith('gfw-monitor.html') else None)
        if article:
            text,count = re.subn(r'<article\b[^>]*>.*?</article>',lambda m:article,text,count=1,flags=re.S)
            assert count == 1, name
        if name == 'api.html':
            text = text.replace('<textarea id="subInput"', '<p style="color:#d5dfeb;line-height:1.7">优先使用原生订阅。点击生成只构造 URL；打开或导入生成的转换链接时，原订阅会传给第三方 api.v1.mk。不要使用公开分享的凭据。</p><textarea id="subInput"')
            text = text.replace('代理受到完美保护。','这次未收集到候选地址，不能据此证明没有泄漏。').replace('您的浏览器禁用了 WebRTC 或未发生泄漏，','')
            text = text.replace('✅ 安全：','检查结果：').replace('探测超时，未发现 WebRTC 泄漏。','探测超时，未完成验证；不能据此判断是否泄漏。')
            text = text.replace('真实宽带的 IP 或局域网 IP，说明您的代理规则可能存在 WebRTC 泄漏漏洞，建议在客户端中开启 Enhanced Mode 或 TUN 模式。','已知的公网地址，请结合客户端路由继续核对。私有地址与候选地址不能直接等同于真实公网出口。')
            text = re.sub(r'即便您开启了全局代理.*?隐私漏洞。','此测试收集 WebRTC 候选地址，并会联系配置的 STUN 服务。请区分私有地址、代理出口与已知的公网地址；空结果不是无泄漏证明。',text)
            text = re.sub(r'真正的 DNS 泄漏探测.*?终极标准。','外部 DNS 测试可帮助观察解析器，但需结合浏览器和客户端设置解释，不能单独证明品牌安全。',text)
            text = text.replace('由于该测试需要庞大的后端算力，我们为您直接对接了全球最权威的两大安全探测机构：','以下测试由第三方服务提供。打开后会向其发起网络请求，请先了解其数据收集说明：')
            text = text.replace('🛡️ 纯前端运行，全面评估与武装您的科学上网环境','配置检查、订阅转换与隐私测试入口')
        if name == 'tools.html':
            text = text.replace('纯前端实现，拒绝隐私泄露','本地编解码与第三方 IP 查询').replace('加解密','编解码').replace('加密','编码').replace('解密','解码')
        if name == 'status.html':
            text = text.replace('在线机场节点测速','浏览器连通性与请求耗时').replace('📡 纯前端真实环境测速工具，一键检测您的机场节点延迟与解锁情况','记录请求结果，结合客户端与实际任务判断')
        if name == 'brands.html':
            matches = list(re.finditer(r'<div class="brand-card">.*?</div>',text,re.S))
            for match,key,label,desc in reversed(list(zip(matches,['weifeng','firefly','wuyou'],['微风网络','Firefly','无忧'],['从线路、流量与计费周期核对服务资料，再验证设备与实际用途。','阅读套餐与协议资料，核对客户端能否读取服务提供的订阅。','查看套餐、客户端与使用条件，选购后按配置和隐私流程验证。']))):
                card = f'<div class="brand-card"><h2>{label}</h2><p>{desc}</p><a href="topic/tuijianjichang/brands/{key}/index.html" class="buy-btn">查看品牌资料 →</a></div>'
                text = text[:match.start()]+card+text[match.end():]
        if name in ('api.html','tools.html','status.html'):
            text = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="'+{'api.html':'订阅格式、配置结构与隐私测试说明，连接客户端、故障排查和品牌资料。','tools.html':'Base64 本地编解码与第三方出口 IP 查询，解释数据流向和结果边界。','status.html':'浏览器连通性与请求耗时检查，结合网络对照和实际应用定位问题。'}[name]+'">',text,count=1)
            if 'name="viewport"' not in text: text = text.replace('</head>','<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>',1)
        if name.endswith('gfw-monitor.html'): text = text.replace('封锁动态与节点存活监控 | Cola 站长','GFW 与节点故障判断 | Cola 站长')
        if name.endswith('privacy.html'): text = text.replace('机场审计规则与隐私揭秘 | Cola 站长','机场隐私与防泄漏检查 | Cola 站长')
        path.write_text(text,encoding='utf-8')
    print(f'Updated {len(targets)} topic hubs. Backup: {backup}')

if __name__ == '__main__': main()
