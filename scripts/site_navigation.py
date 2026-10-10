"""Install the same accessible floating navigation on every HTML page."""
from pathlib import Path
import hashlib
import html
import json
import os
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HEAD_MARKER = '<!-- Shared floating navigation assets -->'
BODY_MARKER = '<!-- Shared floating navigation -->'
END_MARKER = '<!-- End shared floating navigation -->'


def add_navigation(text, path, *, include_content=True):
    path = Path(path).resolve()
    path.relative_to(ROOT)
    if not re.search(r'</head\s*>', text, re.I) or not re.search(r'</body\s*>', text, re.I):
        return text
    try:
        from .content_paths import add_content_paths
    except ImportError:
        from content_paths import add_content_paths
    if include_content:
        text = add_content_paths(text, path)
    try:
        from .brand_comparison_links import add_comparison_link
    except ImportError:
        from brand_comparison_links import add_comparison_link
    if include_content:
        text = add_comparison_link(text, path)
    # Only remove the legacy component, leaving adjacent page CSS untouched.
    text = re.sub(r'<!-- Floating Quick Nav -->\s*<div class="fab-container".*?</script>', '', text, flags=re.S)
    text = re.sub(r'/\* --- Floating Quick Nav --- \*/\s*', '', text)
    text = re.sub(r'(?m)^\s*\.fab-(?:container|button|menu)[^{}]*\{[^{}]*\}\s*', '\n', text)
    text = re.sub(re.escape(HEAD_MARKER) + r'.*?<!-- End shared floating navigation assets -->\s*', '', text, flags=re.S)
    text = re.sub(re.escape(BODY_MARKER) + r'.*?' + re.escape(END_MARKER) + r'\s*', '', text, flags=re.S)
    def link(relative):
        return html.escape(Path(os.path.relpath(ROOT / relative, path.parent)).as_posix(), quote=True)
    assets = f'''{HEAD_MARKER}
<link rel="stylesheet" href="{link('css/floating-navigation.css')}?v=20261010-rings" data-floating-navigation>
<script src="{link('js/floating-navigation-pages.js')}?v=20261010-rings" defer data-floating-navigation></script>
<script src="{link('js/floating-navigation.js')}?v=20261010-rings" defer data-floating-navigation></script>
<!-- End shared floating navigation assets -->
'''
    destinations = [
        ('topic/tuijianjichang/index.html', '站长精选机场推荐'),
        ('topic/tuijianjichang/brands/index.html', '机场品牌总库'),
        ('topic/tuijianjichang/comparison.html', '品牌对比'),
        ('topic/tuijianjichang/faq/index.html', 'FAQ 知识库'),
        ('topic/cybersecurity/privacy.html', '隐私与防泄漏'),
        ('topic/cybersecurity/gfw-monitor.html', 'GFW 与节点故障判断'),
    ]
    menu = ''.join(f'<a href="{link(url)}">{name}</a>' for url, name in destinations)
    back_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5m7-7-7 7 7 7"/></svg>'
    home_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3 10 9-7 9 7M5 9v12h5v-7h4v7h5V9"/></svg>'
    menu_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
    nav = f'''{BODY_MARKER}
<nav class="site-floating-nav" aria-label="快捷导航">
  <div class="site-floating-menu" id="site-floating-menu" hidden>
    <p class="site-floating-title">快速导航</p>
    <a href="{link('index.html')}">返回首页</a>{menu}
  </div>
  <div class="site-floating-controls">
    <button type="button" class="site-floating-action" data-floating-back data-home="{link('index.html')}" aria-label="返回上一页" title="返回上一页">{back_icon}</button>
    <a class="site-floating-action" href="{link('index.html')}" aria-label="返回首页" title="返回首页">{home_icon}</a>
    <button type="button" class="site-floating-toggle" data-floating-toggle aria-controls="site-floating-menu" aria-expanded="false" aria-label="打开快捷导航" title="快捷导航">{menu_icon}</button>
  </div>
</nav>
{END_MARKER}
'''
    text = re.sub(r'</head\s*>', lambda m: assets + m.group(), text, count=1, flags=re.I)
    text = re.sub(r'</body\s*>', lambda m: nav + m.group(), text, count=1, flags=re.I)
    try:
        from .mobile_reading import add_mobile_reading
    except ImportError:
        from mobile_reading import add_mobile_reading
    return add_mobile_reading(text, path)


def main():
    files = [p for p in ROOT.rglob('*.html') if not {'.git', 'node_modules'}.intersection(p.parts)]
    changes = []
    for path in files:
        before = path.read_bytes()
        text = before.decode('utf-8-sig')
        after = add_navigation(text, path).encode('utf-8')
        if before != after:
            changes.append((path, before, after))
    backup = Path(tempfile.mkdtemp(prefix='floating-navigation-before-')) if changes else None
    manifest = ROOT / 'topic/tuijianjichang/faq/article-output-hashes.json'
    hashes = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {}
    for path, before, after in changes:
        saved = backup / path.relative_to(ROOT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
        path.write_bytes(after)
        name = Path(os.path.relpath(path, manifest.parent)).as_posix()
        if hashes.get(name) == hashlib.sha256(before).hexdigest():
            hashes[name] = hashlib.sha256(after).hexdigest()
    if manifest.exists() and changes:
        manifest.write_text(json.dumps(hashes, indent=2) + '\n', encoding='utf-8')
    print(f'Floating navigation: {len(files)} HTML pages checked, {len(changes)} updated.')
    if backup:
        print(f'Backup: {backup}')


if __name__ == '__main__':
    main()
