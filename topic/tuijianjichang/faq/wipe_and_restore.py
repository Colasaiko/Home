import os
import re

faq_dir = r"c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\faq"
index_path = os.path.join(faq_dir, "index.html")

# Read index.html to extract the pristine titles
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# Pattern to find: <a href="jichang-shi-shenme.html" class="faq-item" ...> ... <h3><i ...></i> 机场是什么？</h3>
matches = re.findall(r'<a href="([^"]+\.html)"[^>]*>.*?<h3[^>]*>.*?</i>\s*(.*?)\s*</h3>', index_html, re.DOTALL)

titles = {}
for url, title in matches:
    titles[url] = title.strip()

# Re-generate faq-data.js
faq_data = "const faqList = [\n"
for url, title in titles.items():
    # Escape quotes
    safe_title = title.replace("'", "\\'")
    faq_data += f"  {{ url: '{url}', title: '{safe_title}' }},\n"
faq_data += "];\n"

with open(os.path.join(faq_dir, "faq-data.js"), "w", encoding="utf-8") as f:
    f.write(faq_data)

# Re-generate all files except the 3 protected ones and index.html
files = [f for f in os.listdir(faq_dir) if f.endswith('.html') and f != 'index.html']

for file in files:
    if file in ["anzhuo-shouji-shenme-jichang.html", "2026wending-jichang-tuijian.html", "2026jichang-tuijian-naxie.html"]:
        continue
        
    title = titles.get(file, file.replace(".html", ""))
    
    skeleton = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | 翻墙教程与 FAQ | Cola 站长</title>
  <meta name="description" content="详细解答：{title}。站长 Cola 独家硬核科普与防坑指南，附带顶级机场推荐。">
  <link rel="stylesheet" href="../../../css/style.css">
  <link rel="stylesheet" href="../catalog.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="faq-enhancer.css">
</head>
<body>
  <div id="background"></div>
  <main class="catalog">
    <nav aria-label="面包屑" style="margin-bottom: 25px;"><a href="index.html" class="back-pill"><i class="fa-solid fa-arrow-left"></i> 返回 FAQ 总库</a></nav>
    <article class="panel">
        <h1 style="color: #fff; margin-bottom: 25px;"><i class="fa-solid fa-circle-question"></i> {title}</h1>
        
        <div class="article-content" style="background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.05); padding: 40px; border-radius: 12px; line-height: 1.8; color: #ccc; font-size: 1.1rem; margin-bottom: 40px;">
<p>内容深度撰写中，稍后由 AI 接入更新...</p>
        </div>
    </article>
  </main>
  <script src="faq-data.js"></script>
  <script src="faq-enhancer.js"></script>
</body>
</html>"""

    with open(os.path.join(faq_dir, file), "w", encoding="utf-8") as f:
        f.write(skeleton)

print(f"Successfully wiped and restored {len(files) - 3} files to clean UTF-8.")
