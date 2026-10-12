"""Install shared mobile reflow assets without replacing page content."""
import hashlib
import html
import json
import os
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def add_mobile_reading(text, path):
    if '</head>' not in text:
        return text
    text = re.sub(r'<!-- Mobile reading assets -->.*?<!-- End mobile reading assets -->\n?', '', text, flags=re.S)
    def relative(name):
        return html.escape(Path(os.path.relpath(ROOT / name, Path(path).parent)).as_posix(), quote=True)
    assets = f'<!-- Mobile reading assets -->\n<link rel="stylesheet" href="{relative("css/mobile-reading.css")}?v=20261012-2">\n<script src="{relative("js/mobile-reading.js")}?v=20261012-2" defer></script>\n<!-- End mobile reading assets -->\n'
    return text.replace('</head>', assets + '</head>', 1)


def main():
    manifest_path = ROOT / 'topic/tuijianjichang/faq/article-output-hashes.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    changed = 0
    for path in ROOT.rglob('*.html'):
        if 'data' in path.relative_to(ROOT).parts:
            continue
        before = path.read_bytes()
        old = before.decode('utf-8')
        new = add_mobile_reading(old, path)
        if new != old:
            # Preserve the FAQ generator's overwrite protection for edited files.
            key = Path(os.path.relpath(path, manifest_path.parent)).as_posix()
            after = new.encode('utf-8')
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as staged:
                staged.write(after)
                staged_path = staged.name
            os.replace(staged_path, path)
            if manifest.get(key) == hashlib.sha256(before).hexdigest():
                manifest[key] = hashlib.sha256(after).hexdigest()
            changed += 1
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Mobile assets installed on {changed} pages.')


if __name__ == '__main__':
    main()
