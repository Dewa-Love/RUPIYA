/* shared.js — RUPYA common scripts */
(function () {
  // ── NAV SCROLL ──
  window.addEventListener('scroll', () => document.getElementById('mainNav').classList.toggle('scrolled', window.scrollY > 60));

  // ── ACTIVE NAV LINK ──
  const cur = window.location.pathname.split('/').pop() || 'index.html';
  const loanPages = ['home-loan.html','personal-loan.html','car-loan.html','business-loan.html',
    'gold-loan.html','education-loan.html','lap-loan.html'];
  document.querySelectorAll('.nav-links a, .nm-link').forEach(a => {
    const href = a.getAttribute('href');
    if (href === cur) a.classList.add('active');
    if (loanPages.includes(cur) && a.classList.contains('nav-loans-trigger')) a.classList.add('active');
  });

  // ── SCROLL REVEAL ──
  const obs = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) e.target.classList.add('on'); }), { threshold: .08 });
  document.querySelectorAll('.reveal,.reveal-l,.reveal-r').forEach(el => obs.observe(el));

  // ── TOAST ──
  window.showToast = function (msg, type = '') {
    const t = document.getElementById('toast');
    t.textContent = msg; t.className = 'toast show ' + type;
    setTimeout(() => t.classList.remove('show'), 3200);
  };

  // ── FAQ ACCORDION ──
  window.toggleFaq = function (btn) { btn.parentElement.classList.toggle('open'); };

  // ── MOBILE NAV — uses inline style toggle so it always works ──
  const ham = document.getElementById('navHam');
  const mobileNav = document.getElementById('mobileNav');
  if (ham && mobileNav) {
    ham.addEventListener('click', () => {
      const isOpen = mobileNav.style.display === 'flex';
      mobileNav.style.display = isOpen ? 'none' : 'flex';
      ham.classList.toggle('open', !isOpen);
      document.body.style.overflow = isOpen ? '' : 'hidden';
    });
    mobileNav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      mobileNav.style.display = 'none';
      ham.classList.remove('open');
      document.body.style.overflow = '';
    }));
  }

  // ── HELPERS ──
  window.fmtINR = function (n) {
    if (n >= 10000000) return '₹' + (n / 10000000).toFixed(2) + ' Cr';
    if (n >= 100000) return '₹' + (n / 100000).toFixed(1) + 'L';
    if (n >= 1000) return '₹' + (n / 1000).toFixed(0) + 'K';
    return '₹' + n;
  };
  window.fmtFull = function (n) { return '₹' + Math.round(n).toLocaleString('en-IN'); };
})();
