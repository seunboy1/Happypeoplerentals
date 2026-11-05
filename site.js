/* Happy People Rentals: small enhancements. Every page works without this file. */
(function () {
  var header = document.querySelector('[data-header]');
  var burger = document.querySelector('[data-burger]');

  // Phone menu
  if (header && burger) {
    burger.addEventListener('click', function () {
      var open = header.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }

  // On the homepage the header is see-through over the video until you scroll past it
  if (header && document.body.classList.contains('has-hero')) {
    var onScroll = function () {
      header.classList.toggle('is-solid', window.scrollY > Math.max(120, window.innerHeight - 140));
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Hero video: respect reduced motion, and retry play on browsers that block autoplay
  var video = document.querySelector('.hero video');
  if (video) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      video.removeAttribute('autoplay');
      video.pause();
    } else {
      var play = function () { var p = video.play(); if (p && p.catch) p.catch(function () {}); };
      play();
      document.addEventListener('click', play, { once: true });
    }
  }

  // Sections fade up as they come into view
  var revealed = document.querySelectorAll('[data-reveal]');
  if (revealed.length && 'IntersectionObserver' in window) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); ro.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    revealed.forEach(function (el) { ro.observe(el); });
    // Safety net: never leave anything hidden
    setTimeout(function () { revealed.forEach(function (el) { el.classList.add('is-in'); }); }, 2500);
  } else {
    revealed.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Hero drifts slowly as you scroll (parallax), unless the visitor prefers reduced motion
  var heroMedia = document.querySelector('[data-hero-media]');
  var heroCopy = document.querySelector('[data-hero-copy]');
  if (heroMedia && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var ticking = false;
    var drift = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY || 0;
        heroMedia.style.transform = 'translateY(' + (y * 0.28).toFixed(1) + 'px) scale(' + (1 + Math.min(y, 800) * 0.00012).toFixed(4) + ')';
        if (heroCopy) {
          heroCopy.style.transform = 'translateY(' + (y * -0.1).toFixed(1) + 'px)';
          heroCopy.style.opacity = String(Math.max(0, 1 - y / 640));
        }
        ticking = false;
      });
    };
    window.addEventListener('scroll', drift, { passive: true });
    drift();
  }

  // Connect 4 board drops its pieces once, when it scrolls into view
  var board = document.querySelector('[data-board]');
  if (board && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) {
        board.classList.add('is-live');
        io.disconnect();
      }
    }, { threshold: 0.4 });
    io.observe(board);
  }

  // Quote form: tick the game or package chosen on another page (?game=... or ?package=...)
  var params = new URLSearchParams(window.location.search);
  var game = params.get('game');
  if (game) {
    document.querySelectorAll('input[name="games[]"]').forEach(function (box) {
      if (box.value.toLowerCase() === game.toLowerCase()) box.checked = true;
    });
  }
  var pkg = params.get('package');
  var pkgSelect = document.getElementById('q-pack');
  if (pkg && pkgSelect) {
    Array.prototype.forEach.call(pkgSelect.options, function (o) {
      if (o.value.toLowerCase() === pkg.toLowerCase()) pkgSelect.value = o.value;
    });
  }

  // Forms send to send-form.php and show a confirmation only once the email has gone out
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = {};
      new FormData(form).forEach(function (value, key) {
        if (key === 'games[]') { (data.games = data.games || []).push(value); }
        else { data[key] = value; }
      });
      var button = form.querySelector('[type="submit"]');
      var error = form.querySelector('[data-error]');
      button.disabled = true;
      button.textContent = 'Sending…';
      if (error) error.hidden = true;
      fetch(form.getAttribute('action'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (res) {
        return res.json().catch(function () { return { ok: false }; }).then(function (body) {
          if (!res.ok || !body.ok) throw new Error(body.error || 'failed');
        });
      }).then(function () {
        form.hidden = true;
        var done = form.parentNode.querySelector('[data-done]');
        if (done) { done.hidden = false; done.focus(); }
      }).catch(function () {
        button.disabled = false;
        button.textContent = button.getAttribute('data-label');
        if (error) error.hidden = false;
      });
    });
  });
})();
