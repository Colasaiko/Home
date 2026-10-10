"""Keep brand pages linked to the comparison without rewriting their content."""
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / 'topic/tuijianjichang/brands'


def add_comparison_link(text, path):
    path = Path(path).resolve()
    try:
        relative = path.relative_to(BRANDS)
    except ValueError:
        return text
    if relative.as_posix() != 'index.html' and not re.fullmatch(r'[^/]+/(?:index|latest)\.html', relative.as_posix()):
        return text
    text = re.sub(r'\n?<!-- Brand comparison entry -->.*?<!-- End brand comparison entry -->\n', '', text, flags=re.S)
    slug = relative.parts[0] if len(relative.parts) > 1 else ''
    url = Path(os.path.relpath(BRANDS.parent / 'comparison.html', path.parent)).as_posix()
    if slug:
        url += '?select=' + slug
    entry = '<!-- Brand comparison entry -->\n<aside class="guide-note brand-comparison-entry" aria-label="品牌横向对比"><p><a class="button" href="' + html.escape(url, quote=True) + '">进入品牌对比 →</a> ' + ('已为你选中当前品牌，再勾选其他品牌即可集中比较价格、流量与设备条件。' if slug else '按预算筛选，或勾选几个品牌集中比较价格、流量与设备条件。') + '</p></aside>\n<!-- End brand comparison entry -->\n'
    heading = re.search(r'<h1\b[^>]*>.*?</h1>', text, re.S)
    if heading:
        return text[:heading.end()] + '\n' + entry + text[heading.end():]
    content = re.search(r'<div\b[^>]*id="mainContent"[^>]*>', text)
    if content:
        return text[:content.end()] + '\n' + entry + text[content.end():]
    return text


if __name__ == '__main__':
    count = 0
    for path in BRANDS.rglob('*.html'):
        before = path.read_bytes()
        after = add_comparison_link(before.decode('utf-8'), path).encode('utf-8')
        if before != after:
            path.write_bytes(after)
            count += 1
    print(f'Added comparison entries to {count} brand pages.')
