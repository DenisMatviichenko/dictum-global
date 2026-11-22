import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'js', 'main.js')
s = open(p, encoding='utf-8').read()
BLOCK = r'''
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
'''
if 'var LOCKED' not in s:
    anchor = '  var DEMO = true;\n'
    assert anchor in s
    s = s.replace(anchor, anchor + BLOCK, 1)
    open(p, 'w', encoding='utf-8').write(s)
print('locked' if 'var LOCKED = true' in s else 'fail')
