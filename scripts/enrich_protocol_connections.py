"""Editorial companion to the shared reading paths; run before site_navigation.py."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = {
'5': '''<article class="panel reading-guide"><h1>IPLC/IEPL 专线：线路形态、共享套餐与选购验证</h1>
<p>品牌资料中的“专线”描述网络服务或线路安排，与客户端使用的 SS、VLESS、Trojan 等协议不是同一层概念。理解这个区别，才能避免从线路名称推断隐私、速度或兼容性。</p>
<nav aria-label="专线阅读目录"><a href="#line-concept">线路概念</a> · <a href="#line-check">五步核对</a> · <a href="#line-result">实际验证</a></nav>
<section id="line-concept"><h2>为什么专线标签不能直接当作性能承诺？</h2>
<p>IPLC 指国际私用出租线路，IEPL 指国际以太网专线。企业专线产品一般描述特定地点之间的连接与约定服务条件；机场零售套餐则还涉及共享带宽、入口、出口、调度和计费。专线产品的约定并不会自动成为每位套餐用户的独享带宽。</p>
<p>一条完整连接还包括用户到入口、跨境段、出口到目标等环节。即使其中一段采用专线，也不能据此保证其他环节永远不拥堵、不故障，或整条通信无法被观察。</p></section>
<section id="line-check"><h2>怎样把专线资料带入选购？</h2><ol>
<li><strong>确认描述的环节。</strong>问清品牌的线路资料是在描述入口、跨境段还是全程，不把节点地区当作线路证明。</li>
<li><strong>确认套餐条件。</strong>看流量、倍率、重置、设备限制、限速和共享使用条件，再按照 <a href="../../../FAQ/MonthlyAirportTraffic.html">每月流量估算</a>比较价格。</li>
<li><strong>确认协议与格式。</strong>查看当前订阅里实际提供的协议，核对 <a href="../../../clients.html">客户端版本支持</a>。专线服务不等于所有客户端都兼容。</li>
<li><strong>核对配置与隐私。</strong>通过 <a href="../../../api.html">配置检查</a>理解格式，随后按照 <a href="../privacy.html">隐私检查</a>确认订阅保管、DNS 与应用路由。</li>
<li><strong>做同条件任务测试。</strong>在自己的网络和常用时段测试目标应用，记录失败或耗时。出现问题继续看 <a href="../gfw-monitor.html">故障对照流程</a>。</li>
</ol></section>
<section id="line-result"><h2>如何回到品牌资料继续比较？</h2>
<p><a href="../../tuijianjichang/brands/weifeng/index.html">微风网络</a> 的线路和套餐资料可作为核对入口；再与 <a href="../../tuijianjichang/index.html">主推品牌页</a>上的其他服务逐项比较。资料里的线路标注需要结合实际提供的服务与自己的任务验证，不能推导为完全匿名或永不失联。</p>
<p>可查看运营商如何定义企业线路：<a href="https://international.bt.com/products-services/secure-connectivity/ethernet-access" target="_blank" rel="noopener noreferrer">BT：Global Ethernet 与点到点连接产品</a>。该资料说明企业产品形态，不是本站品牌的线路证明。</p></section></article>''',
'9': '''<article class="panel reading-guide"><h1>DNS、DoH 与代理路由：理解解析，再定位问题</h1>
<p>DNS 把域名解析为地址；DoH 使用 HTTPS 传送 DNS 请求。解析方式、应用代理路由和访问目标是不同环节。了解它们的分工，才能判断“打不开”发生在哪里。</p>
<nav aria-label="DNS 阅读目录"><a href="#dns-scope">DoH 的范围</a> · <a href="#dns-check">六步检查</a> · <a href="#dns-next">复测与记录</a></nav>
<section id="dns-scope"><h2>为什么改成 DoH 后仍可能无法访问？</h2>
<p>DoH 保护的是客户端到所选解析服务之间的 DNS 传输。它不会自动把其他应用流量送进代理，也不会隐藏所有连接元数据。解析服务仍要处理查询，解析服务是否可达与返回地址是否适用也需要核对。</p>
<p>Fake-IP 是部分代理客户端使用的映射机制，不是另一种加密 DNS 协议。DNS、规则、TUN 与浏览器设置互相影响，配置必须按实际客户端版本确认，不能直接复制陌生示例覆盖全部设置。</p></section>
<section id="dns-check"><h2>如何从 DNS 报错逐步处理？</h2><ol>
<li><strong>记录失败目标与原始报错。</strong>区分解析失败、连接超时和平台拒绝，先查看 <a href="../../../FAQ/ClashDNSFailed.html">DNS 排查 FAQ</a>。</li>
<li><strong>确认当前解析路径。</strong>分别记录系统、浏览器与客户端的 DNS 设置，确定哪个环节处理这个应用的查询。</li>
<li><strong>确认解析服务可达。</strong>解析器地址写对不等于请求可以到达。结合日志查看上游连接是否失败。</li>
<li><strong>核对路由与规则。</strong>域名解析成功后仍需连接目标；通过 <a href="../../../FAQ/ClashRulesVsGlobal.html">规则与全局模式说明</a>确认请求走向。</li>
<li><strong>一次调整一项并复测。</strong>保留原配置，使用同一目标观察变化；需要结构检查时进入 <a href="../../../api.html">配置检测</a>。</li>
<li><strong>解释外部测试结果。</strong>测试返回解析器信息仅反映当次条件，按照 <a href="../privacy.html">隐私指南</a>核对浏览器与客户端范围。</li>
</ol></section>
<section id="dns-next"><h2>结果要怎样与品牌和网络条件对上？</h2>
<p>解析正常但连接失败时，继续做 <a href="../gfw-monitor.html">网络和节点对照</a>。需要调整服务时回到 <a href="../../tuijianjichang/index.html">品牌比较</a>核对订阅、客户端和线路条件，换套餐不能自动修复设备上的 DNS 设置。</p>
<p>协议与隐私范围可进一步核对 <a href="https://www.rfc-editor.org/rfc/rfc8484" target="_blank" rel="noopener noreferrer">IETF RFC 8484：DNS over HTTPS</a> 与 <a href="https://www.rfc-editor.org/rfc/rfc9076.html" target="_blank" rel="noopener noreferrer">RFC 9076：DNS 隐私考虑</a>。</p></section></article>''',
}

def main():
    for chapter,article in CHAPTERS.items():
        path = ROOT/f'topic/cybersecurity/protocols/{chapter}.html'
        text = path.read_text(encoding='utf-8')
        text,count = re.subn(r'<article\b[^>]*>.*?</article>',lambda m:article,text,count=1,flags=re.S)
        assert count == 1
        title = re.search(r'<h1>(.*?)</h1>',article).group(1)
        text = re.sub(r'<title>.*?</title>',lambda m:f'<title>{title} | Cola 站长</title>',text,count=1,flags=re.S)
        path.write_text(text,encoding='utf-8')
    path = ROOT/'topic/cybersecurity/protocols.html'
    text = path.read_text(encoding='utf-8').replace('IPLC/IEPL 专线科普：为什么它们不怕 GFW？','IPLC/IEPL 专线：线路形态、共享套餐与选购验证')
    # Keep the index excerpt consistent with the final chapter.
    for chapter,desc in [('5','专线产品与机场共享套餐如何区分？核对线路环节、计费、协议兼容与同条件测试。'),('9','DoH 加密的是解析请求。按 DNS、规则与应用路由逐步检查，不把解析设置当作全部隐私保证。')]:
        text = re.sub(r'(<a href="protocols/'+chapter+r'.html"[^>]*>.*?<span class="protocol-desc">).*?(</span>)',lambda m:m.group(1)+desc+m.group(2),text,count=1,flags=re.S)
    path.write_text(text,encoding='utf-8')
    for name in ('brands.html','tools.html','status.html','api.html'):
        path = ROOT/name
        text = path.read_text(encoding='utf-8')
        if name == 'brands.html':
            text = re.sub(r'<p>为了帮您避坑.*?</p>','<p>这里展示实际品牌资料入口。先核对设备、用量与计费条件，再阅读配置和隐私指南；线路名称和一次测试都不能保证所有目标平台长期可用。</p>',text,count=1,flags=re.S)
            text = text.replace('🚀 拒绝失联，精选全网最稳定、性价比极高的科学上网服务','从套餐、设备与用途出发，比较实际品牌资料')
        if name == 'tools.html':
            text = text.replace('极客工具箱 - 纯前端安全网络工具','极客工具箱 - IP 查询与 Base64 编解码').replace('解锁密文 (Decode)','解码文本 (Decode)')
            text = text.replace("resultBox.innerHTML = '<strong style=\"color:#4facfe;\">解码成功：</strong>\\n\\n' + decoded;", "resultBox.textContent = '解码成功：\\n\\n' + decoded;")
        if name == 'status.html': text = text.replace('实时连通性与真实延迟检测工具','请求结果与网络对照')
        if name == 'api.html': text = text.replace('智能订阅转换 API - 节点分流规则定制','配置检查与订阅转换 - API 工具及测试说明')
        path.write_text(text,encoding='utf-8')
    print('Updated protocol chapters 5/9, index excerpts and utility labels.')

if __name__ == '__main__': main()
