#!/usr/bin/env python3
"""Generate the 5 new Chordseed blog posts (EN + ES), the Spanish blog index,
update the English blog index and sitemap. Usage: python3 gen.py <repo_root>"""
import sys, pathlib, re, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from posts_en import POSTS_EN
from posts_es import POSTS_ES
from PIL import Image

ROOT = pathlib.Path(sys.argv[1])
SITE = 'https://chordseed.pages.dev'
ORDER = ['borrowed', 'reharm', 'key', 'numbers', 'lofi']
DATE = '2026-11-24'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,600&family=Figtree:wght@400;500;600;700&display=swap">')

L = {
 'en': dict(features='Features', pricing='Pricing', open='Open the app', home='Home', app='App', privacy='Privacy', terms='Terms',
            all='← All articles', read='min read', journal='The Chordseed Journal', more='Keep reading', tryh='Try it in Chordseed',
            cta='Open the app →', other='Leer en español', locale='en_US',
            footer='© 2026 Chordseed. Created in Nevada, USA. · App creator:'),
 'es': dict(features='Funciones', pricing='Precios', open='Abrir la app', home='Inicio', app='App', privacy='Privacidad', terms='Términos',
            all='← Todos los artículos', read='min de lectura', journal='El diario de Chordseed', more='Sigue leyendo', tryh='Pruébalo en Chordseed',
            cta='Abrir la app →', other='Read in English', locale='es_ES',
            footer='© 2026 Chordseed. Creado en Nevada, EE. UU. · Creador de la app:'),
}

def url(lang, key):
    return f"/blog/{POSTS_EN[key]['slug']}/" if lang == 'en' else f"/blog/es/{POSTS_ES[key]['slug']}/"

def post(lang, key):
    return POSTS_EN[key] if lang == 'en' else {**POSTS_EN[key], **POSTS_ES[key]}

def esc(s): return html.escape(s, quote=True)

def head(lang, title, desc, canon, og_img, og_alt, up, alt_links, og_type='article'):
    alts = ''.join(f'<link rel="alternate" hreflang="{hl}" href="{SITE}{u}">\n' for hl, u in alt_links)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}{canon}">
{alts}<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Chordseed"><meta property="og:locale" content="{L[lang]['locale']}">
<meta property="og:url" content="{SITE}{canon}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/img/og/{og_img}.jpg">
<meta property="og:image:secure_url" content="{SITE}/assets/img/og/{og_img}.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og/{og_img}.jpg">
<meta name="theme-color" content="#060D0A">
<link rel="icon" type="image/png" href="{up}assets/img/logo.png">
{FONTS}
<link rel="stylesheet" href="{up}blog/blog.css">
'''

def nav(lang, up):
    t = L[lang]
    blog = f'{up}blog/' if lang == 'en' else f'{up}blog/es/'
    return f'''<body>
<div class="sky" aria-hidden="true"></div>
<nav><div class="wrap">
  <a class="brand" href="{up}" aria-label="Chordseed home"><img src="{up}assets/img/logo.png" alt="" width="52" height="52"><b>Chordseed</b></a>
  <div class="links"><a href="{up}#features">{t['features']}</a><a class="keep" href="{blog}">Blog</a><a href="{up}#pricing">{t['pricing']}</a><a class="btn sm" href="{up}app/">{t['open']}</a></div>
</div></nav>
'''

def footer(lang, up):
    t = L[lang]
    blog = f'{up}blog/' if lang == 'en' else f'{up}blog/es/'
    return f'''<footer><div class="wrap">
  <span>{t['footer']} <a href="https://github.com/miguelcodecap" target="_blank" rel="noopener" style="margin:0;color:var(--gold);font-weight:600">miguelcodecap</a> (GitHub)</span>
  <span><a href="{up}">{t['home']}</a><a href="{blog}">Blog</a><a href="{up}app/">{t['app']}</a><a href="{up}privacy.html">{t['privacy']}</a><a href="{up}terms.html">{t['terms']}</a></span>
</div></footer>
</body>
</html>
'''

def card(lang, key, up, thumb=True):
    p = post(lang, key)
    img = f'<img class="thumb" src="{up}assets/img/blog/{p["img"]}.webp" alt="" width="640" height="360" loading="lazy">' if thumb else ''
    return (f'<a class="card" href="{up}{url(lang, key)[1:]}">{img}<small>{esc(p["eyebrow"])} · {p["minutes"]} {L[lang]["read"]}</small>'
            f'<b>{esc(p["title"])}</b><span>{esc(p["card"])}</span></a>')

def article(lang, key):
    p, t = post(lang, key), L[lang]
    up = '../../' if lang == 'en' else '../../../'
    other_lang = 'es' if lang == 'en' else 'en'
    out = head(lang, f'{p["title"]} · Chordseed', p['desc'], url(lang, key), p['og'], p['title'], up,
               [('en', url('en', key)), ('es', url('es', key)), ('x-default', url('en', key))])
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BlogPosting",'
          f'"headline":{json_str(p["title"])},"description":{json_str(p["desc"])},"inLanguage":"{lang}",'
          f'"image":"{SITE}/assets/img/og/{p["og"]}.jpg","datePublished":"{DATE}","dateModified":"{DATE}",'
          f'"mainEntityOfPage":"{SITE}{url(lang, key)}","author":{{"@type":"Organization","name":"Chordseed"}},'
          f'"publisher":{{"@type":"Organization","name":"Chordseed","logo":{{"@type":"ImageObject","url":"{SITE}/assets/img/logo.png"}}}}}}</script>\n')
    out += ld + '</head>\n' + nav(lang, up)
    others = [k for k in ORDER if k != key]
    i = ORDER.index(key)
    picks = [ORDER[(i + 1) % 5], ORDER[(i + 2) % 5]]
    out += f'''<article>
<a href="{'../' if lang == 'en' else '../'}" style="font-size:14px;text-decoration:none">{t['all']}</a>
<span class="eyebrow" style="margin-top:22px">{esc(p['eyebrow'])}</span>
<h1>{esc(p['title'])}</h1>
<p class="lede">{p['lede']}</p>
<div class="meta">{p['minutes']} {t['read']} · {t['journal']} · <a href="{up}{url(other_lang, key)[1:]}" hreflang="{other_lang}" lang="{other_lang}">{t['other']}</a></div>
<img class="cover" src="{up}assets/img/blog/{p['img']}.webp" alt="{esc(p['alt'])}" width="1600" height="905">
{p['body'].strip()}

<div class="try"><h3>{t['tryh']}</h3><p>{p['try_text']}</p><a class="btn" href="{up}app/">{t['cta']}</a></div>
</article>
<div class="more"><span class="eyebrow">{t['more']}</span><div class="cards" style="grid-template-columns:1fr 1fr">{''.join(card(lang, k, up, False) for k in picks)}</div></div>
'''
    out += footer(lang, up)
    d = ROOT / url(lang, key).strip('/')
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(out, encoding='utf-8')

def json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)

def og_images():
    for k in ORDER:
        p = POSTS_EN[k]
        im = Image.open(ROOT / f'assets/img/blog/{p["img"]}.webp').convert('RGB')
        w, h = im.size  # 1600x905 -> crop to 1200:630 ratio
        th = int(w * 630 / 1200)
        top = max(0, (h - th) // 2)
        im.crop((0, top, w, top + th)).resize((1200, 630), Image.LANCZOS).save(ROOT / f'assets/img/og/{p["og"]}.jpg', quality=84, optimize=True, progressive=True)

def es_index():
    up = '../../'
    title = 'Blog en español · Chordseed'
    desc = 'Guías sencillas sobre acordes, ánimos y estructura de canciones para quien toca un poco y quiere componer su propia música.'
    out = head('es', title, desc, '/blog/es/', 'chordseed', 'Blog de Chordseed', up,
               [('en', '/blog/'), ('es', '/blog/es/'), ('x-default', '/blog/')], og_type='website')
    out += '</head>\n' + nav('es', up)
    out += ('<div class="head"><span class="eyebrow">El diario de Chordseed</span><h1>Componer, un acorde a la vez</h1>'
            '<p>Guías sencillas sobre acordes, ánimos y estructura de canciones, para quien toca un poco y quiere escribir su propia música. '
            '<a href="../" hreflang="en" lang="en">Read in English</a></p></div>\n')
    out += '<div class="wrap" style="padding-bottom:70px"><div class="cards">' + ''.join(card('es', k, up) for k in ORDER) + '</div></div>\n'
    out += footer('es', up)
    (ROOT / 'blog/es').mkdir(parents=True, exist_ok=True)
    (ROOT / 'blog/es/index.html').write_text(out, encoding='utf-8')

def en_index():
    f = ROOT / 'blog/index.html'
    t = f.read_text(encoding='utf-8')
    if 'borrowed-chords-beatles' in t:
        return
    new_cards = ''.join(card('en', k, '../') for k in ORDER)
    t = t.replace('<div class="wrap" style="padding-bottom:70px"><div class="cards">',
                  '<div class="wrap" style="padding-bottom:70px"><div class="cards">' + new_cards, 1)
    t = t.replace('and want to write their own music.</p></div>',
                  'and want to write their own music. <a href="../blog/es/" hreflang="es" lang="es">Leer en español</a></p></div>', 1)
    t = t.replace('<meta name="theme-color"',
                  f'<link rel="alternate" hreflang="en" href="{SITE}/blog/">\n<link rel="alternate" hreflang="es" href="{SITE}/blog/es/">\n<meta name="theme-color"', 1)
    f.write_text(t, encoding='utf-8')

def sitemap():
    f = ROOT / 'sitemap.xml'
    t = f.read_text(encoding='utf-8')
    if 'blog/es/' in t:
        return
    urls = [url('en', k) for k in ORDER] + ['/blog/es/'] + [url('es', k) for k in ORDER]
    add = ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod></url>\n' for u in urls)
    t = t.replace(f'  <url><loc>{SITE}/privacy.html</loc>', add + f'  <url><loc>{SITE}/privacy.html</loc>', 1)
    t = t.replace(f'<url><loc>{SITE}/blog/</loc><lastmod>2026-11-09</lastmod>', f'<url><loc>{SITE}/blog/</loc><lastmod>{DATE}</lastmod>', 1)
    f.write_text(t, encoding='utf-8')

if __name__ == '__main__':
    og_images()
    for k in ORDER:
        article('en', k); article('es', k)
    es_index(); en_index(); sitemap()
    print('ok')
