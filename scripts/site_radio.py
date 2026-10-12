"""Share the existing homepage radio and install its persistent player."""
import hashlib
import html
import json
import os
import re
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def add_radio(text, path):
    if '</head>' not in text:
        return text
    text = re.sub(r'<!-- Site radio assets -->.*?<!-- End site radio assets -->\s*', '', text, flags=re.S)
    def relative(name):
        return html.escape(Path(os.path.relpath(ROOT / name, Path(path).parent)).as_posix(), quote=True)
    assets = f'''<!-- Site radio assets -->
<link rel="stylesheet" href="{relative('css/site-radio.css')}?v=20261012-inline3">
<script src="{relative('data/radio-playlist.js')}?v=20261012-inline3" defer></script>
<script src="{relative('js/site-radio.js')}?v=20261012-inline3" defer></script>
<!-- End site radio assets -->
'''
    return text.replace('</head>', assets + '</head>', 1)


def main():
    source = (ROOT / 'data/projects.js').read_text(encoding='utf-8')
    categories = json.loads(re.search(r'const radioMusicData = (\[.*?\n\]);', source, re.S)[1])
    (ROOT / 'data/radio-playlist.js').write_text('window.siteRadioLibrary = ' + json.dumps(categories,ensure_ascii=False,separators=(',',':')) + ';\n',encoding='utf-8')
    manifest_path = ROOT / 'topic/tuijianjichang/faq/article-output-hashes.json'
    hashes = json.loads(manifest_path.read_text(encoding='utf-8'))
    changed = 0
    for path in ROOT.rglob('*.html'):
        if 'data' in path.relative_to(ROOT).parts:
            continue
        before = path.read_bytes()
        after = add_radio(before.decode('utf-8'), path).encode('utf-8')
        if after == before:
            continue
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as staged:
            staged.write(after)
            staged_path = staged.name
        for attempt in range(5):
            try:
                os.replace(staged_path,path)
                break
            except PermissionError:
                if attempt == 4:
                    manifest_path.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                    raise
                time.sleep(.15*(attempt+1))
        key = Path(os.path.relpath(path,manifest_path.parent)).as_posix()
        if hashes.get(key) == hashlib.sha256(before).hexdigest():
            hashes[key] = hashlib.sha256(after).hexdigest()
        changed += 1
    manifest_path.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Radio: {sum(len(c["songs"]) for c in categories)} songs, {len(categories)} categories; {changed} pages updated.')


if __name__ == '__main__':
    main()
