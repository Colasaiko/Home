/**
 * 本地预置/备用极客与前沿网络情报库 (保证任何网络状况下100%秒开)
 */
const curatedNewsData = [
    {
        source: "AI前沿情报",
        tagClass: "tag-ai",
        title: "OpenAI GPT-5 及海外大模型 API 访问风控机制收紧，数据中心 IP 遭遇大面积降权",
        link: "topic/tuijianjichang/index.html",
        pubDate: "2026-10-15T08:30:00Z",
        description: "近期 OpenAI 与 Anthropic 再次升级了客户端登录与 API 调用风控系统。大量廉价公网 VPS 与通用数据中心 IP 出现无法登录、无限循环人机验证（Cloudflare Turnstile）或封号风险。行业专家建议使用纯净原生家庭宽带（Residential IP）或经过 BGP 专线优化的固定出口节点访问以保障账号安全。"
    },
    {
        source: "骨干网动态",
        tagClass: "tag-network",
        title: "全国跨境专线 IEPL / IPLC 迎来全链路带宽扩容，晚高峰抖动率降至 0.3% 以下",
        link: "brands.html",
        pubDate: "2026-10-14T19:20:00Z",
        description: "为应对国际出口高峰期流量拥堵，顶级机场服务商全面完成 2026 沪日、深港及京德跨境内网专线节点升级。实测表明，采用内网传输技术后，完全绕开公网 GFW 审查与 QoS 限速，4K/8K 视频加载无缓冲，游戏联机延迟保持在 30ms 以内极稳水准。"
    },
    {
        source: "流媒体解锁",
        tagClass: "tag-network",
        title: "Netflix 与 Disney+ 启用新一轮住宅 IP 校验，非原生代理节点遭遇区域锁定",
        link: "topic/tuijianjichang/comparison.html",
        pubDate: "2026-10-13T14:45:00Z",
        description: "流媒体巨头 Netflix 近日对东亚与北美节点启动更严苛的 ASN 类型检测，普通广播 IP 仅能观看自制剧。目前微风网络、飞猫云等头部大厂已率先部署专属 DNS 分流与双 ISP 静态住宅节点，实现日区、美区、港区及台区全片库 100% 完美解锁。"
    },
    {
        source: "网络安全",
        tagClass: "tag-security",
        title: "最新浏览器 WebRTC 与 DNS 泄漏防范指南：如何彻底杜绝真实 IP 暴露",
        link: "topic/cybersecurity/privacy.html",
        pubDate: "2026-10-12T11:15:00Z",
        description: "网络安全实验室最新通报，部分现代浏览器即使开启全局代理，仍可能通过 STUN 协议的 WebRTC 请求泄露内网与公网真实 IP。站长建议在客户端开启 Fake-IP 模式并配置 strict-route，配合系统全局 DoH/DoT 加密 DNS，从根本上杜绝 DNS 劫持与流量指纹识别。"
    },
    {
        source: "极客社区",
        tagClass: "tag-gcores",
        title: "新一代代理协议 Hysteria 2 与 TUIC v5 架构深度解析：弱网对抗与高丢包抢跑机制",
        link: "clients.html",
        pubDate: "2026-10-11T16:00:00Z",
        description: "基于标准 QUIC/UDP 开发的 Hysteria 2 与 TUIC 协议在 2026 年已成为主流客户端的标配。在跨国高延迟（>200ms）或恶劣丢包（30%+）环境下，其独创的拥塞控制算法相比传统 TCP 伪装协议可提升高达 300% 的下载吞吐速度。"
    },
    {
        source: "数码生活",
        tagClass: "tag-sspai",
        title: "打造全屋极速漫游：家庭软路由搭配透明代理与分流规则最佳实践",
        link: "tools.html",
        pubDate: "2026-10-10T10:20:00Z",
        description: "在软路由（OpenWrt/iStoreOS）上部署 mihomo 内核，结合 GeoSite 与 GeoIP 规则实现智能国内直连、海外专线走加速器，不仅全屋电视盒子、PS5、Switch 和手机无需单独配置客户端，还能显著降低家庭网络功耗与延迟。"
    }
];

if (typeof window !== 'undefined') {
    window.curatedNewsData = curatedNewsData;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = curatedNewsData;
}
