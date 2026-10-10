from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import json

class Questions(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.rows = []
        self.text = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        url = attrs.get('href', '')
        if tag == 'a' and url.endswith('.html') and '/' not in url:
            self.active = True
            self.url = url
            self.text = []
    def handle_data(self, text):
        if self.active:
            self.text.append(text)
    def handle_endtag(self, tag):
        if tag == 'a' and self.active:
            self.rows.append({'url': self.url, 'title': ''.join(self.text).strip()})
            self.active = False

root = Path(__file__).resolve().parents[1]
folder = root / 'topic/tuijianjichang/faq'
parser = Questions()
parser.feed((folder / 'index.html').read_text(encoding='utf-8-sig'))
print('Questions:', len(parser.rows), 'Distinct URLs:', len({r['url'] for r in parser.rows}))
for i, row in enumerate(parser.rows, 1):
    print(i, row['url'], row['title'])
print('Duplicate titles:', {k: v for k, v in Counter(r['title'] for r in parser.rows).items() if v > 1})
print('Page lengths:', sorted((len(p.read_text(encoding='utf-8-sig')), p.name) for p in folder.glob('*.html'))[:8])
