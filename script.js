<script>
  document.addEventListener('DOMContentLoaded', () => {
    // --- Helpers ---
    const createElement = (tag, attrs = {}, parent = document.body) => {
      const el = document.createElement(tag);
      Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
      parent.appendChild(el);
      return el;
    };

    // --- Scroll Progress Bar ---
    const progressBar = createElement('div', { id: 'scroll-progress' }, document.body);
    const updateProgress = () => {
      const scrollY = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;
      progressBar.style.width = `${pct}%`;
    };
    window.addEventListener('scroll', updateProgress);
    updateProgress();

    // --- Reveal-on-Scroll ---
    const revealObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // --- Theme Toggle ---
    const toggleBtn = createElement('button', { id: 'theme-toggle' }, document.body);
    toggleBtn.textContent = '🌗';
    Object.assign(toggleBtn.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '0.5rem',
      fontSize: '1.2rem',
      background: 'var(--neon-cyan)',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      zIndex: '1001'
    });

    const THEME_KEY = 'light-theme-enabled';
    const applyTheme = enabled => {
      document.documentElement.classList.toggle('light-theme', enabled);
      localStorage.setItem(THEME_KEY, enabled);
    };

    // Initialize theme from storage
    applyTheme(localStorage.getItem(THEME_KEY) === 'true');

    // Toggle handler
    toggleBtn.addEventListener('click', () => {
      const isLight = !document.documentElement.classList.contains('light-theme');
      applyTheme(isLight);
    });
  });
</script>