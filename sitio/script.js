(() => {
  const cmd = document.getElementById("typed-cmd");
  const phrases = [
    "cat manifiesto.txt",
    "desinstalar --software=mestizaje",
    "open soberania_cognitiva",
    "grep -i olvido ./cuerpo",
  ];

  let phraseIndex = 0;
  let charIndex = 0;
  let deleting = false;

  function tick() {
    if (!cmd) return;
    const current = phrases[phraseIndex];

    if (!deleting) {
      charIndex += 1;
      cmd.textContent = current.slice(0, charIndex);
      if (charIndex === current.length) {
        deleting = true;
        window.setTimeout(tick, 1600);
        return;
      }
      window.setTimeout(tick, 55);
      return;
    }

    charIndex -= 1;
    cmd.textContent = current.slice(0, charIndex);
    if (charIndex === 0) {
      deleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      window.setTimeout(tick, 320);
      return;
    }
    window.setTimeout(tick, 28);
  }

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (cmd) {
    if (reduce) {
      cmd.textContent = phrases[0];
    } else {
      tick();
    }
  }

  const reveals = document.querySelectorAll(
    ".section-head, .thesis-item, .audience-list li, .toc li, .price, .swatch, .quote, .distinction-panel"
  );
  reveals.forEach((el) => el.classList.add("reveal"));

  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14, rootMargin: "0px 0px -8% 0px" }
  );

  reveals.forEach((el) => io.observe(el));
})();
