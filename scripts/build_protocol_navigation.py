"""Add static section and chapter navigation to the ten protocol articles."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'topic/cybersecurity/protocols'
HEADING = re.compile(r'<h([2-4])\b([^>]*)>(.*?)</h\1>', re.S)


def plain(value):
    return html.unescape(re.sub(r'<[^>]+>', '', value)).strip()


def build():
    pages = [DIRECTORY / f'{number}.html' for number in range(1, 11)]
    titles = [plain(re.search(r'<h1\b[^>]*>(.*?)</h1>', p.read_text(encoding='utf-8'), re.S)[1]) for p in pages]
    for number, path in enumerate(pages, 1):
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'\n?<!-- Protocol navigation (?:assets|toc|chapters) -->.*?<!-- End protocol navigation -->\n?', '\n', text, flags=re.S)
        text = re.sub(r'<nav aria-label="(?:专线阅读目录|DNS 阅读目录)">.*?</nav>\s*', '', text, flags=re.S)
        content, tail = text.split('<!-- Contextual reading path -->', 1)
        entries = []
        used_ids = set(re.findall(r'\bid="([^"]+)"', text))

        def add_anchor(match):
            level, attrs, body = match.groups()
            existing = re.search(r'\bid=["\']([^"\']+)["\']', attrs)
            if existing:
                anchor = existing[1]
            else:
                anchor = f'protocol-section-{len(entries) + 1}'
                while anchor in used_ids:
                    anchor += '-heading'
                used_ids.add(anchor)
                attrs += f' id="{anchor}"'
            entries.append((int(level), anchor, plain(body)))
            return f'<h{level}{attrs}>{body}</h{level}>'

        content = HEADING.sub(add_anchor, content)
        primary = min(level for level, _, _ in entries)
        links = ''.join(f'<li class="protocol-toc-level-{level - primary}"><a href="#{html.escape(anchor, quote=True)}">{html.escape(label)}</a></li>' for level, anchor, label in entries)
        toc = f'\n<!-- Protocol navigation toc -->\n<nav class="protocol-toc" aria-label="本文目录"><details open><summary>本文目录 <span>第 {number} / 10 篇 · 点击标题跳转</span></summary><ul>{links}</ul></details></nav>\n<!-- End protocol navigation -->\n'
        content = re.sub(r'(</h1>)', lambda m: m[0] + toc, content, count=1)
        text = content + '<!-- Contextual reading path -->' + tail

        def chapter_link(target, direction, relation):
            return f'<a class="protocol-chapter" href="{target}.html" rel="{relation}"><span>{direction} · 第 {target} 篇</span><strong>{html.escape(titles[target - 1])}</strong></a>'

        previous = chapter_link(number - 1, '← 上一篇', 'prev') if number > 1 else '<div class="protocol-chapter-boundary"><span>这是第一篇</span><p>从 Shadowsocks 开始了解协议。</p></div>'
        following = chapter_link(number + 1, '下一篇 →', 'next') if number < 10 else '<div class="protocol-chapter-boundary"><span>已读到最后一篇</span><p>返回总目录，选择想复习的内容。</p></div>'
        chapters = f'\n<!-- Protocol navigation chapters -->\n<nav class="protocol-chapters" aria-label="协议文章连续阅读"><div class="protocol-chapters-heading"><h2>继续阅读协议系列</h2><a href="../protocols.html">全部 10 篇目录 →</a></div><div class="protocol-chapters-grid">{previous}{following}</div><a class="protocol-back-toc" href="#protocol-toc-top">↑ 返回本文目录</a></nav>\n<!-- End protocol navigation -->\n'
        text = text.replace('<nav class="protocol-toc"', '<nav id="protocol-toc-top" class="protocol-toc"', 1)
        text = text.replace('</article>', chapters + '</article>', 1)
        assets = '\n<!-- Protocol navigation assets -->\n<link rel="stylesheet" href="../../../css/protocol-navigation.css?v=20261010-follow">\n<script src="../../../js/protocol-navigation.js?v=20261010-follow" defer></script>\n<!-- End protocol navigation -->\n'
        text = text.replace('</head>', assets + '</head>', 1)
        path.write_text(text, encoding='utf-8')
        print(f'{path.name}: {len(entries)} section links; chapter {number}/10')


if __name__ == '__main__':
    build()
