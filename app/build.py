"""Builds docs/index.html (GitHub Pages) by inlining data.json into index.src.html."""
import pathlib
here = pathlib.Path(__file__).parent
src = (here / 'index.src.html').read_text(encoding='utf-8')
data = (here / 'data.json').read_text(encoding='utf-8')
html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        + src.replace('\n<div class="wrap">', '\n</head><body>\n<div class="wrap">', 1).replace('__DATA__', data) + '\n</body></html>')
(here.parent / 'docs' / 'index.html').write_text(html, encoding='utf-8')
print('docs/index.html written')
