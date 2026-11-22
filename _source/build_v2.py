"""Робить index-v2.html (нова тема) з поточного index.html, не чіпаючи оригінал."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
def ico(d, cls='i', sw='1.4'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'

# шрифти + тема
h = re.sub(r'<link href="https://fonts.googleapis.com/css2[^"]*" rel="stylesheet">',
           '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">', h)
h = h.replace('<link rel="stylesheet" href="css/style.css">', '<link rel="stylesheet" href="css/style.css">\n<link rel="stylesheet" href="css/theme-v2.css">')
h = h.replace('<meta name="theme-color" content="#0B0B0A">', '<meta name="theme-color" content="#0E1217">')
h = h.replace('<a class="btn btn--ghost" href="kontakty.html#form">Зв’язатися з нами</a>', '<a class="btn btn--ghost" href="kontakty.html#form">Записатись на консультацію</a>', 1)

# іконки з колишньої стрічки
strip = re.search(r'<section class="strip".*?</section>', h, re.S).group(0)
items = re.findall(r'<a class="strip__item" href="([^"]+)">(<svg.*?</svg>)<span>(.*?)</span></a>', strip, re.S)
cards = ''.join(
    f'<a class="hcard" href="{href}">{svg.replace("<svg ", "<svg class=\"i\" ", 1).replace("stroke-width=\"1.1\"", "stroke-width=\"1.3\"")}<span>{label.replace("-<br>", "-").replace("<br>", " ")}</span>{ico("M5 12h14M13 6l6 6-6 6", "a", "1.8")}</a>'
    for href, svg, label in items)

hero_new = f'''<section class="hx" id="top">
  <div class="hx__media" aria-hidden="true"><img src="img/dg-hero.jpg" alt="" fetchpriority="high"></div>
  <div class="hx__glass" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="container">
    <div class="hx__copy rise">
      <span class="eyebrow">Україна · Туреччина · міжнародні структури</span>
      <h1 class="h1">Юридичний супровід бізнесу <em>в Україні та Туреччині</em></h1>
      <p class="lead">Комплексні юридичні рішення для бізнесу без кордонів: 10 років в Україні, 4 роки в Туреччині.</p>
      <div class="hx__actions"><a class="btn" href="kontakty.html#form">Отримати консультацію {ARROW}</a><a class="play" href="#about"><i>{ico("M8 5l11 7-11 7z", "p", "1.6")}</i>Дізнатись більше</a></div>
    </div>
    <nav class="hx__cards" aria-label="Ключові напрями">{cards}</nav>
  </div>
</section>

<section class="facts2" aria-label="Dictum у цифрах">
  <div class="facts2__map" aria-hidden="true"><img src="img/dg-map.jpg" alt="" loading="lazy">
    <svg viewBox="0 0 600 160" preserveAspectRatio="none"><path class="facts2__arc" d="M250 62 Q330 0 420 96"/><circle class="facts2__glow" cx="250" cy="62" r="4"/><circle class="facts2__glow" cx="420" cy="96" r="4"/></svg></div>
  <div class="container">
    <p class="facts2__lead">DICTUM — ваш партнер у світі міжнародного права</p>
    <div class="facts2__item"><b>10+</b><span>років супроводу бізнесу в Україні</span></div>
    <div class="facts2__item"><b>4</b><span>роки практики в Туреччині</span></div>
    <div class="facts2__item"><b>3</b><span>офіси: Київ, Анталія, Стамбул</span></div>
    <div class="facts2__item"><b>ТОП-50</b><span>юрфірм України 2021–2025</span></div>
  </div>
</section>'''
h = re.sub(r'<section class="hero" id="top">.*?</section>\s*<section class="strip".*?</section>', lambda m: hero_new, h, count=1, flags=re.S)

about_new = f'''<section class="section about2 is-light" id="about">
  <div class="about2__img" aria-hidden="true"><img src="img/dg-building.jpg" alt="" loading="lazy"></div>
  <div class="container">
    <div class="about2__copy reveal">
      <span class="eyebrow">Про компанію</span>
      <h2 class="h2">Експертиза. Довіра. Результат.</h2>
      <p>Dictum — юридична компанія, яка поєднує глибоку експертизу в податковому, корпоративному та міжнародному праві, практичний досвід і персональний підхід до кожного клієнта. Ми ведемо бізнес в Україні та Туреччині однією командою.</p>
      <a class="btn btn--ghost" href="pro-nas.html">Більше про компанію {ARROW}</a>
    </div>
    <ul class="about2__list reveal" data-d="1">
      <li><i>{ico("M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18", "x", "1.5")}</i>Україна та Туреччина — в одній команді</li>
      <li><i>{ico("M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0", "x", "1.5")}</i>Партнер особисто веде вашу справу</li>
      <li><i>{ico("M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM8.5 12l2.5 2.5 4.5-5", "x", "1.5")}</i>ТОП-50 юрфірм України 2021–2025</li>
    </ul>
  </div>
</section>'''
h = re.sub(r'<section class="section" id="about">.*?</section>', lambda m: about_new, h, count=1, flags=re.S)

# фон послуг — з теми; кейси — світлі
h = h.replace('<section class="section" id="services" style="background:linear-gradient(180deg,#0B0B0A,#12100C 50%,#0B0B0A)">', '<section class="section" id="services">')
h = h.replace('<section class="section reviews" id="reviews">', '<section class="section reviews is-light" id="reviews">')
h = h.replace('<section class="section" id="cases">', '<section class="section is-light" id="cases">')
open(dst, 'w', encoding='utf-8').write(h)
print('ok', len(h))
