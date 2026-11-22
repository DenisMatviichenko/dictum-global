import os, json
#!/usr/bin/env python3
"""Dictum Global — static site generator (black · olive · gold design).
Usage:  python3 _source/generate.py      → writes all pages into the parent folder."""
import html, os, json, datetime, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import re
import content as C
import logo as LOGOMOD
LOGO_SVG = LOGOMOD.svg()
from content import (PRACTICES, INDUSTRIES, PRODUCTS, P, CLUSTERS, CLUSTER_OF, PRODUCT_SHORT,
                     CLIENTS, TEAM_UA, TEAM_TR, NEWS, TAGS, OFFICES, fdate)
from i18n import LANGS, LANG_LABEL, translate, LOCALE

OUT = os.path.dirname(HERE) if os.path.basename(HERE) == '_source' else os.path.join(os.path.dirname(HERE), 'siteD_i')
SITE = 'https://dictum.ua'
e = html.escape

# ------------------------------------------------------------------ icons
ICON = {
    'scales': 'M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0zM12 3l-1 2h2z',
    'globe': 'M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18zM3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18',
    'building': 'M4 21V7l6-3v17M10 21V9l6-2v14M16 21V11l4 1v9M2 21h20M7 10v1M7 14v1M13 12v1M13 16v1',
    'shield': 'M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM8.5 12l2.5 2.5 4.5-5',
    'handshake': 'M2 12l4-4 4 2 3-2 4 1 5 3M6 8l-2 9M18 10l2 7M9 14l2 2a1.5 1.5 0 0 0 2-2M11 12l3 3a1.5 1.5 0 0 0 2-2l-3-3',
    'coins': 'M8 7a5 2 0 1 0 .01 0zM3 7v4c0 1.1 2.2 2 5 2s5-.9 5-2V7M3 11v4c0 1.1 2.2 2 5 2M11 13a5 2 0 1 0 10 0a5 2 0 1 0-10 0M11 13v4c0 1.1 2.2 2 5 2s5-.9 5-2v-4',
    'briefcase': 'M3 8h18v12H3zM8 8V5h8v3M3 13h18M11 13v2h2v-2',
    'chart': 'M3 21h18M5 17l5-5 4 3 6-8M16 7h4v4',
    'gavel': 'M14 4l6 6M12 6l6 6M13 5l-6 6 2 2 6-6M8 12l-5 5 2 2 5-5M4 21h9',
    'doc': 'M6 3h9l4 4v14H6zM14 3v5h5M9 12h7M9 16h7',
    'user': 'M12 12a4 4 0 1 0 0-8a4 4 0 0 0 0 8zM4 21c1-4 4-6 8-6s7 2 8 6',
    'key': 'M15 7a4 4 0 1 1-3.5 6L4 20.5V17h3v-3h3l1.5-1.5A4 4 0 0 1 15 7zM16 9h.01',
    'home': 'M3 11l9-7 9 7M5 10v10h14V10M10 20v-6h4v6',
    'leaf': 'M5 19c0-9 6-14 15-14 0 9-5 15-14 15M5 19l7-7',
    'chat': 'M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12zM8.5 11h.01M12 11h.01M15.5 11h.01',
    'check': 'M5 12l5 5 9-10',
    'arrow': 'M5 12h14M13 6l6 6-6 6',
    'left': 'M19 12H5M11 6l-6 6 6 6',
    'close': 'M6 6l12 12M18 6L6 18',
    'tg': 'M21 4L3 11l6 2 2 6 3-4 5 4zM9 13l9-6',
    'wa': 'M20 12a8 8 0 0 1-11.8 7L4 20l1.1-4.1A8 8 0 1 1 20 12zM9 9c0 3 3 6 6 6l1-1.5-2-1-1 .8c-1-.4-2-1.4-2.3-2.3l.8-1-1-2z',
    'li': 'M4 4h16v16H4zM8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7',
    'yt': 'M2 7a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v10a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3zM10 9l5 3-5 3z',
    'ig': 'M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zM12 8a4 4 0 1 0 0 8a4 4 0 0 0 0-8zM17 7v.01',
    'fb': 'M15 3h-2a4 4 0 0 0-4 4v3H7v4h2v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h2z',
    'mail': 'M3 5h18v14H3zM3 7l9 6 9-6',
}
PRACTICE_ICON = {
    'sudova-praktyka': 'gavel', 'podatkova-ta-mytna-bezpeka': 'coins', 'korporatyvne-pravo': 'briefcase',
    'mizhnarodne-strukturuvannya': 'globe', 'zemlya-ta-budivnyztvo': 'building', 'intelektualna-vlasnist': 'key',
    'trudova-bezpeka': 'user', 'zakhyst-biznesu': 'shield', 'dogovirne-pravo': 'doc', 'antikonkurentne-pravo': 'scales',
    'suprovid-investyzii': 'chart', 'suprovid-nerezydentiv': 'globe', 'antikorupczijna-praktika': 'shield', 'private-client': 'home',
}


def ico(name, cls='', w=None, sw='1.1'):
    size = f' width="{w}" height="{w}"' if w else ''
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c}{size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICON[name]}"/></svg>'



def flag(code, w=20):
    """Inline SVG flag (emoji flags do not render on Windows)."""
    h = round(w * 2 / 3)
    if code == 'ua':
        inner = '<rect width="30" height="10" fill="#0057B7"/><rect y="10" width="30" height="10" fill="#FFD700"/>'
        label = 'Україна'
    else:
        inner = '<rect width="30" height="20" fill="#E30A17"/><circle cx="10.6" cy="10" r="5" fill="#fff"/><circle cx="11.85" cy="10" r="4" fill="#E30A17"/><polygon fill="#fff" points="13.80,10.00 15.55,9.38 15.60,7.53 16.72,9.00 18.50,8.47 17.45,10.00 18.50,11.53 16.72,11.00 15.60,12.47 15.55,10.62"/>'
        label = 'Туреччина'
    return f'<svg class="flag" width="{w}" height="{h}" viewBox="0 0 30 20" role="img" aria-label="{label}">{inner}</svg>'

ARROW = ico('arrow', sw='2')
LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3DCA4"/><stop offset="1" stop-color="#A9782F"/></linearGradient></defs><path d="M6 6h14c9 0 15 6 15 14s-6 14-15 14H6V6z" fill="none" stroke="url(#lg{n})" stroke-width="2.4"/><path d="M6 20l9-7v14z" fill="#8FA63C"/></svg>'''


def logo(r, n):
    return f'<a class="logo" href="{r}index.html" aria-label="Dictum Global — на головну">{LOGO_SVG}</a>'


NAV = [
    ('pro-nas.html', 'Про компанію', 'about'),
    ('praktyky/index.html', 'Послуги', 'practices'),
    ('haluzi/index.html', 'Галузі', 'industries'),
    ('produkty/index.html', 'Продукти', 'products'),
    ('praktyky/mizhnarodne-strukturuvannya.html', 'Міжнародний бізнес', 'intl'),
    ('novyny/index.html', 'Новини', 'news'),
    ('kontakty.html', 'Контакти', 'contacts'),
]


# ------------------------------------------------------------------ layout
def layout(path, title, desc, body, active=None, jsonld=None, image='hero.jpg'):
    r = '../' * path.count('/')
    canon = SITE + '/' + ('' if path == 'index.html' else path.replace('index.html', ''))
    nav = '\n'.join(f'<a href="{r}{h}"' + (' aria-current="page"' if k == active else '') + f'>{t}</a>' for h, t, k in NAV)
    mnav = '\n'.join(f'<a href="{r}{h}">{t}</a>' for h, t, k in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    full = title if title.startswith('Dictum') else f'{title} — Dictum Global'
    return f'''<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<!--HREFLANG-->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dictum Global">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/img/{image}">
<meta property="og:locale" content="uk_UA">
<meta name="theme-color" content="#0E1217">
<link rel="icon" href="{r}img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/style.css">
<link rel="stylesheet" href="{r}css/theme-v2.css">
{ld}
</head>
<body>
<a class="skip-link" href="#main">Перейти до змісту</a>
<header class="site-header">
  <div class="site-header__inner">
    {logo(r, 'h')}
    <nav class="nav" aria-label="Головне меню">
{nav}
    </nav>
    <div class="header-actions">
      <!--LANGSWITCH-->
      <a class="btn btn--ghost" href="{r}kontakty.html#form">Записатись на консультацію</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Відкрити меню"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <nav aria-label="Мобільне меню">
{mnav}
  </nav>
  <div class="mobile-menu__foot">
    <a class="btn" href="{r}kontakty.html#form">Отримати консультацію {ARROW}</a>
    <a href="tel:+380678295806">+38 (067) 829 58 06</a>
    <a href="mailto:info@dictum.ua">info@dictum.ua</a>
    <!--LANGSWITCH-->
  </div>
</div>
<main id="main">
{body}
</main>
{footer(r)}
{tip(r)}
<script src="{r}js/main.js" defer></script>
</body>
</html>
'''


def footer(r):
    pr = ''.join(f'<li><a href="{r}praktyky/{s}.html">{e(P[s]["title"])}</a></li>' for s in
                 ['mizhnarodne-strukturuvannya', 'podatkova-ta-mytna-bezpeka', 'korporatyvne-pravo', 'zakhyst-biznesu', 'sudova-praktyka'])
    return f'''<footer class="site-footer">
  <div class="container site-footer__top">
    <div class="stack" style="gap:20px;max-width:340px">
      {logo(r, 'f')}
      <p class="muted" style="margin:0;font-size:14px;line-height:1.7">Ваш надійний партнер у світі міжнародного права та бізнесу. Офіси в Києві, Анталії та Стамбулі.</p>
      <div class="socials">
        <a href="https://www.linkedin.com/company/dictum.law/" aria-label="LinkedIn" rel="noopener" target="_blank">{ico('li', sw='1.6')}</a>
        <a href="https://www.youtube.com/@DictumLawCompany" aria-label="YouTube" rel="noopener" target="_blank">{ico('yt', sw='1.6')}</a>
        <a href="https://www.instagram.com/dictum.law/" aria-label="Instagram" rel="noopener" target="_blank">{ico('ig', sw='1.6')}</a>
        <a href="https://www.facebook.com/dictum.law/" aria-label="Facebook" rel="noopener" target="_blank">{ico('fb', sw='1.6')}</a>
        <a href="https://t.me/morozsvitlana" aria-label="Telegram" rel="noopener" target="_blank">{ico('tg', sw='1.6')}</a>
      </div>
    </div>
    <div><h4>Послуги</h4><ul>{pr}<li><a href="{r}praktyky/index.html">Усі 14 практик →</a></li></ul></div>
    <div><h4>Компанія</h4><ul>
      <li><a href="{r}pro-nas.html">Про компанію</a></li><li><a href="{r}pro-nas.html#team">Експерти</a></li><li><a href="{r}pro-nas.html#awards">Нагороди</a></li>
      <li><a href="{r}klienty.html">Клієнти</a></li><li><a href="{r}haluzi/index.html">Галузі</a></li><li><a href="{r}produkty/index.html">Продукти</a></li><li><a href="{r}novyny/index.html">Новини</a></li>
    </ul></div>
    <div><h4>Контакти</h4><ul>
      <li><a href="tel:+380678295806">+38 (067) 829 58 06</a></li><li><a href="tel:+380663722429">+38 (066) 37 22 429</a></li>
      <li><a href="mailto:info@dictum.ua">info@dictum.ua</a></li><li><a href="https://wa.me/380663722429" rel="noopener" target="_blank">WhatsApp</a></li>
      <li><a href="viber://chat?number=%2B380678295806">Viber</a></li><li><a href="{r}kontakty.html">Офіси →</a></li>
    </ul></div>
  </div>
  <div class="container site-footer__bottom">
    <span>© <span data-year>2026</span> Dictum Global. Усі права захищено.</span>
    <a href="https://dictum.ua/soglashenie/">Угода про обробку персональних даних</a>
  </div>
</footer>'''


def tip(r):
    return f'''<aside class="tip" id="tip" role="dialog" aria-label="Підказка: залиште заявку" aria-hidden="true">
  <button class="tip__close" type="button" aria-label="Закрити підказку">{ico('close', sw='1.6')}</button>
  <div class="tip__head"><span class="tip__icon" aria-hidden="true">{ico('chat', sw='1.8')}</span><span class="tip__title">Чим можемо бути корисними для Вас?</span></div>
  <p class="tip__text">Залиште заявку — експерт Dictum зв’яжеться з вами та запропонує рішення.</p>
  <p class="tip__done" role="status" hidden></p>
  <form data-endpoint="" novalidate>
    <input type="hidden" name="source" value="Підказка на сайті">
    <label class="field"><span>Ваш телефон</span><input type="tel" name="phone" autocomplete="tel" placeholder="+38 0__ ___ __ __" required><em class="field__err" aria-live="polite"></em></label>
    <div class="tip__row">
      <button class="btn" type="submit">Залишити заявку</button>
      <a class="tip__msg" href="https://t.me/morozsvitlana" aria-label="Написати в Telegram" rel="noopener" target="_blank">{ico('tg', sw='1.6')}</a>
      <a class="tip__msg" href="https://wa.me/380663722429" aria-label="Написати у WhatsApp" rel="noopener" target="_blank">{ico('wa', sw='1.6')}</a>
    </div>
  </form>
</aside>
<button class="fab" id="tip-fab" type="button" aria-label="Відкрити підказку: залишити заявку">{ico('chat', sw='1.8')}</button>'''


def head(eyebrow, title_html, right='', lead=''):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="head"><div class="head__title reveal"><span class="eyebrow">{eyebrow}</span><h2 class="h2">{title_html}</h2>{lead_html}</div>{right}</div>'


def page_hero(r, crumbs, label, title_html, lead, image, facts=''):
    cr = ''.join(f'<a href="{r}{h}">{e(t)}</a><span aria-hidden="true">/</span>' for h, t in crumbs)
    return f'''<section class="page-hero">
  <div class="page-hero__media" aria-hidden="true"><img src="{r}img/{image}" alt="" fetchpriority="high"></div>
  <div class="container page-hero__inner">
    <div class="page-hero__copy rise">
      <nav class="crumbs" aria-label="Навігаційний ланцюжок">{cr}<span aria-current="page">{e(label)}</span></nav>
      <span class="eyebrow eyebrow--line">{e(label)}</span>
      <h1 class="h1">{title_html}</h1>
      <p class="lead">{lead}</p>
    </div>
    <div class="rise" style="animation-delay:.15s">{facts}</div>
  </div>
</section>'''


def facts_box(r, rows):
    out = []
    for label, val, href in rows:
        inner = f'<span>{label}</span>' + (f'<b>{val}</b>' if val else ARROW.replace('<svg', '<svg width="18" height="18"'))
        out.append(f'<a href="{href}">{inner}</a>' if href else f'<div>{inner}</div>')
    return '<div class="facts">' + ''.join(out) + '</div>'


def contact_form(fid='form'):
    return f'''<form class="form reveal" data-d="1" id="{fid}" data-contact data-endpoint="" novalidate>
  <span class="form__title">Потрібна консультація?</span>
  <span class="muted" style="font-size:14px;margin-top:-8px">Залиште запит — експерт зв’яжеться з вами.</span>
  <label class="field"><span>Ім’я та прізвище</span><input type="text" name="name" autocomplete="name" required><em class="field__err" aria-live="polite"></em></label>
  <div class="row2">
    <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" required><em class="field__err" aria-live="polite"></em></label>
    <label class="field"><span>Телефон</span><input type="tel" name="phone" autocomplete="tel" required><em class="field__err" aria-live="polite"></em></label>
  </div>
  <label class="field"><span>Ваше питання або посилання на документ</span><textarea name="message" rows="3"></textarea></label>
  <label class="check"><input type="checkbox" name="consent" value="yes" required><span>Погоджуюсь з <a href="https://dictum.ua/soglashenie/">Угодою</a> на обробку даних</span></label>
  <button class="btn" type="submit">Надіслати запит {ARROW}</button>
  <p class="form__status" role="status" aria-live="polite"></p>
</form>'''


def contacts_section(r, title='Запишіться на зустріч з експертом'):
    return f'''<section class="section contacts" id="contacts">
  <img src="{r}img/meeting.jpg" alt="" aria-hidden="true" loading="lazy">
  <div class="container split" style="align-items:start">
    <div class="stack reveal">
      <span class="eyebrow">Контактна інформація</span>
      <h2 class="h2">{title}</h2>
      <div class="tiles">
        <a class="tile" href="tel:+380678295806"><small>Телефон</small><b>+38 (067) 829 58 06</b></a>
        <a class="tile" href="tel:+380663722429"><small>Телефон</small><b>+38 (066) 37 22 429</b></a>
        <a class="tile" href="mailto:info@dictum.ua"><small>Пошта</small><b>info@dictum.ua</b></a>
        <div class="tile"><small>Месенджери</small><span class="row row--icons"><a class="msg" href="https://t.me/morozsvitlana" rel="noopener" target="_blank" aria-label="Telegram" title="Telegram"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M21.6 3.3 2.9 10.5c-1.3.5-1.2 1.3-.2 1.6l4.8 1.5 1.8 5.6c.2.6.4.8.8.8.4 0 .6-.2.9-.5l2.4-2.3 4.9 3.6c.9.5 1.5.2 1.8-.8l3.2-15.1c.3-1.3-.5-1.9-1.7-1.6zM9 13.4l9.5-6c.4-.3.8-.1.5.2l-7.8 7.1-.3 3.4L9 13.4z"/></svg></a><a class="msg" href="https://wa.me/380663722429" rel="noopener" target="_blank" aria-label="WhatsApp" title="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.2A9.7 9.7 0 0 0 3.6 16.9L2.3 21.7l4.9-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7c-1.5 0-2.9-.4-4.2-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1a6.5 6.5 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.4-.6 1.6-1.2.2-.6.2-1.1.1-1.2l-.4-.2z"/></svg></a><a class="msg" href="viber://chat?number=%2B380678295806" aria-label="Viber" title="Viber"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 1.8c-2.4 0-6.5.3-8.4 2.1C2.2 5.3 1.8 7.3 1.7 9.8c-.1 2.5-.2 7.2 4.3 8.5v2c0 .4.2.9.8.5l2.2-2.4c3 .2 5.3-.3 5.6-.4.6-.2 4.1-.6 4.7-5 .6-4.6-.2-7.5-1.7-8.8C16.4 3 14.2 1.8 12 1.8zm.2 1.6c1.8 0 3.7.7 4.6 1.6 1.2 1.1 1.8 3.6 1.3 7.4-.5 3.6-3.1 3.8-3.6 4-.2.1-2.2.6-4.8.4l-2.6 2.8v-2.6c-3.6-1-3.4-4.9-3.3-7 .1-2 .4-3.7 1.6-4.8 1.5-1.4 4.8-1.7 6.8-1.8zm-3.4 2.5c-.3 0-.6.1-.8.3-.6.5-1.3 1.2-1 2 .8 2.1 2 4 3.6 5.6 1.6 1.6 3.5 2.7 5.6 3.5.8.3 1.5-.4 2-1 .4-.4.3-1-.1-1.3l-1.6-1.2c-.4-.3-1-.2-1.3.2l-.4.6c-.2.3-.6.3-.9.2-1.5-.7-2.8-2-3.5-3.5-.1-.3 0-.7.2-.9l.6-.4c.4-.3.5-.9.2-1.3L9.8 6.3c-.3-.3-.6-.4-1-.4zm3.6.3c-.2 0-.3.2-.3.4s.2.3.4.3c1.9.1 3.4 1.6 3.5 3.5 0 .2.2.4.4.4s.3-.2.3-.4c-.1-2.3-1.9-4.2-4.3-4.2zm.2 1.4c-.2 0-.3.1-.4.3 0 .2.1.4.3.4 1.1.1 1.9.9 2 2 0 .2.2.3.4.3s.3-.2.3-.4c-.1-1.4-1.2-2.5-2.6-2.6z"/></svg></a></span></div>
      </div>
    </div>
    {contact_form()}
  </div>
</section>'''


def mission(r):
    return f'''<section class="mission">
  <img src="{r}img/briefcase.jpg" alt="" aria-hidden="true" loading="lazy">
  <div class="container mission__inner">
    <div class="mission__copy reveal">
      <h2 class="h2">Ваш успіх — <em>наша місія</em></h2>
      <p class="lead">Зв’яжіться з нами сьогодні, щоб отримати персональну консультацію від експертів Dictum.</p>
      <a class="btn" href="{r}kontakty.html#form">Зв’язатися з нами {ARROW}</a>
    </div>
  </div>
</section>'''


CUR = {'lang': 'uk'}


def lang_prefix(lang):
    return '' if lang == 'uk' else lang + '/'


def write(path, content):
    lang = CUR['lang']
    depth = path.count('/')
    if lang != 'uk':
        content = translate(content, lang)
        content = re.sub(r'((?:href|src)=")((?:\.\./)*)(css/|js/|img/)', lambda m: m.group(1) + '../' + m.group(2) + m.group(3), content)
        content = content.replace('<html lang="uk">', f'<html lang="{lang}">').replace('content="uk_UA"', f'content="{LOCALE[lang]}"')
        content = content.replace(f'<link rel="canonical" href="{SITE}/', f'<link rel="canonical" href="{SITE}/{lang}/').replace(f'property="og:url" content="{SITE}/', f'property="og:url" content="{SITE}/{lang}/')
    to_site_root = '../' * (depth + (0 if lang == 'uk' else 1))
    sw = '<div class="lang" aria-label="Language">' + ''.join(
        f'<a href="{to_site_root}{lang_prefix(l)}{path}" lang="{l}"' + (' aria-current="true"' if l == lang else '') + f'>{LANG_LABEL[l]}</a>' for l in LANGS) + '</div>'
    content = content.replace('<!--LANGSWITCH-->', sw)
    clean = '' if path == 'index.html' else path.replace('index.html', '')
    hl = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{lang_prefix(l)}{clean}">\n' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{SITE}/{clean}">'
    content = content.replace('<!--HREFLANG-->', hl)
    path = lang_prefix(lang) + path
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)


REVIEWS = [(c[0], role) for c, role in zip(CLIENTS, ['Розвиток і просування бізнесу', 'Б’юті-проєкт', 'Імпорт обладнання для HoReCa', 'Барне обладнання та інгредієнти', 'YouTube-продакшен', 'Бізнес-об’єднання', 'Медичний центр'])]
REVIEWS[5] = ('Спілка підприємців України', REVIEWS[5][1])

FAQ = [
    ('З якими юрисдикціями ви працюєте?', 'Україна та Туреччина — у нас офіси в Києві, Анталії та Стамбулі. Для міжнародного структурування підбираємо іноземні юрисдикції під бізнес-модель клієнта, реєструємо компанії та супроводжуємо їх.'),
    ('Чи супроводжуєте ви іноземців і нерезидентів?', 'Так: дозвіл на роботу, посвідки на тимчасове й постійне проживання, громадянство, відкриття рахунків, реєстрація бізнесу та віддаленого офісу іноземної компанії в Україні.'),
    ('Що таке зовнішній юридичний департамент?', 'Абонентський супровід: проводимо аудит, формуємо пакет із фіксованою вартістю та обсягом годин щомісяця і щомісяця звітуємо про виконану роботу.'),
    ('Чи можна отримати консультацію онлайн?', 'Так. Напишіть у Telegram, WhatsApp або Viber чи залиште заявку на сайті — ми запропонуємо зручний час зустрічі.'),
    ('Хто веде мою справу?', 'Справи веде команда під керівництвом керуючого партнера Світлани Мороз — адвоката, кандидата юридичних наук; у Туреччині — партнера Наталії Олейнікової.'),
]


def faq_block(items, single=True, fid='faq'):
    out = []
    for i, (q, a) in enumerate(items):
        out.append(f'<details{" open" if i == 0 else ""}><summary><span class="n">{i + 1:02d}</span><span class="q">{e(q)}</span><span class="pm" aria-hidden="true"></span></summary><div class="faq__a">{a}</div></details>')
    return f'<div class="faq reveal" id="{fid}"' + (' data-single' if single else '') + '>' + ''.join(out) + '</div>'


# ------------------------------------------------------------------ home
GEO_SVG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'region_map.svg'), encoding='utf-8').read()
GEO_META = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'region_map.json'), encoding='utf-8'))
DOTS_SVG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'region_dots.svg'), encoding='utf-8').read()
GMAP_SVG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gmap.svg'), encoding='utf-8').read()
def geo_html():
    return '<div class="gm reveal">' + GMAP_SVG + '</div>'
def geo_html_light():
    p = GEO_META['pos']
    lbl = lambda k, name, fl, side: f'<span class="geo__label geo__label--{side}" style="left:{p[k][0]}%;top:{p[k][1]}%">{flag(fl, 16)}{name}</span>'
    return (f'<div class="geo reveal"><div class="geo__map" style="aspect-ratio:{GEO_META["W"]}/{GEO_META["H"]}"><img class="geo__base" src="img/dg-region.svg" alt="" loading="lazy">' + GEO_SVG
            + lbl('kyiv', 'Київ', 'ua', 'right') + lbl('ist', 'Стамбул', 'tr', 'left') + lbl('ant', 'Анталія', 'tr', 'right') + '</div></div>')

def page_home():
    r = ''
    strip = [('Міжнародне<br>право', 'scales', 'praktyky/mizhnarodne-strukturuvannya.html'), ('Податкове<br>планування', 'coins', 'praktyky/podatkova-ta-mytna-bezpeka.html'),
             ('Реєстрація компаній<br>за кордоном', 'building', 'praktyky/korporatyvne-pravo.html'), ('Податкова<br>та митна безпека', 'shield', 'praktyky/podatkova-ta-mytna-bezpeka.html'),
             ('Бізнес-<br>консалтинг', 'handshake', 'produkty/zovnishnij-departament.html')]
    SV = lambda d, c, sw='1.4': f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'
    hcards = ''.join(f'<a class="hcard" href="{h}">{ico(i, "i", sw="1.3")}<span>{t.replace("-<br>", "-").replace("<br>", " ")}</span>{SV("M5 12h14M13 6l6 6-6 6", "a", "1.8")}</a>' for t, i, h in strip)
    strip_html = ''.join(f'<a class="strip__item" href="{h}">{ico(i, w=40)}<span>{t}</span></a>' for t, i, h in strip)
    services = [('Міжнародне податкове планування', 'Податкові моделі, трансфертне ціноутворення, КІК і Substance.', 'coins', 'podatkova-ta-mytna-bezpeka'),
                ('Реєстрація компаній за кордоном', 'Вибір юрисдикції, реєстрація, рахунки, корпоративні документи.', 'globe', 'mizhnarodne-strukturuvannya'),
                ('Юридичний супровід бізнесу', 'Корпоративне та договірне право, зовнішній юрдепартамент.', 'briefcase', 'korporatyvne-pravo'),
                ('Супровід інвестицій', 'Due diligence, інвестиційні угоди, M&A, захист інвестора.', 'chart', 'suprovid-investyzii'),
                ('Захист бізнесу', 'Перевірки, обшуки, арешти рахунків, протидія рейдерству.', 'shield', 'zakhyst-biznesu'),
                ('Судова практика', 'Податкові, митні, договірні та корпоративні спори.', 'gavel', 'sudova-praktyka')]
    cards = ''.join(f'<a class="card reveal" data-d="{k % 3}" href="praktyky/{s}.html">{ico(i, "ico")}<b>{t}</b><span>{d}</span></a>' for k, (t, d, i, s) in enumerate(services))
    SAMPLES = [
        ('Допомогли зареєструвати компанію в Туреччині та відкрити рахунки. Усе пояснили простою мовою й дотрималися термінів.', 'Керівник IT-компанії', 'IT · Київ — Стамбул', 'IT'),
        ('Під час податкової перевірки команда була поруч із першого дня. Донарахування вдалося скасувати.', 'Фінансовий директор', 'Імпорт обладнання', 'ФД'),
        ('Працюємо з Dictum як із зовнішнім юрдепартаментом: швидкі відповіді, зрозумілі звіти й жодних сюрпризів.', 'Власниця бізнесу', 'Б’юті-індустрія', 'ВБ'),
        ('Допомогли вибудувати структуру бізнесу між Україною та Туреччиною. Партнер особисто вів проєкт від початку до кінця.', 'Засновник компанії', 'E-commerce', 'ЗК'),
        ('Оперативно зняли арешт із рахунків і пояснили, як уникнути таких ризиків надалі.', 'Генеральний директор', 'Дистрибуція', 'ГД'),
        ('Супровід угоди з турецьким партнером пройшов спокійно: договір, перевірка контрагента, переговори.', 'Комерційний директор', 'Виробництво', 'КД'),
    ]
    reviews = ''.join(f'''<figure class="review" role="group" aria-roledescription="слайд" aria-label="{k + 1} з {len(SAMPLES)}">
  <div class="stack" style="gap:18px"><span class="review__q" aria-hidden="true">“</span><div class="review__stars" role="img" aria-label="Оцінка 5 з 5">★★★★★</div>
  <blockquote>{e(t)}</blockquote><span class="review__sample">Приклад відгуку</span></div>
  <figcaption><span class="avatar" aria-hidden="true">{e(ini)}</span><span><b>{e(n)}</b><small>{e(role)}</small></span></figcaption>
</figure>''' for k, (t, n, role, ini) in enumerate(SAMPLES))
    compare = [('Команда з досвідом у 14 практиках', '✓', '—', '◐'), ('Україна та Туреччина в одній команді', '✓', '—', '—'),
               ('Фіксований щомісячний пакет і звітність', '✓', '✓', '—'), ('Моніторинг реєстрів і нових судових спорів', '✓', '◐', '—'),
               ('Тренінги персоналу до перевірок і обшуків', '✓', '—', '◐'), ('Оперативний виїзд на підприємство', '✓', '✓', '◐')]
    mark = lambda v: {'✓': '<span aria-label="так">✓</span>', '—': '<span aria-label="ні">—</span>', '◐': '<span style="font-size:13px">частково</span>'}[v]
    rows = ''.join(f'<tr><th scope="row">{t}</th><td class="is-us">{mark(a)}</td><td>{mark(b)}</td><td>{mark(c)}</td></tr>' for t, a, b, c in compare)
    offices = ''.join(f'<div><b>{flag("ua" if c == "Україна" else "tr", 24)}{t}</b><span>{e(a)}</span></div>' for t, c, a, m in OFFICES)
    cases = [('Податки · IT', '09.06.2026', 'Як аудит Dictum врятував міжнародний IT-бізнес від податкового шторму'),
             ('Захист бізнесу', '27.05.2021', 'Захист бізнесу під час обшуків: лайфхаки зняття арешту'),
             ('Судова практика', '15.07.2021', 'Спори за договорами франчайзингу: секрети судових перемог')]
    cases_html = ''.join(f'<a class="case reveal" data-d="{k}" href="https://dictum.ua/klienty/" rel="noopener"><div class="case__meta"><span>{t}</span><span>{d}</span></div><h3>{e(h)}</h3><span class="more">Читати кейс →</span></a>' for k, (t, d, h) in enumerate(cases))

    body = f'''
<section class="hx" id="top">
  <div class="hx__media" aria-hidden="true"><img src="img/dg-hero.jpg" alt="" fetchpriority="high"></div>
  <div class="hx__glass" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="container">
    <div class="hx__copy rise">
      <span class="eyebrow">Україна · Туреччина · міжнародні структури</span>
      <h1 class="h1">Юридичний супровід бізнесу <em>в Україні та Туреччині</em></h1>
      <p class="lead">Комплексні юридичні рішення для бізнесу без кордонів: 10 років в Україні, 4 роки в Туреччині.</p>
      <div class="hx__actions"><a class="btn" href="kontakty.html#form">Отримати консультацію {ARROW}</a><a class="play" href="#about"><i>{SV("M8 5l11 7-11 7z", "p", "1.6")}</i>Дізнатись більше</a></div>
    </div>
    <nav class="hx__cards" aria-label="Ключові напрями">{hcards}</nav>
  </div>
</section>

<section class="facts2" aria-label="Dictum у цифрах">
  <div class="facts2__map" aria-hidden="true">{DOTS_SVG}</div>
  <div class="container">
    <p class="facts2__lead">DICTUM — ваш партнер у світі міжнародного права</p>
    <div class="facts2__item"><b>10+</b><span>років супроводу бізнесу в Україні</span></div>
    <div class="facts2__item"><b>4</b><span>роки практики в Туреччині</span></div>
    <div class="facts2__item"><b>3</b><span>офіси: Київ, Анталія, Стамбул</span></div>
    <div class="facts2__item"><b>ТОП-50</b><span>юрфірм України 2021–2025</span></div>
  </div>
</section>

<section class="section about2 is-light" id="about">
  <div class="about2__img" aria-hidden="true"><img src="img/dg-building.jpg" alt="" loading="lazy"></div>
  <div class="container">
    <div class="about2__copy reveal">
      <span class="eyebrow">Про компанію</span>
      <h2 class="h2">Експертиза. Довіра. Результат.</h2>
      <p>Dictum — юридична компанія, яка поєднує глибоку експертизу в податковому, корпоративному та міжнародному праві, практичний досвід і персональний підхід до кожного клієнта. Ми ведемо бізнес в Україні та Туреччині однією командою.</p>
      <a class="btn btn--ghost" href="pro-nas.html">Більше про компанію {ARROW}</a>
    </div>
    <ul class="about2__list reveal" data-d="1">
      <li><i>{SV("M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18", "x", "1.5")}</i>Україна та Туреччина — в одній команді</li>
      <li><i>{SV("M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0", "x", "1.5")}</i>Партнер особисто веде вашу справу</li>
      <li><i>{SV("M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM8.5 12l2.5 2.5 4.5-5", "x", "1.5")}</i>ТОП-50 юрфірм України 2021–2025</li>
    </ul>
  </div>
</section>

<section class="section" id="services">
  <div class="container services-layout">
    <div class="stack reveal" style="max-width:420px">
      <span class="eyebrow">Наші послуги</span>
      <h2 class="h2">Рішення <em>для</em> міжнародного бізнесу</h2>
      <p class="lead" style="font-size:16px">Ми допомагаємо бізнесу працювати ефективно в Україні та за кордоном — від податкової безпеки до захисту в суді.</p>
      <a class="btn btn--ghost" href="praktyky/index.html" style="align-self:flex-start">Усі 14 практик {ARROW}</a>
    </div>
    <div class="cards">{cards}</div>
  </div>
</section>

<section class="section reviews is-light" id="reviews">
  <div class="container carousel" data-carousel aria-roledescription="карусель" aria-label="Відгуки клієнтів">
    {head('Відгуки клієнтів', 'Що кажуть про <em>нашу роботу</em>', f'<div class="carousel__nav"><span class="carousel__count" aria-live="polite"></span><button class="round" type="button" data-prev aria-label="Попередній відгук">{ico("left", sw="1.6")}</button><button class="round round--solid" type="button" data-next aria-label="Наступний відгук">{ico("arrow", sw="1.8")}</button></div>')}
    <div class="carousel__viewport"><div class="carousel__track">{reviews}</div></div>
    <div class="dots" aria-label="Вибір відгуку"></div>
  </div>
</section>

<section class="section">
  <div class="container">
    {head('Формат співпраці', 'Чому бізнес обирає <em>зовнішній департамент</em> Dictum', '<a class="btn btn--ghost" href="produkty/zovnishnij-departament.html">Про продукт</a>')}
    <div class="table-wrap reveal"><table class="compare">
      <thead><tr><th scope="col">Що ви отримуєте</th><th scope="col" class="is-us">Dictum</th><th scope="col">Штатний юрист</th><th scope="col">Разові консультації</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="legend">✓ — входить у формат · «частково» — залежить від домовленостей · — — не передбачено</p>
  </div>
</section>

<section class="section gm-sec" id="global">
  <div class="container split">
    {geo_html()}
    <div class="stack reveal" data-d="1">
      <span class="eyebrow">Міжнародна присутність</span>
      <h2 class="h2">Глобальна експертиза — <em>локальна увага</em></h2>
      <p class="lead" style="font-size:16px">Офіси в Києві, Анталії та Стамбулі. Супроводжуємо міжнародне структурування, нерезидентів в Україні та український бізнес у Туреччині — разом з Українською бізнес-радою в Туреччині (UBC).</p>
      <div class="office-rows">{offices}</div>
      <a class="btn btn--ghost" href="praktyky/mizhnarodne-strukturuvannya.html" style="align-self:flex-start">Дізнатися більше {ARROW}</a>
    </div>
  </div>
</section>

<section class="section is-light" id="cases">
  <div class="container">
    {head('Кейси та аналітика', 'Реальні справи — <em>реальні рішення</em>', '<a class="btn btn--ghost" href="novyny/index.html">Усі публікації</a>')}
    <div class="grid3">{cases_html}</div>
  </div>
</section>

<section class="section bg-2 bt">
  <div class="container split" style="align-items:start">
    <div class="stack reveal"><span class="eyebrow">Часті запитання</span><h2 class="h2">Відповідаємо <em>одразу</em></h2><p class="lead" style="font-size:16px">Не знайшли відповіді? Напишіть нам у <a href="https://t.me/morozsvitlana" style="color:var(--gold)">Telegram</a> або <a href="https://wa.me/380663722429" style="color:var(--gold)">WhatsApp</a>.</p></div>
    {faq_block([(q, e(a)) for q, a in FAQ])}
  </div>
</section>

{mission(r)}
{contacts_section(r)}
'''
    ld = {'@context': 'https://schema.org', '@type': 'LegalService', 'name': 'Dictum Global', 'url': SITE, 'image': SITE + '/img/hero.jpg',
          'email': 'info@dictum.ua', 'telephone': '+380678295806',
          'address': [{'@type': 'PostalAddress', 'streetAddress': 'вул. Нижньоключова, 14, офіс 9', 'addressLocality': 'Київ', 'addressCountry': 'UA'},
                      {'@type': 'PostalAddress', 'streetAddress': 'Sinan Mah., 1288. Sk. No: 2', 'postalCode': '07100', 'addressLocality': 'Antalya', 'addressCountry': 'TR'},
                      {'@type': 'PostalAddress', 'streetAddress': 'Merkez Mah., Sadabad Cd. No: 44A', 'postalCode': '34406', 'addressLocality': 'İstanbul', 'addressCountry': 'TR'}],
          'sameAs': ['https://www.facebook.com/dictum.law/', 'https://www.instagram.com/dictum.law/', 'https://www.linkedin.com/company/dictum.law/', 'https://www.youtube.com/@DictumLawCompany']}
    write('index.html', layout('index.html', 'Dictum Global — юридична компанія: міжнародне право та бізнес',
                               'Dictum Global — комплексні юридичні рішення для бізнесу без кордонів: 10 років в Україні, 4 роки в Туреччині. Податки, міжнародне структурування, захист бізнесу.', body, jsonld=ld))


# ------------------------------------------------------------------ lists & details
def page_practices_index():
    r = '../'
    groups = []
    for i, (title, text, slugs) in enumerate(CLUSTERS):
        cards = ''.join(f'<a class="card" href="{s}.html">{ico(PRACTICE_ICON[s], "ico")}<b>{e(P[s]["title"])}</b><span>{len(P[s]["cards"])} напрямів роботи</span><span class="more">Детальніше →</span></a>' for s in slugs)
        groups.append(f'<div class="group"><div class="group__head reveal"><span class="group__num">{["I","II","III","IV"][i]}</span><h2 class="h3">{e(title)}</h2><p class="muted" style="margin:0;line-height:1.7">{e(text)}</p></div><div class="cards reveal" data-d="1">{cards}</div></div>')
    body = page_hero(r, [('index.html', 'Головна')], 'Послуги', '14 практик — <em>одна команда</em>',
                     'Від податкової безпеки та міжнародних структур до судового захисту. Оберіть напрям, щоб побачити повний перелік послуг.', 'towers.jpg',
                     facts_box(r, [('Практик', '14', None), ('Напрямів', '4', None), ('Обговорити задачу', '', f'{r}kontakty.html#form')])) + f'''
<section class="section"><div class="container">{''.join(groups)}</div></section>
{mission(r)}{contacts_section(r)}'''
    write('praktyky/index.html', layout('praktyky/index.html', 'Послуги', 'Усі 14 практик Dictum Global: судова практика, податкова та митна безпека, корпоративне право, міжнародне структурування та інші.', body, 'practices', image='towers.jpg'))


def services_faq(item, r):
    items = []
    expert = f'<div class="expert"><span>Експерт: <b>Світлана Мороз</b>, керуючий партнер, адвокат, к.ю.н.</span><a class="link" href="{r}kontakty.html#form" style="min-height:auto">Замовити {ARROW}</a></div>'
    for c in item['cards']:
        if c['li']:
            body = '<ul>' + ''.join(f'<li>{e(x)}</li>' for x in c['li']) + '</ul>' + expert
        else:
            body = '<p style="margin:0">Деталі напряму обговоримо на консультації — розкажіть про вашу задачу.</p>' + expert
        items.append((c['t'], body))
    return items


def detail_page(item, r, crumbs, label, image, siblings, icon='doc'):
    intro = item['intro']
    lead = e(intro[0]) if intro else ''
    has_items = any(c['li'] for c in item['cards'])
    facts = facts_box(r, [('Напрямів роботи', str(len(item['cards'])), '#services'), ('Отримати консультацію', '', f'{r}kontakty.html#form')])
    body = page_hero(r, crumbs, label, e(item['title']), lead, image, facts)
    if len(intro) > 1:
        paras = ''.join(f'<p>{e(p)}</p>' for p in intro[1:])
        body += f'''<section class="section"><div class="container split" style="align-items:start">
  <div class="stack reveal"><span class="eyebrow">Наш підхід</span><h2 class="h2">Що <em>важливо</em> знати</h2></div>
  <div class="prose reveal" data-d="1">{paras}</div></div></section>'''
    if item['adv']:
        advs = ''.join(f'<div class="card reveal" data-d="{k}">{ico(["check","shield","chart"][k % 3], "ico")}<b>{e(t)}</b><span>{e(d)}</span></div>' for k, (t, d) in enumerate(item['adv']))
        body += f'<section class="section bg-2 bt"><div class="container">{head("Переваги", "Чому <em>Dictum</em>")}<div class="grid3">{advs}</div></div></section>'
    toggle = '<button class="btn btn--ghost" type="button" data-toggle-all="services-list">Розгорнути все</button>' if has_items and len(item['cards']) > 1 else ''
    body += f'''<section class="section bt" id="services"><div class="container">
  {head('Наші послуги', 'Що <em>ми робимо</em>', toggle)}
  {faq_block(services_faq(item, r), single=False, fid='services-list')}
</div></section>'''
    sib = [s for s in siblings if s['slug'] != item['slug']][:6]
    if sib:
        cards = ''.join(f'<a class="card" href="{s["slug"]}.html">{ico(PRACTICE_ICON.get(s["slug"], icon), "ico")}<b>{e(s["title"])}</b><span class="more">Детальніше →</span></a>' for s in sib)
        body += f'<section class="section bg-2 bt"><div class="container">{head("Також", "Суміжні <em>напрями</em>")}<div class="cards">{cards}</div></div></section>'
    body += mission(r) + contacts_section(r, 'Обговоримо <em>вашу задачу</em>')
    return body


def page_practice(p):
    r = '../'
    cl = CLUSTER_OF.get(p['slug'], 0)
    ordered = [P[s] for c in CLUSTERS for s in c[2]]
    sibs = [P[s] for s in CLUSTERS[cl][2]] + [x for x in ordered if CLUSTER_OF.get(x['slug']) != cl]
    image = 'map.jpg' if p['slug'] in ('mizhnarodne-strukturuvannya', 'suprovid-nerezydentiv', 'suprovid-investyzii') else 'towers.jpg'
    body = detail_page(p, r, [('index.html', 'Головна'), ('praktyky/index.html', 'Послуги')], p['title'], image, sibs)
    active = 'intl' if p['slug'] == 'mizhnarodne-strukturuvannya' else 'practices'
    write(f'praktyky/{p["slug"]}.html', layout(f'praktyky/{p["slug"]}.html', p['title'], (p['intro'][0] if p['intro'] else p['title'])[:155], body, active, image=image))


def page_industries_index():
    r = '../'
    cards = ''.join(f'<a class="card reveal" data-d="{k % 3}" href="{x["slug"]}.html"><span style="font-size:15px;font-weight:700;letter-spacing:.12em;color:var(--olive-text)">{k + 1:02d}</span><b style="font-size:20px;font-weight:600">{e(x["title"])}</b><span>{e(x["intro"][0][:120])}…</span><span class="more">Детальніше →</span></a>' for k, x in enumerate(INDUSTRIES))
    body = page_hero(r, [('index.html', 'Головна')], 'Галузі', 'Розуміємо <em>специфіку</em> вашої галузі',
                     'Консультуємо та захищаємо бізнес у 14 секторах економіки — з урахуванням галузевого регулювання та судової практики.', 'map.jpg',
                     facts_box(r, [('Секторів економіки', '14', None), ('Обговорити задачу', '', f'{r}kontakty.html#form')])) + f'''
<section class="section"><div class="container"><div class="cards" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr))">{cards}</div></div></section>
{mission(r)}{contacts_section(r)}'''
    write('haluzi/index.html', layout('haluzi/index.html', 'Галузі', 'Юридичний супровід бізнесу в 14 секторах економіки: промисловість, Retail & FMCG, нерухомість, енергетика, медицина, IT та інші.', body, 'industries', image='map.jpg'))


def page_industry(x):
    r = '../'
    body = detail_page(x, r, [('index.html', 'Головна'), ('haluzi/index.html', 'Галузі')], x['title'], 'towers.jpg', INDUSTRIES, icon='building')
    write(f'haluzi/{x["slug"]}.html', layout(f'haluzi/{x["slug"]}.html', x['title'], x['intro'][0][:155], body, 'industries', image='towers.jpg'))


def page_products_index():
    r = '../'
    icons = ['building', 'briefcase', 'user', 'shield']
    cards = ''.join(f'<a class="card reveal" data-d="{k % 2}" href="{p["slug"]}.html" style="min-height:260px">{ico(icons[k], "ico")}<b style="font-size:22px;font-weight:600">{e(p["title"])}</b><span style="font-size:15px">{e(PRODUCT_SHORT[p["slug"]])}</span><span class="more">Детальніше →</span></a>' for k, p in enumerate(PRODUCTS))
    body = page_hero(r, [('index.html', 'Головна')], 'Продукти', 'Формати <em>співпраці</em>',
                     'Готові моделі роботи з Dictum — від запуску компанії до постійного юридичного департаменту та навчання команди.', 'meeting.jpg',
                     facts_box(r, [('Готових форматів', '4', None), ('Підібрати формат', '', f'{r}kontakty.html#form')])) + f'''
<section class="section"><div class="container"><div class="grid2">{cards}</div></div></section>
{mission(r)}{contacts_section(r)}'''
    write('produkty/index.html', layout('produkty/index.html', 'Продукти', 'Продукти Dictum Global: оформлення бізнесу, зовнішній юридичний департамент, спеціаліст в офіс, тренінги з корпоративної безпеки.', body, 'products', image='meeting.jpg'))


def page_product(p):
    r = '../'
    body = detail_page(p, r, [('index.html', 'Головна'), ('produkty/index.html', 'Продукти')], p['title'], 'meeting.jpg', PRODUCTS, icon='briefcase')
    write(f'produkty/{p["slug"]}.html', layout(f'produkty/{p["slug"]}.html', p['title'], PRODUCT_SHORT[p['slug']], body, 'products', image='meeting.jpg'))


def initials(n):
    w = n.split()
    return (w[0][0] + w[-1][0]) if len(w) > 1 else w[0][0]


def page_about():
    r = ''
    person = lambda n, role: f'<article class="person reveal"><div class="person__photo"><span>{initials(n)}</span></div><h3>{e(n)}</h3><p>{e(role)}</p></article>'
    ua = ''.join(person(*x) for x in TEAM_UA[1:])
    tr = ''.join(person(*x) for x in TEAM_TR)
    body = page_hero(r, [('index.html', 'Головна')], 'Про компанію', 'Експертиза. <em>Довіра.</em> Результат.',
                     'Dictum — юридична компанія з офісами в Києві, Анталії та Стамбулі. 10 років супроводжуємо бізнес в Україні та 4 роки — у Туреччині.', 'towers.jpg',
                     facts_box(r, [(flag('ua', 22) + 'Років в Україні', '10', None), (flag('tr', 22) + 'Років у Туреччині', '4', None), ('Офіси', '3', None)])) + f'''
<section class="section"><div class="container split">
  <div class="frame reveal" style="aspect-ratio:5/4"><img src="img/meeting.jpg" alt="Переговорна кімната з документами та видом на місто" loading="lazy"><span class="frame__corner" aria-hidden="true"></span></div>
  <div class="stack reveal" data-d="1"><span class="eyebrow">Наш підхід</span><h2 class="h2">Стратегія, що <em>захищає</em> бізнес</h2>
  <p class="lead">Ми досліджуємо всі обставини справи, визначаємо ризики та слабкі місця, готуємо докази й процесуальні документи та формуємо ефективну стратегію для захисту інтересів клієнта в судах усіх юрисдикцій.</p>
  <div class="stats"><div><b>10</b><span>років в Україні</span></div><div><b>4</b><span>роки в Туреччині</span></div><div><b>14</b><span>практик</span></div><div><b>15</b><span>людей у команді</span></div></div></div>
</div></section>
<section class="section bg-2 bt" id="team"><div class="container">
  {head('Експерти', 'Наша команда <em>в Україні</em>')}
  <div class="lead-person reveal"><div class="person__photo"><span>СМ</span></div><div class="stack"><span class="eyebrow">Засновниця · керуючий партнер</span><h3 class="h2" style="font-size:clamp(36px,4vw,52px)">Світлана Мороз</h3><p class="lead">Адвокат, кандидат юридичних наук. ТОП-100 юристів України за версією «Юридичної газети» у податковому, митному, трудовому, інвестиційному праві та інтелектуальній власності (2020–2025). Співзасновниця Української бізнес-ради в Туреччині (UBC).</p><a class="btn" href="kontakty.html#form" style="align-self:flex-start">Записатися на зустріч {ARROW}</a></div></div>
  <div class="team">{ua}</div>
  <div style="height:96px"></div>
  {head('Türkiye', 'Наша команда <em>в Туреччині</em>')}
  <div class="team">{tr}</div>
</div></section>
<section class="section bt" id="awards"><div class="container">
  {head('Визнання', 'Нагороди <em>та рейтинги</em>')}
  <div class="reveal">
    <div class="award"><span class="award__y">2021–2025</span><span class="award__t">ТОП-50 юридичних фірм України</span><span class="award__d">За версіями видань «Юридична газета» та «Юридична практика».</span></div>
    <div class="award"><span class="award__y">2021–2025</span><span class="award__t">«Лідери ринку»</span><span class="award__d">Рейтинг видання «Юридична газета».</span></div>
    <div class="award"><span class="award__y">2020–2025</span><span class="award__t">ТОП-100 юристів України</span><span class="award__d">Рейтинг «Вибір клієнта» від «Юридичної газети»: Світлана Мороз — серед кращих юристів у податковому, митному, трудовому та інвестиційному праві, а також інтелектуальній власності.</span></div>
  </div>
</div></section>
<section class="section section--tight bg-2 bt"><div class="container head" style="margin:0">
  <div class="head__title"><span class="eyebrow">Кар’єра</span><h2 class="h2">Стати частиною <em>команди</em></h2><p class="lead">Чекаємо на ваше резюме.</p></div>
  <a class="btn" href="mailto:info@dictum.ua?subject=%D0%A0%D0%B5%D0%B7%D1%8E%D0%BC%D0%B5">Надіслати резюме {ARROW}</a>
</div></section>
{mission(r)}{contacts_section(r)}'''
    write('pro-nas.html', layout('pro-nas.html', 'Про компанію', 'Dictum Global: команда в Україні та Туреччині, підхід, нагороди та рейтинги.', body, 'about', image='towers.jpg'))


def page_clients():
    r = ''
    cards = ''.join(f'<article class="card reveal" data-d="{k % 3}" style="min-height:260px"><span class="avatar" aria-hidden="true">{e(initials(n))}</span><b style="font-size:20px;font-weight:600">{e(n)}</b>' + (f'<span style="font-size:14px;line-height:1.7">{e(d)}</span>' if d else '') + '</article>' for k, (n, d) in enumerate(CLIENTS))
    body = page_hero(r, [('index.html', 'Головна')], 'Клієнти', 'Серед тих, хто нам <em>довіряє</em>',
                     'Консультуємо та захищаємо бізнес у промисловості, Retail & FMCG, нерухомості, енергетиці, IT, креативних індустріях, медицині та сфері послуг.', 'meeting.jpg',
                     facts_box(r, [('Стати клієнтом', '', f'{r}kontakty.html#form')])) + f'''
<section class="section"><div class="container"><div class="cards" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr))">{cards}</div></div></section>
{mission(r)}{contacts_section(r)}'''
    write('klienty.html', layout('klienty.html', 'Клієнти', 'Клієнти Dictum Global: компанії з HoReCa, медицини, медіа, б’юті-сфери та бізнес-об’єднання.', body, 'about', image='meeting.jpg'))


def page_news():
    r = '../'
    chips = '<button class="chip" type="button" data-tag="all" aria-pressed="true">Усе</button>' + ''.join(f'<button class="chip" type="button" data-tag="{k}" aria-pressed="false">{v}</button>' for k, v in TAGS.items())
    rows = []
    for d, tag, t, s, href in NEWS:
        h = href if href.startswith('http') else href.replace('novyny/', '')
        rows.append(f'<a class="news-row" href="{h}" data-tag="{tag}"' + (' rel="noopener"' if href.startswith('http') else '') + f'><time datetime="{d}">{fdate(d)}</time><div><h3>{e(t)}</h3><p>{e(s)}</p></div><span class="tag">{TAGS[tag]}</span></a>')
    body = page_hero(r, [('index.html', 'Головна')], 'Новини', 'Аналітика <em>для власників</em>',
                     'Податкові зміни, міжнародне структурування, новини Dictum та Української бізнес-ради в Туреччині.', 'map.jpg',
                     facts_box(r, [('YouTube', '', 'https://www.youtube.com/@DictumLawCompany'), ('Facebook', '', 'https://www.facebook.com/dictum.law/')])) + f'''
<section class="section" data-news><div class="container">
  <div class="news-tools"><label class="search"><span>Пошук публікацій</span><input type="search" placeholder="Substance, КІК, UBC…"></label><div class="chips" role="group" aria-label="Рубрики">{chips}</div></div>
  <div>{''.join(rows)}</div>
  <p class="empty" hidden>Нічого не знайдено. Спробуйте інший запит.</p>
</div></section>
{mission(r)}{contacts_section(r)}'''
    write('novyny/index.html', layout('novyny/index.html', 'Новини та аналітика', 'Новини та аналітика Dictum Global: податки, Substance, КІК, SAF-T, Туреччина та UBC.', body, 'news', image='map.jpg'))


def page_article():
    r = '../'
    body = page_hero(r, [('index.html', 'Головна'), ('novyny/index.html', 'Новини')], 'Податки',
                     'SAF-T UA: нові правила податкового контролю — <em>до чого готуватися бізнесу?</em>',
                     'Світлана Мороз · <time datetime="2026-11-16">16 листопада 2026</time>', 'towers.jpg', '') + f'''
<article class="section"><div class="container"><div class="article">
  <p>SAF-T UA — це стандартизований файл бухгалтерських даних, який ДПС може запросити під час документальної перевірки. Великий платник податків має надати його не пізніше двох робочих днів після запиту — і за періоди, починаючи з 2024 року.</p>
  <p>Якщо облікова система до цього не готова, двох днів може не вистачити. Excel тут не врятує: файл подається тільки в XML і перевіряється за схемою ДПС.</p>
  <div class="callout"><span class="eyebrow">Прямий ефір</span><b>17 листопада о 16:00 — як підготувати бізнес до SAF-T UA</b><span>Спікери: Світлана Мороз — керуючий партнер Dictum, адвокат, к.ю.н.; Олена Широкова — MBA, CFO, бізнес-аналітик в IT, партнер аудиторської компанії, експерт з цифрової трансформації підприємств.</span></div>
  <h2>Що розберемо</h2>
  <ul>
    <li>Що таке SAF-T і як він працює в Португалії, Польщі, Норвегії та інших країнах</li>
    <li>З яких розділів складається файл SAF-T UA і які дані з обліку туди потрапляють</li>
    <li>XML, XSD та Excel-шаблони ДПС — що з цього подають, а що лише допомагає підготуватися</li>
    <li>Якою має бути облікова система (SAP, Microsoft Dynamics, Oracle, BAS та інші), щоб сформувати й перевірити файл</li>
    <li>Законодавча підстава, строки подання і штрафи</li>
    <li>Програмні рішення на українському ринку — що перевірити, перш ніж обирати</li>
  </ul>
  <p>Підготуйтеся до запиту ДПС заздалегідь, а не за два дні до дедлайну.</p>
  <div class="share"><span class="muted" style="margin-right:8px">Поділитися:</span>
    <a class="btn btn--ghost btn--sm" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdictum.ua%2Fnovyny%2Fsaf-t-ua.html" rel="noopener" target="_blank">Facebook</a>
    <a class="btn btn--ghost btn--sm" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdictum.ua%2Fnovyny%2Fsaf-t-ua.html" rel="noopener" target="_blank">LinkedIn</a>
    <a class="btn btn--ghost btn--sm" href="https://t.me/share/url?url=https%3A%2F%2Fdictum.ua%2Fnovyny%2Fsaf-t-ua.html" rel="noopener" target="_blank">Telegram</a>
    <button class="btn btn--ghost btn--sm" type="button" data-copy-link>Копіювати посилання</button>
  </div>
</div></div></article>
{contacts_section(r, 'Потрібна допомога <em>з SAF-T?</em>')}'''
    ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': 'SAF-T UA: нові правила податкового контролю — до чого готуватися бізнесу?',
          'datePublished': '2026-11-16', 'author': {'@type': 'Person', 'name': 'Світлана Мороз'}, 'publisher': {'@type': 'Organization', 'name': 'Dictum Global'}}
    write('novyny/saf-t-ua.html', layout('novyny/saf-t-ua.html', 'SAF-T UA: нові правила податкового контролю', 'SAF-T UA — стандартизований файл бухгалтерських даних, який ДПС може запросити під час перевірки. Що потрібно знати бізнесу.', body, 'news', jsonld=ld, image='towers.jpg'))


def page_contacts():
    r = ''
    offices = ''.join(f'<article class="office reveal" data-d="{k}"><div class="stack" style="gap:10px"><span class="eyebrow">{flag("ua" if c == "Україна" else "tr", 22)}{c}</span><h3>{t}</h3></div><div class="stack" style="gap:14px"><p>{e(a)}</p><a class="link" href="{e(m)}" rel="noopener" target="_blank">Відкрити на мапі {ARROW}</a></div></article>' for k, (t, c, a, m) in enumerate(OFFICES))
    body = page_hero(r, [('index.html', 'Головна')], 'Контакти', 'Розпочнімо <em>розмову</em>',
                     'Зателефонуйте, напишіть у месенджер або залиште заявку — ми зв’яжемося, щоб призначити зустріч з експертом.', 'briefcase.jpg',
                     facts_box(r, [('+38 (067) 829 58 06', '', 'tel:+380678295806'), ('+38 (066) 37 22 429', '', 'tel:+380663722429'), ('info@dictum.ua', '', 'mailto:info@dictum.ua')])) + f'''
<section class="section"><div class="container">{head('Офіси', 'Три міста — <em>одна команда</em>')}<div class="offices3">{offices}</div></div></section>
{contacts_section(r)}'''
    write('kontakty.html', layout('kontakty.html', 'Контакти', 'Контакти Dictum Global: офіси в Києві, Анталії та Стамбулі, телефони, email і форма запису на зустріч.', body, 'contacts', image='briefcase.jpg'))


def page_404():
    body = f'''<section class="page-hero" style="min-height:80vh">
  <div class="page-hero__media" aria-hidden="true"><img src="/img/hero.jpg" alt=""></div>
  <div class="container page-hero__inner"><div class="page-hero__copy"><span class="eyebrow eyebrow--line">Помилка 404</span><h1 class="h1">Цієї сторінки <em>не існує</em></h1><p class="lead">Можливо, її перенесли під час оновлення сайту.</p><a class="btn" href="/index.html" style="align-self:flex-start">На головну {ARROW}</a></div></div>
</section>'''
    html_ = layout('404.html', 'Сторінку не знайдено', 'Сторінку не знайдено.', body)
    for a in ('href="css/', 'src="js/', 'href="img/', 'href="index.html', 'href="pro-nas', 'href="praktyky/', 'href="haluzi/', 'href="produkty/', 'href="novyny/', 'href="kontakty', 'href="klienty'):
        html_ = html_.replace(a, a.replace('="', '="/'))
    write('404.html', html_)


def extras():
    urls = ['', 'praktyky/', 'haluzi/', 'produkty/', 'pro-nas.html', 'klienty.html', 'novyny/', 'novyny/saf-t-ua.html', 'kontakty.html']
    urls += [f'praktyky/{p["slug"]}.html' for p in PRACTICES] + [f'haluzi/{x["slug"]}.html' for x in INDUSTRIES] + [f'produkty/{x["slug"]}.html' for x in PRODUCTS]
    today = datetime.date.today().isoformat()
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}/{lang_prefix(l)}{u}</loc><lastmod>{today}</lastmod></url>\n' for l in LANGS for u in urls) + '</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    write('img/favicon.svg', LOGOMOD.favicon())


def load(lang):
    """Swap content globals to the given language (texts from *.{lang}.txt)."""
    global PRACTICES, INDUSTRIES, PRODUCTS, P
    sfx = '' if lang == 'uk' else '.' + lang
    PRACTICES = C.parse(f'practices{sfx}.txt') + C.parse(f'practices2{sfx}.txt')
    INDUSTRIES = C.parse(f'industries{sfx}.txt')
    PRODUCTS = C.parse(f'products{sfx}.txt')
    P = {p['slug']: p for p in PRACTICES}
    CUR['lang'] = lang


if __name__ == '__main__':
    for lang in LANGS:
        load(lang)
        page_home()
        page_practices_index()
        for p in [P[s] for c in CLUSTERS for s in c[2]]:
            page_practice(p)
        page_industries_index()
        for x in INDUSTRIES:
            page_industry(x)
        page_products_index()
        for x in PRODUCTS:
            page_product(x)
        page_about(); page_clients(); page_news(); page_article(); page_contacts()
    load('uk')
    page_404(); extras()
    print('built into', OUT, sum(len(f) for _, _, f in os.walk(OUT)), 'files')
