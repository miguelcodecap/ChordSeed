#!/usr/bin/env python3
"""Build the standalone Chordseed site (index.html) from the .dc.html sources in src/.
Usage: python3 build.py   -> writes index.html next to this file."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = {  # artifact asset id -> local file
    '85f00614d3b3815fbc8eaf6e2ebde1ba': 'assets/samples/guitar.json',
    '95d3807dba3d28a579b7fa0248138d93': 'assets/samples/piano.json',
    '76bc2776bbdf0c4c116459fc7db4cb96': 'assets/samples/eguitar.json',
    'eec270c5293a87022ab24e3b6c4a3bbc': 'assets/samples/flute.json',
    'bbe2c304a6aea668dc18c4d9f2b068ca': 'assets/samples/strings.json',
    '0bbb45d757a05a34fb9a660624ab95ac': 'assets/img/logo.png',
    '48d48012a66681c4137c00ce0c524b41': 'assets/img/sage-explain.webp',
    '6c0971d9e067a24781a61e967d406cd6': 'assets/img/sage-think.webp',
    'a1bcb5be43be1bb1de4b50eccb33d492': 'assets/img/sage-celebrate.webp',
    '59c41745f0aec0f2d5954978aabf7883': 'assets/img/sage-encourage.webp',
    '440c86fbc0a00111d14d8c556bbe7e24': 'assets/img/sage-play.webp',
}
def split(path):
    t = (ROOT / 'src' / path).read_text(encoding='utf-8')
    body = re.search(r'<x-dc>([\s\S]*)</x-dc>', t).group(1)
    helmet = re.search(r'<helmet>([\s\S]*?)</helmet>', body)
    script = re.search(r'<script type="text/x-dc"[^>]*>([\s\S]*?)</script>', t).group(1)
    tpl = body.replace(helmet.group(0), '') if helmet else body
    tpl = re.sub(r'<script type="text/x-dc"[\s\S]*?</script>', '', tpl)
    return (helmet.group(1) if helmet else ''), tpl.strip(), script
def blobs(s):
    def rep(m):
        f = ASSETS.get(m.group(1))
        if not f: raise SystemExit('Unknown asset id ' + m.group(1) + ' (add it to ASSETS in build.py)')
        return f
    return re.sub(r'/_blob/([0-9a-f]{32})', rep, s)
def js(s): return json.dumps(s).replace('</', '<\\/')
mh, mt, ms = split('Main.dc.html')
dh, dt, ds = split('Diagram.dc.html')
html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Chordseed · Every song begins as a seed</title>
<meta name="description" content="Chordseed helps you write songs: build chord progressions, hear them on real instruments, learn the theory behind them and see how famous songs use them.">
<meta property="og:title" content="Chordseed">
<meta property="og:description" content="Every song begins as a seed. Build chord progressions, hear them and learn why they work.">
<meta property="og:image" content="assets/img/logo.png">
<meta name="theme-color" content="#060D0A">
<link rel="icon" type="image/png" href="assets/img/logo.png">
{blobs(mh)}
</head>
<body>
<div id="app"></div>
<noscript>Chordseed needs JavaScript enabled.</noscript>
<script src="runtime/dc-runtime.js"></script>
<script>
ChordseedRuntime.define('Diagram', {js(blobs(dt))}, {js(ds)});
ChordseedRuntime.define('Main', {js(blobs(mt))}, {js(blobs(ms))});
window.__cs = ChordseedRuntime.mount('Main', document.getElementById('app'));
</script>
</body>
</html>
'''
# The app lives in /app/; shared assets stay at the site root.
html = (html.replace('"assets/', '"../assets/').replace("'assets/", "'../assets/")
            .replace('src="runtime/', 'src="../runtime/')
            .replace('href=\\"privacy.html\\"', 'href=\\"../privacy.html\\"').replace('href=\\"terms.html\\"', 'href=\\"../terms.html\\"'))
(ROOT / 'app').mkdir(exist_ok=True)
(ROOT / 'app' / 'index.html').write_text(html, encoding='utf-8')
print('app/index.html', len(html), 'bytes')
