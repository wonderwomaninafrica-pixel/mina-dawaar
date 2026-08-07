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

  // sample reader — pages live in the HTML so crawlers get the whole sample,
  // and this only controls which one is on screen
  var book = document.getElementById('reader-book');
  if (book) {
    var pages = Array.prototype.slice.call(book.querySelectorAll('.book-page'));
    var prev = document.getElementById('prev-page');
    var next = document.getElementById('next-page');
    var now = document.getElementById('page-now');
    var current = 0;
    // pages ship visible so crawlers and text extractors get the whole sample;
    // the reader collapses them to one at a time only once JS is running
    pages.forEach(function (pg, i) { pg.hidden = i !== 0; });

    var show = function (i, dir) {
      if (i < 0 || i >= pages.length) { return; }
      pages[current].hidden = true;
      pages[current].classList.remove('turn-next', 'turn-prev');
      current = i;
      pages[current].hidden = false;
      if (dir) { pages[current].classList.add(dir === 1 ? 'turn-next' : 'turn-prev'); }
      if (now) { now.textContent = String(current + 1); }
      if (prev) { prev.disabled = current === 0; }
      if (next) { next.disabled = current === pages.length - 1; }
      var top = book.getBoundingClientRect().top + window.scrollY - 90;
      if (window.scrollY > top) { window.scrollTo({ top: top, behavior: 'smooth' }); }
    };

    if (prev) { prev.addEventListener('click', function () { show(current - 1, -1); }); }
    if (next) { next.addEventListener('click', function () { show(current + 1, 1); }); }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { show(current + 1, 1); }
      if (e.key === 'ArrowLeft') { show(current - 1, -1); }
    });

    var x0 = null;
    book.addEventListener('touchstart', function (e) { x0 = e.changedTouches[0].clientX; }, { passive: true });
    book.addEventListener('touchend', function (e) {
      if (x0 === null) { return; }
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) { show(current + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1); }
      x0 = null;
    }, { passive: true });

    show(0);
  }

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
