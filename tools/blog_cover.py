#!/usr/bin/env python3
"""Render a topic cover: brand background + title + guitar chord diagrams of the article's key progression."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path('/home/claude/chordseed')

def diagram(name, frets):
    # frets: 6 strings low E -> high e; 'x' muted, 0 open, n fret
    nums = [int(f) for f in frets if f not in 'x0']
    base = 1 if not nums or max(nums) <= 4 else min(nums)
    W, H, x0, y0, sx, sy = 170, 230, 25, 62, 24, 34
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<text x="{W/2}" y="30" text-anchor="middle" class="cn">{name}</text>']
    if base == 1:
        s.append(f'<rect x="{x0-1}" y="{y0-5}" width="{sx*5+2}" height="6" fill="#E8D872"/>')
    else:
        s.append(f'<text x="{x0-8}" y="{y0+sy*0.65}" text-anchor="end" class="bf">{base}</text>')
    for i in range(6):
        s.append(f'<line x1="{x0+i*sx}" y1="{y0}" x2="{x0+i*sx}" y2="{y0+sy*4}" stroke="#C9D6C6" stroke-width="2"/>')
    for j in range(5):
        s.append(f'<line x1="{x0}" y1="{y0+j*sy}" x2="{x0+sx*5}" y2="{y0+j*sy}" stroke="#C9D6C6" stroke-width="2"/>')
    for i, f in enumerate(frets):
        x = x0 + i * sx
        if f == 'x':
            s.append(f'<text x="{x}" y="{y0-14}" text-anchor="middle" class="mk">×</text>')
        elif f == '0':
            s.append(f'<circle cx="{x}" cy="{y0-20}" r="7" fill="none" stroke="#E4EDE2" stroke-width="2.5"/>')
        else:
            n = int(f) - base + 1
            s.append(f'<circle cx="{x}" cy="{y0+(n-0.5)*sy}" r="10" fill="#E8D872"/>')
    s.append('</svg>')
    return ''.join(s)

def render(spec, out):
    chords = ''.join(f'<div class="ch {"hl" if c.get("hl") else ""}">{diagram(c["n"], c["f"])}</div>' for c in spec['chords'])
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
    body{{margin:0;width:1600px;height:905px;overflow:hidden;font-family:Inter,sans-serif;color:#E4EDE2}}
    .bg{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,13,10,.96) 0%,rgba(6,13,10,.82) 45%,rgba(6,13,10,.55) 100%),url('file://{ROOT}/assets/img/brand/fondos/{spec.get("bg","panoramico-luna-16x9.webp")}') center/cover}}
    .wrap{{position:absolute;inset:0;padding:90px 100px;display:flex;flex-direction:column;justify-content:space-between}}
    .eb{{color:#E8D872;font-weight:700;letter-spacing:.2em;font-size:24px;text-transform:uppercase}}
    h1{{font-family:'Liberation Serif',serif;font-style:italic;font-weight:700;font-size:86px;line-height:1.02;margin:18px 0 0;max-width:1150px;color:#F4F1DC}}
    .row{{display:flex;align-items:flex-end;gap:26px}}
    .ch{{background:rgba(15,29,22,.88);border:1.5px solid #2F4A3B;border-radius:22px;padding:6px 4px}}
    .ch.hl{{border-color:#E8D872;box-shadow:0 0 40px rgba(232,216,114,.35)}}
    .cn{{font:700 30px Inter;fill:#F4F7EC}} .mk{{font:700 20px Inter;fill:#9FB3A4}} .bf{{font:600 18px Inter;fill:#9FB3A4}}
    .lab{{margin-left:20px;color:#9FB3A4;font-size:30px;font-weight:600;padding-bottom:16px}} .lab b{{color:#E8D872}}
    .brand{{position:absolute;right:100px;top:90px;display:flex;align-items:center;gap:10px;font:italic 700 34px 'Liberation Serif';color:#E2D07A}}
    .brand img{{width:64px}}
    </style></head><body><div class="bg"></div>
    <div class="brand"><img src="file://{ROOT}/assets/img/logo.png">Chordseed</div>
    <div class="wrap"><div><div class="eb">{spec["eyebrow"]}</div><h1>{spec["title"]}</h1></div>
    <div class="row">{chords}<div class="lab">{spec["label"]}</div></div></div></body></html>'''
    p = pathlib.Path('/tmp/cover.html'); p.write_text(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = b.new_page(viewport={'width': 1600, 'height': 905})
        pg.goto('file:///tmp/cover.html'); pg.wait_for_timeout(400)
        pg.screenshot(path=out); b.close()

if __name__ == '__main__':
    render(json.loads(sys.argv[1]), sys.argv[2])
