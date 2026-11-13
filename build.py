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
    '9c054e395a51d22640bca3947e92d965': 'assets/img/brand/fondos/panoramico-luna-16x9.webp',
    'c313510ca824c5f72fe34997f25e510f': 'assets/img/brand/fondos/bosque-app-9x16.webp',
    'f339a40ae0bbd31a517b6c85d793a665': 'assets/img/brand/fondos/textura-luciernagas-1x1.webp',
    'c8eff3f68593086c4680ac00400cdeda': 'assets/img/sage-explain.webp',
    '75038a63391fd7d3c5360256b2464469': 'assets/img/sage-think.webp',
    '10ad2059a9a47cd9297647428a61afe0': 'assets/img/sage-celebrate.webp',
    '39ce5f000bc2a416b84e9f03887bfd36': 'assets/img/sage-encourage.webp',
    '07f414ba6ee81a1f81096847c9c6af3a': 'assets/img/sage-play.webp',
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
<meta property="og:site_name" content="Chordseed">
<meta property="og:url" content="https://chordseed.pages.dev/app/">
<meta property="og:title" content="Chordseed · Every song begins as a seed">
<meta property="og:description" content="Find the next chord for the mood you want. Hear it, play it and learn why it works. Free in your browser.">
<meta property="og:image" content="https://chordseed.pages.dev/assets/img/og/chordseed.jpg">
<meta property="og:image:secure_url" content="https://chordseed.pages.dev/assets/img/og/chordseed.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Chordseed: an owl-masked forest alchemist with a lantern watches a glowing musical seed sprout from a tree stump under the moon.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Chordseed · Every song begins as a seed">
<meta name="twitter:description" content="Find the next chord for the mood you want. Hear it, play it and learn why it works. Free in your browser.">
<meta name="twitter:image" content="https://chordseed.pages.dev/assets/img/og/chordseed.jpg">
<link rel="canonical" href="https://chordseed.pages.dev/app/">
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

# Server-side engine for the Claude connector and the assistant
import runpy
runpy.run_path(str(ROOT / "server" / "build_engine.py"))
