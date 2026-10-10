"""Verify contextual links independently of the floating navigation."""
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__()
        self.ids=[]
        self.links=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs: self.links.append(attrs['href'])

def main():
    pages={p.resolve():p.read_text(encoding='utf-8-sig') for p in ROOT.rglob('*.html') if not {'.git','node_modules'}.intersection(p.parts)}
    ids={p:set(Page(t).ids) for p,t in pages.items()}
    profiles=Counter()
    edges={}
    skipped=[]
    for path,text in pages.items():
        if path == ROOT/'index.html' or path.name in ('test_old.html','test_curr.html') or re.search(r'<meta[^>]+http-equiv=["\']refresh',text,re.I):
            skipped.append(path.relative_to(ROOT).as_posix())
            continue
        assert text.count('<!-- Contextual reading path -->') == 1,path
        assert text.count('<!-- Contextual reading assets -->') == 1,path
        assert text.count('<!-- Shared floating navigation -->') == 1,path
        section=re.search(r'<!-- Contextual reading path -->(.*?)<!-- End contextual reading path -->',text,re.S).group(1)
        profiles.update(re.findall(r'data-reading-profile="([^"]+)"',section))
        parsed=Page(section)
        assert len(parsed.links) >= 2,path
        assert text.count('id="continue-reading"') == 1,path
        edges[path]=set()
        # Check all links in editorial guides, not just the generated cards.
        relevant=section+''.join(re.findall(r'<(?:article|aside)[^>]*class="[^"]*reading-guide[^>]*>(.*?)</(?:article|aside)>',text,re.S))
        for link in Page(relevant).links:
            url=urlsplit(link)
            if url.scheme or url.netloc: continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            assert target in pages,(path,link)
            assert not url.fragment or unquote(url.fragment) in ids[target],(path,link)
            edges[path].add(target)
        assert path not in {(path.parent/urlsplit(a).path).resolve() for a in parsed.links},path
    core=[ROOT/p for p in ['api.html','tools.html','status.html','clients.html','topic/cybersecurity/privacy.html','topic/cybersecurity/gfw-monitor.html','topic/cybersecurity/protocols.html','topic/tuijianjichang/index.html','topic/tuijianjichang/brands/index.html','topic/tuijianjichang/faq/index.html']]
    content_edges={}
    for current,text in pages.items():
        body=re.sub(r'<!-- Shared floating navigation -->.*?<!-- End shared floating navigation -->','',text,flags=re.S)
        content_edges[current]=set()
        for link in Page(body).links:
            url=urlsplit(link)
            if url.scheme or url.netloc: continue
            target=(current.parent/unquote(url.path)).resolve() if url.path else current
            if target in pages: content_edges[current].add(target)
    # Every core topic must reach every other via content links, without FAB links.
    for origin in core:
        visited=set()
        pending=[origin]
        while pending:
            current=pending.pop()
            if current in visited: continue
            visited.add(current)
            pending.extend(content_edges[current]-visited)
        assert set(core) <= visited,origin
    folder=ROOT/'topic/tuijianjichang/faq'
    manifest=json.loads((folder/'article-output-hashes.json').read_text(encoding='utf-8'))
    for name,digest in manifest.items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest() == digest,name
    print(f'PASS: {sum(profiles.values())} content pages, {len(profiles)} contextual profiles, valid targets and fragments; 10 core topics mutually reachable without floating navigation; FAQ output hashes match.')
    print(f'Excluded {len(skipped)} home/preview/redirect pages from reading-path checks.')
    print('Profiles: '+json.dumps(profiles,ensure_ascii=False,sort_keys=True))

if __name__ == '__main__': main()
