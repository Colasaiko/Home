import os
import re

faq_dir = r"c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\faq"
faq_data_path = os.path.join(faq_dir, "faq-data.js")

# Get correct titles
titles = {}
try:
    with open(faq_data_path, "r", encoding="utf-8") as f:
        content = f.read()
        matches = re.findall(r"{ url: '(.*?)', title: '(.*?)' }", content)
        for url, title in matches:
            titles[url] = title
except Exception as e:
    pass

files = [f for f in os.listdir(faq_dir) if f.endswith('.html') and f != 'index.html']

for file in files:
    if file in ["anzhuo-shouji-shenme-jichang.html", "2026wending-jichang-tuijian.html", "2026jichang-tuijian-naxie.html"]:
        continue
        
    path = os.path.join(faq_dir, file)
    
    # Read the current broken file
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        broken_html = f.read()
        
    # Extract just the article content body
    article_content = ""
    match = re.search(r'(?s)class="article-content"[^>]*>(.*?)</div>\s*</article>', broken_html)
    if match:
        article_content = match.group(1).strip()
    
    # Clean up the known GBK artifacts in the AI text
    article_content = article_content.replace('?', '。')
    article_content = article_content.replace('</p>', '。</p>')
    article_content = article_content.replace('</h3>', '</h3>')
    article_content = article_content.replace('</h2>', '</h2>')
    
    # Strip any accidental duplicate text or weird AI output
    article_content = re.sub(r'，稍后由 AI 接入更新...</p>', '</p>', article_content)
    article_content = re.sub(r'<p>内容深度撰写中</p>', '', article_content)
    
    title = titles.get(file, file.replace(".html", ""))
    
    # Rebuild the perfect skeleton
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
{article_content}
        </div>
    </article>
  </main>
  <script src="faq-data.js"></script>
  <script src="faq-enhancer.js"></script>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(skeleton)

print("All HTML skeletons fixed and GBK artifacts cleaned up using Python.")
