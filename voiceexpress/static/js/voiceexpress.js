const themeToggle = document.querySelector('[data-toggle-theme]');
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const html = document.documentElement;
    const next = html.dataset.theme === 'dark' ? 'light' : 'dark';
    html.dataset.theme = next;
    localStorage.setItem('voiceexpress-theme', next);
  });
}

const savedTheme = localStorage.getItem('voiceexpress-theme');
if (savedTheme) {
  document.documentElement.dataset.theme = savedTheme;
}

const carousel = document.querySelector('[data-carousel]');
if (carousel) {
  const track = carousel.querySelector('.carousel-track');
  carousel.querySelector('[data-carousel-prev]').addEventListener('click', () => {
    track.scrollBy({ left: -260, behavior: 'smooth' });
  });
  carousel.querySelector('[data-carousel-next]').addEventListener('click', () => {
    track.scrollBy({ left: 260, behavior: 'smooth' });
  });
}

const report = document.querySelector('[data-report]');
if (report) {
  const buttons = report.querySelectorAll('.report-controls button');
  const annotations = report.querySelector('[data-annotations]');
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      buttons.forEach((btn) => btn.classList.remove('active'));
      button.classList.add('active');
      const mode = button.dataset.layer;
      annotations.style.display = mode === 'research' ? 'block' : 'none';
    });
  });
}

const zineToggle = document.querySelector('[data-zine-toggle]');
if (zineToggle) {
  zineToggle.addEventListener('click', () => {
    const spreads = document.querySelector('[data-zine-spreads]');
    spreads.classList.toggle('active');
  });
}

const photoViewer = document.querySelector('[data-photo-viewer]');
if (photoViewer) {
  const buttons = photoViewer.querySelectorAll('.photo-modes button');
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      buttons.forEach((btn) => btn.classList.remove('active'));
      button.classList.add('active');
      photoViewer.dataset.mode = button.dataset.mode;
    });
  });
}

const highlightKey = 'voiceexpress-highlights';
const highlightable = document.querySelectorAll('.article .body, .report-body');
highlightable.forEach((section) => {
  section.addEventListener('mouseup', () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    if (text.length > 3) {
      const notes = JSON.parse(localStorage.getItem(highlightKey) || '[]');
      notes.push({ text, time: new Date().toISOString() });
      localStorage.setItem(highlightKey, JSON.stringify(notes));
    }
  });
});
