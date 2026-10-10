import os

base_dir = r"c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\ai"
os.makedirs(base_dir, exist_ok=True)

layout_top = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Cola 站长 AI 极客教程</title>
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="../tuijianjichang/catalog.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    .article-content { max-width: 900px; margin: 40px auto; background: rgba(20,20,20,0.8); padding: 40px; border-radius: 15px; border: 1px solid rgba(155, 89, 182, 0.3); color: #d0d0d0; line-height: 1.8; font-size: 1.05rem; }
    .article-content h2 { color: #e056fd; font-size: 1.8rem; margin-top: 30px; margin-bottom: 20px; border-bottom: 1px solid rgba(224, 86, 253, 0.2); padding-bottom: 10px; }
    .article-content h3 { color: #fff; font-size: 1.3rem; margin-top: 25px; margin-bottom: 15px; }
    .article-content p { margin-bottom: 15px; }
    .article-content ul, .article-content ol { margin-bottom: 20px; padding-left: 20px; }
    .article-content li { margin-bottom: 10px; }
    .article-content strong { color: #fff; }
    .promo-box { background: rgba(243, 156, 18, 0.1); border-left: 4px solid #f39c12; padding: 20px; margin: 30px 0; border-radius: 0 8px 8px 0; }
    .promo-box a { color: #f39c12; font-weight: bold; text-decoration: underline; }
    /* --- Floating Quick Nav --- */
    .fab-container { position: fixed; bottom: 30px; right: 30px; z-index: 9999; font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; }
    .fab-button { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: #121212; display: flex; justify-content: center; align-items: center; font-size: 24px; cursor: pointer; box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4); transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .fab-button:hover { transform: scale(1.1); box-shadow: 0 6px 20px rgba(79, 172, 254, 0.6); }
    .fab-button i { transition: transform 0.3s ease; }
    .fab-container.active .fab-button i { transform: rotate(45deg); }
    .fab-menu { position: absolute; bottom: 80px; right: 0; width: 220px; background: rgba(18, 18, 18, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(79, 172, 254, 0.3); border-radius: 12px; padding: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); opacity: 0; visibility: hidden; transform: translateY(20px) scale(0.95); transform-origin: bottom right; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .fab-container.active .fab-menu { opacity: 1; visibility: visible; transform: translateY(0) scale(1); }
    .fab-menu h4 { color: #fff; margin: 0 0 15px 0; font-size: 1rem; text-align: center; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 10px; }
    .fab-menu a { display: flex; align-items: center; gap: 10px; color: #ccc; text-decoration: none; padding: 10px 12px; border-radius: 8px; margin-bottom: 8px; transition: 0.2s; font-size: 0.95rem; }
    .fab-menu a:last-child { margin-bottom: 0; }
    .fab-menu a:hover { background: rgba(79, 172, 254, 0.15); color: #4facfe; transform: translateX(5px); }
  </style>
</head>
<body>
  <div id="background"></div>
  <main class="catalog">
    <nav aria-label="面包屑"><a href="index.html" class="back-pill"><i class="fa-solid fa-arrow-left"></i> 返回 AI 教程库</a></nav>
    <div class="article-content">
        <h1>{title}</h1>
"""

layout_bottom = """
    </div>
  </main>
  
  <!-- Floating Quick Nav -->
  <div class="fab-container" id="fabContainer">
      <div class="fab-menu">
          <h4><i class="fa-solid fa-map-location-dot"></i> 快速导航</h4>
          <a href="../../index.html"><i class="fa-solid fa-house"></i> 回到首页</a>
          <a href="../tuijianjichang/index.html"><i class="fa-solid fa-plane-departure"></i> 2026 机场推荐</a>
          <a href="../tuijianjichang/brands/index.html"><i class="fa-solid fa-layer-group"></i> 机场品牌总库</a>
          <a href="../tuijianjichang/faq/index.html"><i class="fa-solid fa-circle-question"></i> FAQ 知识库</a>
          <a href="../cybersecurity/privacy.html"><i class="fa-solid fa-shield-halved"></i> 隐私与防泄漏</a>
          <a href="../cybersecurity/gfw-monitor.html"><i class="fa-solid fa-heart-pulse"></i> GFW 实时监控</a>
      </div>
      <div class="fab-button" id="fabButton">
          <i class="fa-solid fa-plus"></i>
      </div>
  </div>
  <script>
      document.getElementById('fabButton').addEventListener('click', function(e) {
          document.getElementById('fabContainer').classList.toggle('active');
          e.stopPropagation();
      });
      document.addEventListener('click', function(e) {
          if (!document.getElementById('fabContainer').contains(e.target)) {
              document.getElementById('fabContainer').classList.remove('active');
          }
      });
  </script>
</body>
</html>
"""

pages = {
    "chatgpt.html": {
        "title": "2026 最新 ChatGPT Plus 注册与防封号终极指南",
        "content": """
<h2>为什么你的 ChatGPT 总是被封号？</h2>
<p>在 2026 年的今天，OpenAI 的风控手段已经升级到了史无前例的严格程度。无数国内用户在费尽心思搞定虚拟信用卡（如 Wildcard 或 Depay）后，刚刚充值成功 ChatGPT Plus，没过两天就迎来了无情的 <strong>Access Denied</strong> 或直接被封号。这其中最大的罪魁祸首，并不是你的信用卡，而是你的<strong>网络 IP</strong>。</p>
<div class="promo-box">
    <strong>💡 站长强烈建议：</strong>不要使用廉价的万人骑直连机场！OpenAI 的系统会实时封杀那些被数百人同时使用且频繁变动归属地的脏 IP。要想账号长治久安，请务必使用拥有原生纯净 IP 的顶级专线。建议直接参考我们的 <a href="../tuijianjichang/index.html">2026 机场主推榜</a>，选择像 <strong>微风网络</strong> 或 <strong>无忧</strong> 这样提供独家原生 IP 的 IPLC 节点。
</div>
<h2>一、安全注册与充值流程</h2>
<h3>1. 准备干净的环境</h3>
<p>在开始注册之前，请务必打开浏览器的无痕模式，或者创建一个全新的浏览器独立配置档（Profile）。连接上您的原生 IP 节点（建议全局代理，并开启本地 DNS 防泄露）。通过 <code>whoer.net</code> 测试一下当前的匿名度，确保没有 WebRTC 泄露。</p>
<h3>2. 获取海外手机号验证</h3>
<p>虽然目前部分地区的注册已经取消了强制手机号验证，但为了保险起见，建议通过 SMS-Activate 等知名接码平台，选择欧美等非热门区域的号码进行辅助验证。</p>
<h3>3. 虚拟信用卡绑定技巧</h3>
<p>在进行 ChatGPT Plus 升级时，账单地址请务必填写与您当前节点 IP 所在的州或城市一致的免税州地址（如俄勒冈州、特拉华州、蒙大拿州）。这能大幅度降低 Stripe 支付网关的风控拦截率。</p>
<h2>二、日常防封号的核心准则</h2>
<ul>
    <li><strong>固定节点：</strong> 注册完成后，在日常使用中请尽量固定使用某一个国家的节点，切忌早上在日本，下午在美国，晚上在新加坡。</li>
    <li><strong>避免共享：</strong> 不要将您的账号密码随意分享给多人异地登录。</li>
    <li><strong>API 使用规范：</strong> 如果您申请了 API Key，绝对不要将 Key 暴露在公网 GitHub 代码库中，这会触发系统的立刻封禁。</li>
</ul>
<p>只要遵守上述原则，并坚持使用像 <strong>灵猫</strong>、<strong>飞猫云</strong> 这样经得起考验的原生专线，你的账号基本可以高枕无忧。</p>
"""
    },
    "claude.html": {
        "title": "Claude 3 封号太严重？如何优雅地绕过地区限制",
        "content": """
<h2>Claude 3：地球上风控最严苛的 AI</h2>
<p>随着 Claude 3 Opus 在代码逻辑和长文本解析上的卓越表现，越来越多的人开始将其作为主力生产力工具。然而，Anthropic 公司的风控力度堪称变态，很多用户甚至在注册页面的第一步就遭遇了直接封禁（所谓的“秒封”）。</p>
<div class="promo-box">
    <strong>💡 核心破局点：</strong>Claude 3 会深度检测你的 IP 是否为机房 IP (Hosting)、你的时区是否匹配、甚至你的浏览器指纹。想要稳稳地使用 Claude，一条高端、隐蔽的家庭宽带 IP (ISP) 或高质量原生 IP 是必需品。你可以去 <a href="../tuijianjichang/index.html">机场主推榜</a> 寻找 <strong>跨界</strong> 或 <strong>飞猫云</strong> 这样支持高级流媒体/AI 解锁的服务商。
</div>
<h2>一、浏览器防指纹隔离技术</h2>
<p>对于 Claude，普通的无痕模式已经不够用了。强烈建议使用防关联浏览器（如 AdsPower，哪怕是免费版）或者至少是 Chrome 的完全独立配置档，并安装 Canvas Blocker 插件来伪装浏览器指纹。</p>
<h2>二、注册时的四大忌讳</h2>
<ul>
    <li><strong>忌讳一：</strong> 使用 Google 账号直接一键授权登录（一旦你的 Google 账号绑定了国内手机或曾被判定为国内活跃用户，极易被连坐）。建议使用纯净的海外邮箱（如 ProtonMail）进行原生注册。</li>
    <li><strong>忌讳二：</strong> 节点不稳定导致的 IP 跳动。在接收短信验证码的这三分钟内，如果你的连接断开并自动切换到了另一个国家的节点，账号必死无疑。这也是为什么我们极其强调选择 <strong>大佬云 (Dalao)</strong> 这种具备全冗余 IPLC 架构、绝不断流的高端节点的原因。</li>
    <li><strong>忌讳三：</strong> 使用烂大街的接码号段。</li>
    <li><strong>忌讳四：</strong> 本地计算机的时区与语言未更改。请在系统设置中将时区改为美国，语言首选英语。</li>
</ul>
<h2>三、被封号后的申诉</h2>
<p>如果不幸被封禁，可以尝试向 <code>support@anthropic.com</code> 发送申诉邮件。态度诚恳，表明自己是真正的个人用户，只是在旅行途中。虽然成功率极低，但如果是误杀，偶尔也能找回账号。</p>
"""
    },
    "prompt.html": {
        "title": "Prompt 提示词工程：从小白到大师的 BROKE 框架",
        "content": """
<h2>废话连篇？那是你不会提问</h2>
<p>你是否经常觉得 AI 给出的回答就像是“正确的废话”？这是因为大模型是概率预测机器，你给的上下文越少，它猜测出的结果就越平庸。掌握 Prompt 提示词工程，是让你从“AI 体验者”进阶为“AI 掌控者”的唯一途径。</p>
<h2>一、万能的 BROKE 框架</h2>
<p>BROKE 框架是目前业界最推崇的结构化提示词编写方法：</p>
<ul>
    <li><strong>B (Background) 背景：</strong> 详细描述当前的业务场景和前置信息。</li>
    <li><strong>R (Role) 角色：</strong> 赋予 AI 一个顶级专家的身份（如：“你是一个拥有 20 年经验的高级前端架构师”）。</li>
    <li><strong>O (Objectives) 目标：</strong> 明确你最终想要达成的结果。</li>
    <li><strong>K (Key Results) 关键结果：</strong> 规定输出的具体内容要求（例如：“请输出三个不同的方案，并用表格对比优劣”）。</li>
    <li><strong>E (Evolve) 演进：</strong> 提出进一步优化的方向。</li>
</ul>
<h2>二、程序员专属：高阶代码 Review 模板</h2>
<p>你可以直接复制以下模板，填入你的代码：</p>
<pre style="background: #1e1e1e; padding: 15px; border-radius: 8px; color: #dcdcdc; overflow-x: auto;">
# Role: 高级资深系统架构师

# Background:
我正在使用 Python/Django 开发一个高并发的电商抢购接口。

# Objectives:
请对以下提供的代码片段进行严苛的 Code Review。

# Key Results:
1. 找出所有可能导致竞态条件 (Race Condition) 的逻辑漏洞。
2. 指出数据库锁使用的不当之处。
3. 提供一份重构后的优化代码，并用注释详细解释改动原因。

# Code:
[在此粘贴你的代码]
</pre>
<p><em>提示：在进行长文本代码分析时，请确保你的网络连接极其稳定。如果你频繁遭遇“生成中断”的问题，建议升级你的网络出海工具，去 <a href="../tuijianjichang/index.html">推荐榜单</a> 找那些主打不限速 IPLC 专线的优质品牌（如微风、闪跃）。</em></p>
"""
    },
    "midjourney.html": {
        "title": "Midjourney V6 核心参数与神仙画风咒语大全",
        "content": """
<h2>跨入 AI 绘画的神之领域</h2>
<p>Midjourney V6 相比之前的版本，在对自然语言的理解和光影真实感上有了质的飞跃。你不再需要堆砌毫无逻辑的关键词，而是可以用更口语化、像导演调度摄影机一样的语言来命令 AI。</p>
<h2>一、必背的核心后缀参数</h2>
<p>无论你的提示词写得多好，如果没有配合正确的参数设定，产出的图像往往会失去控制：</p>
<ul>
    <li><strong>--ar 16:9</strong>：调整图片的宽高比，适合桌面壁纸或视频素材；--ar 9:16 则适合小红书和抖音等竖屏平台。</li>
    <li><strong>--v 6.0</strong>：强制指定使用 V6 引擎（如果你没有在 /settings 里设置默认的话）。</li>
    <li><strong>--sref [图片URL]</strong>：极其逆天的“风格参考”功能。放上你喜欢的画风图片链接，MJ 会完美模仿其色调和笔触。</li>
    <li><strong>--cref [图片URL]</strong>：“角色一致性”参考。让 AI 在不同的场景里画出长相一模一样的同一个角色！</li>
</ul>
<h2>二、神仙画风咒语公式（直接复制可用）</h2>
<h3>1. 赛博朋克极客风</h3>
<p><code>A cyberpunk hacker sitting in a neon-lit dark room, surrounded by holographic coding screens, dramatic lighting, volumetric fog, highly detailed, 8k resolution, shot on 35mm lens --ar 16:9 --v 6.0 --style raw</code></p>
<h3>2. 唯美二次元吉卜力风</h3>
<p><code>Studio Ghibli style, a young girl standing in a massive magical library, floating glowing books, soft sunlight filtering through giant stained glass windows, pastel colors, anime art, masterpiece --ar 16:9 --niji 6</code></p>
<div class="promo-box">
    <strong>💡 站长提示：</strong>Midjourney 的生图极度消耗带宽（尤其是大图放大 Upscale 时）。如果你的梯子速度太慢，每次生成都会让你等到崩溃。想要秒刷无压力出图，请务必选配一条不限速的顶级专线，前往查阅站长的 <a href="../tuijianjichang/index.html">高性价比机场严选榜单</a>，其中 <strong>Firefly</strong> 和 <strong>跨界</strong> 在大流量并发下载方面表现尤为抢眼。
</div>
"""
    },
    "api-deploy.html": {
        "title": "API 中转池搭建与本地开源大模型部署指南",
        "content": """
<h2>告别昂贵的官方 API：开源与中转的力量</h2>
<p>如果你是一名独立开发者或者想在自己的 App 中接入 AI 能力，直接使用 OpenAI 官方的 API 往往面临两个巨大的难题：一是价格极其昂贵（尤其是 GPT-4），二是网络连接要求极高（服务器必须在海外）。</p>
<h2>一、搭建 OneAPI 聚合分发池</h2>
<p>OneAPI 是目前开源社区中最强大的大模型接口管理工具。它可以将 OpenAI、Anthropic、百度文心、阿里通义千问等国内外上百种模型的 API，全部统一包装成标准的 OpenAI 格式进行分发。</p>
<ul>
    <li><strong>优势 1：</strong>你可以去网络上寻找极其便宜的第三方中转商家（俗称“逆向池”），填入 OneAPI，瞬间实现 API 调用成本降级 90%。</li>
    <li><strong>优势 2：</strong>实现负载均衡。填入多个商家的 Key，当某一家宕机时，OneAPI 会自动切换，保证你的业务永不掉线。</li>
</ul>
<p><strong>部署要求：</strong> 一台海外的廉价 VPS（例如 Vultr 或搬瓦工），配合 Docker 即可一键跑起来。如果你在内网环境拉取 Docker 镜像极慢，请给你的服务器配置代理。若对线路质量要求苛刻，可参阅 <a href="../tuijianjichang/index.html">站长主推榜</a> 了解市面上的顶级海外线路架构原理。</p>
<h2>二、本地运行开源模型：Ollama + Llama 3</h2>
<p>对于数据极度敏感（不能传到云端）的业务，或者想在断网环境下使用的极客，本地部署开源大模型是最佳方案。</p>
<p><strong>Ollama</strong> 是一款让本地跑模型变得像运行普通软件一样简单的神器。只需要在终端输入一行命令 <code>ollama run llama3</code>，哪怕是普通轻薄本（只要有 8GB 以上内存），也能流畅地与 AI 对话。</p>
<p>结合 <strong>Open-WebUI</strong>，你甚至可以在自己的内网上搭建一个拥有漂亮界面的“私有版 ChatGPT”。这才是属于极客的终极浪漫！</p>
"""
    }
}

for filename, data in pages.items():
    filepath = os.path.join(base_dir, filename)
    full_html = layout_top.replace("{title}", data["title"]) + data["content"] + layout_bottom
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_html)

print("All 5 SEO optimized AI tutorial pages generated successfully.")
