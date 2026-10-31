document.addEventListener("DOMContentLoaded", () => {
  const viewport = document.getElementById("viewport");
  const track = document.getElementById("track");
  const next = document.getElementById("next");
  const prev = document.getElementById("prev");

  let cardWidth;

  function calculateWidth() {
    cardWidth = track.querySelector(".testimonial-card").offsetWidth + 24;
  }

  calculateWidth();
  window.addEventListener("resize", calculateWidth);

  const originals = [...track.children];
  originals.forEach(card => track.append(card.cloneNode(true)));
  originals.forEach(card => track.append(card.cloneNode(true)));

  const slides = [...track.children];
  viewport.scrollLeft = cardWidth * originals.length;

  function updateActive() {
    slides.forEach(card => card.classList.remove("active"));
    const index = Math.round(
      (viewport.scrollLeft + viewport.offsetWidth / 2) / cardWidth
    );
    slides[index]?.classList.add("active");
  }

  next.onclick = () => viewport.scrollBy({ left: cardWidth, behavior: "smooth" });
  prev.onclick = () => viewport.scrollBy({ left: -cardWidth, behavior: "smooth" });

  viewport.addEventListener("scroll", () => {
    const limit = cardWidth * originals.length;
    if (viewport.scrollLeft <= cardWidth) viewport.scrollLeft += limit;
    if (viewport.scrollLeft >= limit * 2) viewport.scrollLeft -= limit;
    updateActive();
  });

  updateActive();
});
