import os
import re

base_dir = r"c:\Users\USER\Desktop\BLOG\Github内容\Home"
topic_index = os.path.join(base_dir, r"topic\index.html")
ai_dir = os.path.join(base_dir, r"topic\ai")

# 1. Update topic/index.html
with open(topic_index, "r", encoding="utf-8") as f:
    topic_content = f.read()

# Replace the link and text
# The original might have "AI 极客教程 (规划中)" and "cybersecurity/index.html" in the same block.
# We'll just do simple string replacements to avoid regex parsing issues.
topic_content = topic_content.replace('href="cybersecurity/index.html" class="project-card"', 'href="ai/index.html" class="project-card"')
# Wait, there are TWO project-cards pointing to cybersecurity/index.html? Let's check. 
# It's safer to use regex to specifically target the AI block.
topic_content = re.sub(
    r'<a href="[^"]+" class="project-card"[^>]*>(\s*<i[^>]+fa-microchip[^>]+></i>\s*<h3[^>]*>)AI 极客教程 \(规划中\)',
    r'<a href="ai/index.html" class="project-card" style="text-decoration: none; transition: 0.3s;" onmouseover="this.style.transform=\'translateY(-5px)\';this.style.boxShadow=\'0 10px 20px rgba(0,0,0,0.5)\';" onmouseout="this.style.transform=\'translateY(0)\';this.style.boxShadow=\'none\';">\1AI 极客教程',
    topic_content
)
# Update "规划中" span to "已上线" or just remove it
topic_content = re.sub(
    r'(<h3[^>]*>AI 极客教程</h3>.*?<div class="project-tag"><span style="background: #[a-zA-Z0-9]+;">)规划中(</span></div>)',
    r'\1已上线\2',
    topic_content,
    flags=re.DOTALL
)

with open(topic_index, "w", encoding="utf-8") as f:
    f.write(topic_content)

# 2. Create topic/ai/index.html
os.makedirs(ai_dir, exist_ok=True)
ai_index_path = os.path.join(ai_dir, "index.html")

ai_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 极客教程 | Cola 站长</title>
  <meta name="description" content="AI 极客教程：深度解析大模型的高阶玩法，解锁 ChatGPT、Claude 等前沿工具的进阶使用技巧与防封号指南。">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="../tuijianjichang/catalog.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    .brand-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
    .brand-card { background: rgba(30, 30, 30, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 25px; transition: 0.3s; }
    .brand-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.4); border-color: #9b59b6; }
    .brand-card h2 { color: #9b59b6; font-size: 1.4rem; margin-top: 0; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
    .brand-card p { color: #ccc; line-height: 1.6; font-size: 0.95rem; margin-bottom: 20px; }
    .card-links a { background: rgba(155, 89, 182, 0.15); color: #9b59b6; padding: 8px 15px; border-radius: 6px; text-decoration: none; font-size: 0.9rem; transition: 0.2s; font-weight: bold; border: 1px solid rgba(155, 89, 182, 0.3); }
    .card-links a:hover { background: #9b59b6; color: #fff; }
    
    /* Hero Header */
    .hero-section { text-align: center; margin-bottom: 40px; padding: 50px 20px; background: linear-gradient(145deg, rgba(30,30,30,0.8), rgba(15,15,15,0.95)); border: 1px solid rgba(155, 89, 182, 0.3); border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.6), inset 0 0 20px rgba(155, 89, 182, 0.05); position: relative; overflow: hidden; }
    .hero-glow { position: absolute; top: -50%; left: 50%; transform: translateX(-50%); width: 250px; height: 250px; background: rgba(155, 89, 182, 0.2); filter: blur(80px); border-radius: 50%; z-index: 0; }
  </style>
</head>
<body>
  <div id="background"></div>
  <main class="catalog">
    <nav aria-label="面包屑"><a href="../index.html" class="back-pill"><i class="fa-solid fa-arrow-left"></i> 返回专题库</a></nav>
    
    <header class="hero-section">
        <div class="hero-glow"></div>
        <div style="position: relative; z-index: 1;">
            <div style="display: inline-block; padding: 6px 16px; background: rgba(155, 89, 182, 0.1); border: 1px solid rgba(155, 89, 182, 0.4); color: #e056fd; border-radius: 30px; font-size: 0.9rem; font-weight: bold; margin-bottom: 20px; letter-spacing: 1px;">
                <i class="fa-solid fa-microchip"></i> 突破大模型能力边界
            </div>
            
            <h1 style="font-size: 2.8rem; font-weight: 900; margin: 0 0 20px 0; background: linear-gradient(to right, #ffffff, #e056fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 2px;">AI 极客教程与实战指南</h1>
            
            <p style="font-size: 1.15rem; color: #b0b0b0; max-width: 700px; margin: 0 auto 20px auto; line-height: 1.8;">
                深度解析大模型的高阶玩法，解锁 <span style="color: #fff; font-weight: bold;">ChatGPT、Claude 3、Midjourney</span> 等前沿工具的进阶使用技巧、提示词工程与防封号实战指南。
            </p>
        </div>
    </header>

    <section class="brand-grid">
        <article class="brand-card">
            <h2><i class="fa-brands fa-bots"></i> ChatGPT 进阶实战</h2>
            <p>从 Plus 会员安全充值、无痕注册，到最新的 GPT-4o 高级数据分析与 GPTs 构建指南。彻底解决“Access Denied”与大面积封号难题。</p>
            <div class="card-links"><a href="chatgpt.html"><i class="fa-solid fa-arrow-right"></i> 进入专区</a></div>
        </article>
        
        <article class="brand-card">
            <h2><i class="fa-solid fa-brain"></i> Claude 3 突破限制</h2>
            <p>目前最强代码辅助大模型 Claude 3 Opus 的使用指南。涵盖如何优雅地突破地区与节点封锁限制，以及长文本解析的最佳实践。</p>
            <div class="card-links"><a href="claude.html"><i class="fa-solid fa-arrow-right"></i> 进入专区</a></div>
        </article>

        <article class="brand-card">
            <h2><i class="fa-solid fa-terminal"></i> Prompt 提示词工程</h2>
            <p>拒绝废话连篇！学习结构化提示词编写框架（如 BROKE 框架），掌握让大模型输出精准、深度、符合业务逻辑格式文本的核心秘籍。</p>
            <div class="card-links"><a href="prompt.html"><i class="fa-solid fa-arrow-right"></i> 进入专区</a></div>
        </article>

        <article class="brand-card">
            <h2><i class="fa-solid fa-palette"></i> Midjourney 绘画流</h2>
            <p>从零基础到 AI 画师。深入解析后缀参数 (--v 6.0, --sref, --cref)、光影提示词配方，以及如何生成高质量、一致性的角色立绘与摄影级图像。</p>
            <div class="card-links"><a href="midjourney.html"><i class="fa-solid fa-arrow-right"></i> 进入专区</a></div>
        </article>
        
        <article class="brand-card">
            <h2><i class="fa-solid fa-server"></i> API 中转与本地部署</h2>
            <p>针对开发者的终极指南。如何寻找靠谱的第三方中转 API 降低调用成本，以及如何在本地机器部署 Llama 3、Stable Diffusion 等开源模型。</p>
            <div class="card-links"><a href="api-deploy.html"><i class="fa-solid fa-arrow-right"></i> 进入专区</a></div>
        </article>
        
        <article class="brand-card" style="border-color: rgba(255, 255, 255, 0.05); opacity: 0.7;">
            <h2><i class="fa-solid fa-hourglass-half"></i> 更多专题筹备中</h2>
            <p>AI 视频生成（Sora / Runway）、AI 自动化工作流（Make / Zapier）等深度实战教程正在紧密测试与撰写中，敬请期待。</p>
            <div class="card-links"><span style="color: #666; font-size: 0.9rem;">Coming Soon</span></div>
        </article>
    </section>
  </main>
</body>
</html>"""

with open(ai_index_path, "w", encoding="utf-8") as f:
    f.write(ai_html)
    
print("Successfully updated topic/index.html and created topic/ai/index.html")
