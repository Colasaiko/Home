"""Install shared mobile reflow assets without replacing page content."""
import hashlib
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def add_mobile_reading(text, path):
    if '</head>' not in text:
        return text
    text = re.sub(r'\n?<!-- Mobile reading assets -->.*?<!-- End mobile reading assets -->\n?', '\n', text, flags=re.S)
    def relative(name):
        return html.escape(Path(os.path.relpath(ROOT / name, Path(path).parent)).as_posix(), quote=True)
    assets = f'\n<!-- Mobile reading assets -->\n<link rel="stylesheet" href="{relative("css/mobile-reading.css")}?v=20261010-1">\n<script src="{relative("js/mobile-reading.js")}?v=20261010-1" defer></script>\n<!-- End mobile reading assets -->\n'
    return text.replace('</head>', assets + '</head>', 1)


def main():
    manifest_path = ROOT / 'topic/tuijianjichang/faq/article-output-hashes.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    changed = 0
    for path in ROOT.rglob('*.html'):
        if 'data' in path.relative_to(ROOT).parts:
            continue
        old = path.read_text(encoding='utf-8')
        new = add_mobile_reading(old, path)
        if new != old:
            # Preserve the FAQ generator's overwrite protection for edited files.
            for key, digest in manifest.items():
                if (ROOT / key).resolve() == path.resolve() and digest == hashlib.sha256(old.encode()).hexdigest():
                    manifest[key] = hashlib.sha256(new.encode()).hexdigest()
            path.write_text(new, encoding='utf-8')
            changed += 1
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Mobile assets installed on {changed} pages.')


if __name__ == '__main__':
    main()
