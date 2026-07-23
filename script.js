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

  // book covers: subtle tilt toward the cursor, so they feel touchable
  document.querySelectorAll('.book-cover').forEach(function (cover) {
    cover.style.transition = 'transform .4s ease';
    cover.style.transformStyle = 'preserve-3d';
    cover.addEventListener('mousemove', function (e) {
      var rect = cover.getBoundingClientRect();
      var px = (e.clientX - rect.left) / rect.width - 0.5;
      var py = (e.clientY - rect.top) / rect.height - 0.5;
      cover.style.transition = 'transform .08s linear';
      cover.style.transform = 'perspective(900px) rotateY(' + (px * 9).toFixed(2) + 'deg) rotateX(' + (-py * 9).toFixed(2) + 'deg) scale(1.015)';
    });
    cover.addEventListener('mouseleave', function () {
      cover.style.transition = 'transform .5s cubic-bezier(.2,.7,.2,1)';
      cover.style.transform = '';
    });
  });

  // newsletter — submits to Formspree, with a real success/error check
  var form = document.querySelector('.stay-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var confirmEl = document.querySelector('.stay-confirm');
      var input = form.querySelector('input[name="email"]');
      var email = input ? input.value.trim() : '';
      if (email.length < 3) { return; }

      var submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) { submitBtn.disabled = true; }

      fetch(form.action, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      }).then(function (response) {
        if (response.ok) {
          if (confirmEl) { confirmEl.style.display = 'block'; }
          form.style.display = 'none';
        } else {
          if (submitBtn) { submitBtn.disabled = false; }
          if (confirmEl) {
            confirmEl.textContent = 'Something went wrong. Please try again.';
            confirmEl.style.display = 'block';
          }
        }
      }).catch(function () {
        if (submitBtn) { submitBtn.disabled = false; }
        if (confirmEl) {
          confirmEl.textContent = 'Something went wrong. Please try again.';
          confirmEl.style.display = 'block';
        }
      });
    });
  }
});
