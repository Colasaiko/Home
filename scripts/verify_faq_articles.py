"""Check the static FAQ library without changing any files."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from urllib.parse import urlsplit, unquote

FOLDER = Path(__file__).resolve().parents[1] / 'topic/tuijianjichang/faq'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.headings = [], [], []
        self.in_heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('a', 'link') and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'script' and 'src' in attrs:
            self.links.append(attrs['src'])
        if tag == 'h3':
            self.in_heading = True

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_heading = False

    def handle_data(self, text):
        if self.in_heading:
            self.headings.append(text)


def main():
    articles = json.loads((FOLDER / 'faq-articles.json').read_text(encoding='utf-8'))
    index = (FOLDER / 'index.html').read_text(encoding='utf-8')
    urls = re.findall(r'<div class="faq-item"(?: data-search="[^"]*")?><a href="([^"]+)"', index)
    assert len(urls) == len(set(urls)) == len(articles), 'Missing or duplicated index links'
    assert set(urls) == {a['url'] for a in articles}, 'Index and article data disagree'
    for article in articles:
        path = FOLDER / article['url']
        text = path.read_text(encoding='utf-8')
        assert '\ufffd' not in text and '内容深度撰写中' not in text, path
        assert not re.search(r'\{(?:client|service|region|audience|page_topic)\}', text), path
        page = Page()
        page.feed(text)
        assert len(page.ids) == len(set(page.ids)), path
        count = len(article['steps'])
        assert [i for i in page.ids if i.startswith('step-')] == [f'step-{i}' for i in range(1, count + 1)], path
        assert len(page.headings) == count and all(h.startswith(f'步骤 {i}：') for i, h in enumerate(page.headings, 1)), path
        assert page.ids.index('why') < page.ids.index('how') < page.ids.index('step-1'), path
        for link in page.links:
            if link.startswith(('https:', 'http:', 'mailto:', 'tel:', 'data:')):
                continue
            url = urlsplit(link)
            base, fragment = unquote(url.path), unquote(url.fragment)
            assert not base or (path.parent / base).exists(), (path, link)
            assert base or not fragment or fragment in page.ids, (path, link)
    print(f'PASS: {len(articles)} unique UTF-8 articles; WHY before HOW, ordered variable-length steps, valid directories and local links.')


if __name__ == '__main__':
    main()
