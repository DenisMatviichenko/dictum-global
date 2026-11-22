"""Тимчасові приклади відгуків (без імен реальних клієнтів), з позначкою «Приклад відгуку»."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
g = open('generate.py', encoding='utf-8').read()
s = g.index("    reviews = ''.join(f'''<figure class=\"review\"")
e = g.index("for k, (n, role) in enumerate(REVIEWS))", s) + len("for k, (n, role) in enumerate(REVIEWS))")
new = """    SAMPLES = [
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
</figure>''' for k, (t, n, role, ini) in enumerate(SAMPLES))"""
g = g[:s] + new + g[e:]
open('generate.py', 'w', encoding='utf-8').write(g)
i = open('i18n.py', encoding='utf-8').read()
ADD = """# --- review samples
'Приклад відгуку': ('Sample review', 'Örnek yorum', 'Пример отзыва'),
'Допомогли зареєструвати компанію в Туреччині та відкрити рахунки. Усе пояснили простою мовою й дотрималися термінів.': ('They helped us register a company in Türkiye and open bank accounts. Everything was explained in plain language and deadlines were met.', 'Türkiye’de şirket kurmamıza ve banka hesapları açmamıza yardımcı oldular. Her şeyi sade bir dille anlattılar ve sürelere uydular.', 'Помогли зарегистрировать компанию в Турции и открыть счета. Всё объяснили простым языком и уложились в сроки.'),
'Під час податкової перевірки команда була поруч із першого дня. Донарахування вдалося скасувати.': ('During the tax audit the team was with us from day one. The additional assessments were cancelled.', 'Vergi denetimi sırasında ekip ilk günden yanımızdaydı. Ek tarhiyatlar iptal edildi.', 'Во время налоговой проверки команда была рядом с первого дня. Доначисления удалось отменить.'),
'Працюємо з Dictum як із зовнішнім юрдепартаментом: швидкі відповіді, зрозумілі звіти й жодних сюрпризів.': ('We work with Dictum as our external legal department: quick answers, clear reports and no surprises.', 'Dictum ile dış hukuk departmanımız olarak çalışıyoruz: hızlı yanıtlar, anlaşılır raporlar ve sürpriz yok.', 'Работаем с Dictum как с внешним юрдепартаментом: быстрые ответы, понятные отчёты и никаких сюрпризов.'),
'Допомогли вибудувати структуру бізнесу між Україною та Туреччиною. Партнер особисто вів проєкт від початку до кінця.': ('They helped us structure our business between Ukraine and Türkiye. A partner personally led the project from start to finish.', 'Ukrayna ile Türkiye arasında iş yapımızı kurmamıza yardımcı oldular. Projeyi baştan sona bir ortak bizzat yürüttü.', 'Помогли выстроить структуру бизнеса между Украиной и Турцией. Партнёр лично вёл проект от начала до конца.'),
'Оперативно зняли арешт із рахунків і пояснили, як уникнути таких ризиків надалі.': ('They promptly lifted the freeze on our accounts and explained how to avoid such risks in future.', 'Hesaplarımızdaki blokeyi hızla kaldırdılar ve bu tür risklerden nasıl kaçınacağımızı anlattılar.', 'Оперативно сняли арест со счетов и объяснили, как избежать таких рисков в будущем.'),
'Супровід угоди з турецьким партнером пройшов спокійно: договір, перевірка контрагента, переговори.': ('Support for the deal with our Turkish partner went smoothly: the contract, counterparty check and negotiations.', 'Türk ortağımızla anlaşma süreci sorunsuz geçti: sözleşme, karşı taraf kontrolü ve müzakereler.', 'Сопровождение сделки с турецким партнёром прошло спокойно: договор, проверка контрагента, переговоры.'),
'Керівник IT-компанії': ('Head of an IT company', 'BT şirketi yöneticisi', 'Руководитель IT-компании'),
'IT · Київ — Стамбул': ('IT · Kyiv — Istanbul', 'BT · Kyiv — İstanbul', 'IT · Киев — Стамбул'),
'Фінансовий директор': ('Chief Financial Officer', 'Finans direktörü', 'Финансовый директор'),
'Імпорт обладнання': ('Equipment import', 'Ekipman ithalatı', 'Импорт оборудования'),
'Власниця бізнесу': ('Business owner', 'İşletme sahibi', 'Владелица бизнеса'),
'Б’юті-індустрія': ('Beauty industry', 'Güzellik sektörü', 'Бьюти-индустрия'),
'Засновник компанії': ('Company founder', 'Şirket kurucusu', 'Основатель компании'),
'Генеральний директор': ('CEO', 'Genel müdür', 'Генеральный директор'),
'Дистрибуція': ('Distribution', 'Dağıtım', 'Дистрибуция'),
'Комерційний директор': ('Commercial director', 'Ticari direktör', 'Коммерческий директор'),
'Виробництво': ('Manufacturing', 'Üretim', 'Производство'),
'ФД': ('CF', 'FD', 'ФД'), 'ВБ': ('BO', 'İS', 'ВБ'), 'ЗК': ('CF', 'ŞK', 'ОК'), 'ГД': ('CE', 'GM', 'ГД'), 'КД': ('CD', 'TD', 'КД'),
"""
if "'Приклад відгуку'" not in i:
    i = i.replace('# --- theme v2\n', ADD + '# --- theme v2\n', 1)
    open('i18n.py', 'w', encoding='utf-8').write(i)
print('reviews ok')
