document.addEventListener('DOMContentLoaded', function () {

  // nav background on scroll
  var nav = document.querySelector('.site-nav');
  var onScroll = function () {
    if (window.scrollY > 40) { nav.classList.add('is-scrolled'); }
    else { nav.classList.remove('is-scrolled'); }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('is-open');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { links.classList.remove('is-open'); });
    });
  }

  // reveal on scroll
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // newsletter (static demo — no backend)
  var form = document.querySelector('.stay-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var confirm = document.querySelector('.stay-confirm');
      var input = form.querySelector('input');
      if (input && input.value.trim().length > 2) {
        if (confirm) { confirm.style.display = 'block'; }
        form.style.display = 'none';
      }
    });
  }
});
