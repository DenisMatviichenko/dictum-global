"""Переводить генератор сайту на тему v2 (усі сторінки, 4 мови). Резервні копії: *.v1-backup.py"""
import shutil, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for f in ['generate.py', 'i18n.py']:
    b = f.replace('.py', '.v1-backup.py')
    if not os.path.exists(b):
        shutil.copy(f, b)
g = open('generate.py', encoding='utf-8').read()

def rep(old, new, count=1):
    global g
    assert old in g, 'NOT FOUND: ' + old[:80]
    g = g.replace(old, new, count)

# ---- layout: шрифти, тема, кнопка в шапці
rep('<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">')
rep('<link rel="stylesheet" href="{r}css/style.css">', '<link rel="stylesheet" href="{r}css/style.css">\n<link rel="stylesheet" href="{r}css/theme-v2.css">')
rep('<meta name="theme-color" content="#0B0B0A">', '<meta name="theme-color" content="#0E1217">')
rep('<a class="btn btn--ghost" href="{r}kontakty.html#form">Зв’язатися з нами</a>', '<a class="btn btn--ghost" href="{r}kontakty.html#form">Записатись на консультацію</a>')

# ---- головна: картки напрямів у hero
rep("    strip_html = ''.join(", '''    SV = lambda d, c, sw='1.4': f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'
    hcards = ''.join(f'<a class="hcard" href="{h}">{ico(i, "i", sw="1.3")}<span>{t.replace("-<br>", "-").replace("<br>", " ")}</span>{SV("M5 12h14M13 6l6 6-6 6", "a", "1.8")}</a>' for t, i, h in strip)
    strip_html = ''.join(''')

start = g.index('<section class="hero" id="top">')
end = g.index('<section class="section" id="services"')
new_top = '''<section class="hx" id="top">
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
  <div class="facts2__map" aria-hidden="true"><img src="img/dg-map.jpg" alt="" loading="lazy">
    <svg viewBox="0 0 600 160" preserveAspectRatio="none"><path class="facts2__arc" d="M250 62 Q330 0 420 96"/><circle class="facts2__glow" cx="250" cy="62" r="4"/><circle class="facts2__glow" cx="420" cy="96" r="4"/></svg></div>
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

'''
g = g[:start] + new_top + g[end:]
rep('<section class="section" id="services" style="background:linear-gradient(180deg,#0B0B0A,#12100C 50%,#0B0B0A)">', '<section class="section" id="services">')
rep('<section class="section reviews" id="reviews">', '<section class="section reviews is-light" id="reviews">')
rep('<section class="section" id="cases">', '<section class="section is-light" id="cases">')
open('generate.py', 'w', encoding='utf-8').write(g)

# ---- переклади нових фраз
i = open('i18n.py', encoding='utf-8').read()
NEW = '''# --- theme v2
'Записатись на консультацію': ('Book a consultation', 'Danışmanlık randevusu alın', 'Записаться на консультацию'),
'Юридичний супровід бізнесу': ('Legal support for business', 'İşletmeler için hukuki destek', 'Юридическое сопровождение бизнеса'),
'в Україні та Туреччині': ('in Ukraine and Türkiye', 'Ukrayna ve Türkiye’de', 'в Украине и Турции'),
'Дізнатись більше': ('Learn more', 'Daha fazla bilgi', 'Узнать больше'),
'Dictum у цифрах': ('Dictum in numbers', 'Rakamlarla Dictum', 'Dictum в цифрах'),
'DICTUM — ваш партнер у світі міжнародного права': ('DICTUM — your partner in international law', 'DICTUM — uluslararası hukukta ortağınız', 'DICTUM — ваш партнёр в мире международного права'),
'Експертиза. Довіра. Результат.': ('Expertise. Trust. Results.', 'Uzmanlık. Güven. Sonuç.', 'Экспертиза. Доверие. Результат.'),
'Україна та Туреччина — в одній команді': ('Ukraine and Türkiye — one team', 'Ukrayna ve Türkiye — tek ekip', 'Украина и Турция — в одной команде'),
'Партнер особисто веде вашу справу': ('A partner personally handles your case', 'Dosyanızı bizzat bir ortak yürütür', 'Партнёр лично ведёт ваше дело'),
'ТОП-50 юрфірм України 2021–2025': ('TOP-50 law firms of Ukraine 2021–2025', 'Ukrayna’nın ilk 50 hukuk bürosu 2021–2025', 'ТОП-50 юрфирм Украины 2021–2025'),
'''
if "'Записатись на консультацію'" not in i:
    i = i.replace('D = {\n', 'D = {\n' + NEW, 1)
    open('i18n.py', 'w', encoding='utf-8').write(i)
print('patched')
