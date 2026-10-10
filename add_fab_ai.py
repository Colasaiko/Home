import os, re

path = r'c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\ai\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

css = """
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
.fab-menu a i { width: 16px; text-align: center; }
"""

html_inject = """
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
"""

content = re.sub(r'(</style>)', f'{css}\n\\1', content, flags=re.IGNORECASE)
content = re.sub(r'(</body>)', f'{html_inject}\n\\1', content, flags=re.IGNORECASE)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FAB added to AI page.")
