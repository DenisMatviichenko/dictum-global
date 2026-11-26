/* DICTUM GLOBAL — interactions (no dependencies) */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  /* ---- Translations of script messages (by <html lang>) ---- */
  var I18N = {"uk": {"close": "Закрити меню", "open": "Відкрити меню", "review": "Відгук ", "collapse": "Згорнути все", "expand": "Розгорнути все", "subject": "Заявка з сайту Dictum", "consent": "Потрібна ваша згода", "required": "Заповніть це поле", "email": "Перевірте email", "phone": "Перевірте номер телефону", "check": "Будь ласка, перевірте позначені поля.", "sending": "Надсилаємо…", "mail": "Відкриваємо ваш поштовий застосунок…", "thanks": "Дякуємо! Ми зв’яжемося з вами найближчим часом.", "fail": "Не вдалося надіслати. Зателефонуйте: +38 (067) 829 58 06.", "demo": "Демо-версія сайту: зв’язок поки не підключено", "copied": "Скопійовано"}, "en": {"close": "Close menu", "open": "Open menu", "review": "Review ", "collapse": "Collapse all", "expand": "Expand all", "subject": "Request from the Dictum website", "consent": "Your consent is required", "required": "Please fill in this field", "email": "Please check the email", "phone": "Please check the phone number", "check": "Please check the highlighted fields.", "sending": "Sending…", "mail": "Opening your email app…", "thanks": "Thank you! We will contact you shortly.", "fail": "Could not send. Please call: +38 (067) 829 58 06.", "demo": "Demo version of the site: contact is not connected yet", "copied": "Copied"}, "tr": {"close": "Menüyü kapat", "open": "Menüyü aç", "review": "Yorum ", "collapse": "Tümünü kapat", "expand": "Tümünü aç", "subject": "Dictum web sitesinden talep", "consent": "Onayınız gerekli", "required": "Lütfen bu alanı doldurun", "email": "E-postayı kontrol edin", "phone": "Telefon numarasını kontrol edin", "check": "Lütfen işaretli alanları kontrol edin.", "sending": "Gönderiliyor…", "mail": "E-posta uygulamanız açılıyor…", "thanks": "Teşekkürler! En kısa sürede sizinle iletişime geçeceğiz.", "fail": "Gönderilemedi. Lütfen arayın: +38 (067) 829 58 06.", "demo": "Sitenin demo sürümü: iletişim henüz bağlı değil", "copied": "Kopyalandı"}, "ru": {"close": "Закрыть меню", "open": "Открыть меню", "review": "Отзыв ", "collapse": "Свернуть всё", "expand": "Развернуть всё", "subject": "Заявка с сайта Dictum", "consent": "Требуется ваше согласие", "required": "Заполните это поле", "email": "Проверьте email", "phone": "Проверьте номер телефона", "check": "Пожалуйста, проверьте отмеченные поля.", "sending": "Отправляем…", "mail": "Открываем ваше почтовое приложение…", "thanks": "Спасибо! Мы свяжемся с вами в ближайшее время.", "fail": "Не удалось отправить. Позвоните: +38 (067) 829 58 06.", "demo": "Демо-версия сайта: связь пока не подключена", "copied": "Скопировано"}};
  var LANG = (document.documentElement.lang || 'uk').slice(0, 2);
  function L(k) { return (I18N[LANG] && I18N[LANG][k]) || I18N.uk[k] || k; }

  /* ДЕМО-РЕЖИМ: сайт лише показує вигляд.
     true  → форми нічого не надсилають, а телефони/пошта/месенджери нічого не відкривають.
     false → звичайна робота (форми за data-endpoint, посилання tel:/mailto: працюють). */
  var DEMO = true;

  /* ЗАКРИТИЙ РЕЖИМ: поки відкрита лише головна сторінка українською.
     true  → інші сторінки, розділи меню й перемикач мов заблоковані (відкриття будь-якої іншої сторінки веде на головну).
     false → увесь сайт і всі мови доступні. */
  var LOCKED = true;
  if (LOCKED) {
    var meScript = document.querySelector('script[src$="js/main.js"]');
    var ROOT = new URL('..', meScript ? meScript.src : location.href).href;
    var HOMES = [ROOT, ROOT + 'index.html'];
    var clean = function (u) { return u.split('#')[0].split('?')[0]; };
    if (HOMES.indexOf(clean(location.href)) < 0) { location.replace(ROOT + 'index.html'); return; }
    document.documentElement.classList.add('is-locked');
    var lockToast = document.createElement('div');
    lockToast.setAttribute('role', 'status');
    lockToast.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);z-index:95;padding:12px 20px;border-radius:999px;background:#141A21;border:1px solid rgba(169,190,90,.5);color:#DCE5B5;font-size:14px;opacity:0;transition:opacity .3s,transform .3s;pointer-events:none;white-space:nowrap';
    document.body.appendChild(lockToast);
    var lockT = null;
    var lockSay = function (t) {
      lockToast.textContent = t; lockToast.style.opacity = '1'; lockToast.style.transform = 'translateX(-50%)';
      clearTimeout(lockT); lockT = setTimeout(function () { lockToast.style.opacity = '0'; lockToast.style.transform = 'translateX(-50%) translateY(20px)'; }, 2200);
    };
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]'); if (!a) return;
      var href = a.getAttribute('href');
      if (/^(#|tel:|mailto:|viber:)/.test(href)) return;
      var u = new URL(href, location.href);
      var internal = u.href.indexOf(ROOT) === 0 || /(^|\.)dictum\.ua$/.test(u.hostname);
      if (!internal) return;
      if (HOMES.indexOf(clean(u.href)) >= 0) return;
      e.preventDefault(); e.stopPropagation();
      if (/kontakty\.html$/.test(clean(u.href))) {
        var burger = document.querySelector('.burger[aria-expanded="true"]'); if (burger) burger.click();
        var target = document.getElementById('form') || document.getElementById('contacts');
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
      }
      lockSay(a.closest('.lang') ? 'Інші мови скоро будуть доступні' : 'Розділ скоро буде доступний');
    }, true);
  }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var store = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---- Hero brand title: stretch "GLOBAL LAW COMPANY" to the width of "Dictum" ---- */
  function fitBrand() {
    var main = document.querySelector('.brand-title__main'), sub = document.querySelector('.brand-title__sub');
    if (!main || !sub) return;
    sub.style.letterSpacing = '0px'; sub.style.marginRight = '0px';
    var fs = parseFloat(getComputedStyle(sub).fontSize) || 16;
    var n = sub.textContent.length;
    var extra = main.getBoundingClientRect().width - sub.getBoundingClientRect().width;
    var ls = Math.max(0, extra / Math.max(1, n - 1));
    sub.style.letterSpacing = (ls / fs) + 'em';
    sub.style.marginRight = (-ls / fs) + 'em';
  }
  fitBrand();
  window.addEventListener('resize', fitBrand);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitBrand);

  /* ---- Header ---- */
  var header = document.querySelector('.site-header');
  function onScrollHeader() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 24); }
  onScrollHeader();
  window.addEventListener('scroll', onScrollHeader, { passive: true });

  /* ---- Mobile menu ---- */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('mobile-menu');
  function setMenu(open) {
    if (!burger || !menu) return;
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? L('close') : L('open'));
    menu.classList.toggle('is-open', open);
    menu.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('menu-open', open);
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('is-open')) { setMenu(false); burger.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 1024) setMenu(false); });
  }

  /* ---- Reveal ---- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add('is-in'); }); }

  /* ---- Reviews carousel ---- */
  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var track = root.querySelector('.carousel__track');
    var slides = Array.prototype.slice.call(track.children);
    var prev = root.querySelector('[data-prev]');
    var next = root.querySelector('[data-next]');
    var count = root.querySelector('.carousel__count');
    var dotsWrap = root.querySelector('.dots');
    var i = 0, timer = null;
    var dots = slides.map(function (s, k) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', L('review') + (k + 1));
      b.innerHTML = '<span></span>';
      b.addEventListener('click', function () { go(k); restart(); });
      dotsWrap.appendChild(b);
      return b;
    });
    function perView() { return window.innerWidth <= 680 ? 1 : window.innerWidth <= 1024 ? 2 : 3; }
    function go(k) {
      var n = slides.length, pv = perView(), max = Math.max(0, n - pv);
      i = (k + n) % n;
      var pos = Math.min(i, max);
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 18;
      var w = slides[0].getBoundingClientRect().width + gap;
      track.style.transform = 'translateX(' + (-pos * w) + 'px)';
      slides.forEach(function (s, k2) {
        s.classList.toggle('is-active', k2 === i);
        s.setAttribute('aria-hidden', String(k2 < pos || k2 >= pos + pv));
      });
      dots.forEach(function (d, k2) { d.setAttribute('aria-current', String(k2 === i)); });
      if (count) count.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0');
    }
    function restart() {
      if (reduce) return;
      clearInterval(timer);
      timer = setInterval(function () { go(i + 1); }, 7000);
    }
    prev.addEventListener('click', function () { go(i - 1); restart(); });
    next.addEventListener('click', function () { go(i + 1); restart(); });
    root.addEventListener('mouseenter', function () { clearInterval(timer); });
    root.addEventListener('mouseleave', restart);
    root.addEventListener('focusin', function () { clearInterval(timer); });
    var sx = null;
    track.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 40) { go(i + (dx < 0 ? 1 : -1)); restart(); }
      sx = null;
    });
    window.addEventListener('resize', function () { go(i); });
    go(0); restart();
  });

  /* ---- FAQ: one open at a time ---- */
  document.querySelectorAll('[data-single]').forEach(function (root) {
    root.addEventListener('toggle', function (e) {
      if (e.target.open) root.querySelectorAll('details[open]').forEach(function (d) { if (d !== e.target) d.open = false; });
    }, true);
  });
  document.querySelectorAll('[data-toggle-all]').forEach(function (btn) {
    var root = document.getElementById(btn.getAttribute('data-toggle-all'));
    btn.addEventListener('click', function () {
      var ds = root.querySelectorAll('details');
      var anyClosed = Array.prototype.some.call(ds, function (d) { return !d.open; });
      ds.forEach(function (d) { d.open = anyClosed; });
      btn.textContent = anyClosed ? L('collapse') : L('expand');
    });
  });

  /* ---- News filter ---- */
  var news = document.querySelector('[data-news]');
  if (news) {
    var input = news.querySelector('input[type="search"]');
    var chips = news.querySelectorAll('.chip');
    var rows = news.querySelectorAll('.news-row');
    var empty = news.querySelector('.empty');
    var tag = 'all';
    var apply = function () {
      var q = (input.value || '').trim().toLowerCase(), shown = 0;
      rows.forEach(function (r) {
        var ok = (tag === 'all' || r.getAttribute('data-tag') === tag) && (!q || r.textContent.toLowerCase().indexOf(q) !== -1);
        r.hidden = !ok; if (ok) shown++;
      });
      empty.hidden = shown !== 0;
    };
    input.addEventListener('input', apply);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        tag = c.getAttribute('data-tag');
        chips.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
        apply();
      });
    });
  }

  /* ---- Forms ----
     Put your backend URL into data-endpoint (Formspree, PHP mailer, CRM webhook).
     Empty endpoint → the visitor's mail client opens with a prefilled message. */
  function sendForm(form, done) {
    if (DEMO) { setTimeout(function () { done(true); }, 400); return; }
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    data.page = location.href;
    var endpoint = form.getAttribute('data-endpoint');
    if (endpoint) {
      return fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); done(true); })
        .catch(function () { done(false); });
    }
    var body = Object.keys(data).filter(function (k) { return k !== 'consent'; }).map(function (k) { return k + ': ' + data[k]; }).join('\n');
    window.location.href = 'mailto:info@dictum.ua?subject=' + encodeURIComponent(L('subject')) + '&body=' + encodeURIComponent(body);
    done(true, true);
  }
  function validate(form) {
    var ok = true, first = null;
    form.querySelectorAll('[required]').forEach(function (el) {
      var msg = '';
      if (el.type === 'checkbox') { if (!el.checked) msg = L('consent'); }
      else if (!el.value.trim()) msg = L('required');
      else if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim())) msg = L('email');
      else if (el.type === 'tel' && el.value.replace(/\D/g, '').length < 9) msg = L('phone');
      var wrap = el.closest('.field') || el.closest('.check');
      if (wrap) {
        wrap.classList.toggle('is-invalid', !!msg);
        var err = wrap.querySelector('.field__err'); if (err) err.textContent = msg;
      }
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (msg) { ok = false; if (!first) first = el; }
    });
    if (first) first.focus();
    return ok;
  }
  document.querySelectorAll('form[data-contact]').forEach(function (form) {
    var status = form.querySelector('.form__status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(form)) { if (status) status.textContent = L('check'); return; }
      if (status) status.textContent = L('sending');
      sendForm(form, function (ok, mail) {
        if (!status) return;
        status.textContent = mail ? L('mail') : ok ? L('thanks') : L('fail');
        if (ok && !mail) form.reset();
      });
    });
  });

  /* ---- Scroll tip ---- */
  var tip = document.getElementById('tip');
  var fab = document.getElementById('tip-fab');
  if (tip && fab) {
    var shown = false;
    var open = function () {
      tip.classList.add('is-open'); tip.setAttribute('aria-hidden', 'false');
      fab.classList.remove('is-visible'); shown = true;
    };
    var close = function () {
      tip.classList.remove('is-open'); tip.setAttribute('aria-hidden', 'true');
      fab.classList.add('is-visible'); store.set('dg-tip', 'closed');
    };
    var maybe = function () {
      if (shown || store.get('dg-tip') === 'closed') return;
      if (window.scrollY > 500) open();
    };
    /* AUTO_TIP: true → підказка сама виринає при прокручуванні / через 6 с; false → лише по кнопці-значку. */
    var AUTO_TIP = false;
    if (!AUTO_TIP || store.get('dg-tip') === 'closed') fab.classList.add('is-visible');
    else {
      window.addEventListener('scroll', maybe, { passive: true });
      setTimeout(function () { if (!shown && store.get('dg-tip') !== 'closed') open(); }, 6000);
    }
    tip.querySelector('.tip__close').addEventListener('click', close);
    fab.addEventListener('click', open);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && tip.classList.contains('is-open')) close(); });
    var tf = tip.querySelector('form');
    tf.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(tf)) return;
      sendForm(tf, function (ok, mail) {
        var d = tip.querySelector('.tip__done');
        d.hidden = false;
        d.textContent = mail ? L('mail') : ok ? L('thanks') : L('fail');
        if (ok && !mail) { tf.hidden = true; store.set('dg-tip', 'closed'); }
      });
    });
  }

  /* ---- Demo: contact links do nothing ---- */
  if (DEMO) {
    var toast = document.createElement('div');
    toast.setAttribute('role', 'status');
    toast.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);z-index:90;padding:12px 18px;border-radius:999px;background:#161A0D;border:1px solid #4A5524;color:#C3D47A;font-size:14px;opacity:0;transition:opacity .3s,transform .3s;pointer-events:none';
    document.body.appendChild(toast);
    var tt = null;
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="tel:"], a[href^="mailto:"], a[href^="viber:"], a[href*="t.me/"], a[href*="wa.me/"]');
      if (!a) return;
      e.preventDefault();
      toast.textContent = L('demo');
      toast.style.opacity = '1'; toast.style.transform = 'translateX(-50%)';
      clearTimeout(tt); tt = setTimeout(function () { toast.style.opacity = '0'; toast.style.transform = 'translateX(-50%) translateY(20px)'; }, 2200);
    }, true);
  }

  /* ---- Copy link ---- */
  document.querySelectorAll('[data-copy-link]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!navigator.clipboard) return;
      navigator.clipboard.writeText(location.href).then(function () {
        var t = b.textContent; b.textContent = L('copied'); setTimeout(function () { b.textContent = t; }, 1600);
      });
    });
  });

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
