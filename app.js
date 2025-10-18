// Modular page loader for Investate

function loadPage(page) {
  fetch(page)
    .then(res => res.text())
    .then(html => {
      const main = document.getElementById('main-content');
      main.innerHTML = html;
      // remove .active from any existing screens (including main-menu)
      document.querySelectorAll('.screen.active').forEach(s => s.classList.remove('active'));
      // If the loaded page has a .screen element, mark it active so CSS shows it
      const injectedScreen = main.querySelector('.screen');
      if (injectedScreen) injectedScreen.classList.add('active');
      // Call page-specific init if it exists
      if (page.includes('search') && typeof window.initSearchPage === 'function') {
        window.initSearchPage();
      }
      if (page.includes('favorites') && typeof window.initFavoritesPage === 'function') {
        window.initFavoritesPage();
      }
      if (page.includes('analytics') && !page.includes('property_analytics') && typeof window.initAnalyticsPage === 'function') {
        window.initAnalyticsPage();
      }
      if (page.includes('settings') && typeof window.initSettingsPage === 'function') {
        window.initSettingsPage();
      }
      if (page.includes('property_analytics') && typeof window.initPropertyAnalyticsPage === 'function') {
        window.initPropertyAnalyticsPage();
      }
    });
}

function showScreen(screen) {
  const pageMap = {
    'search': 'search.html',
    'favorites': 'favorites.html',
    'analytics': 'analytics.html',
    'settings': 'settings.html',
    'property-analytics': 'property_analytics.html',
    'main-menu': 'search.html'
  };
  loadPage(pageMap[screen]);
}

window.addEventListener('DOMContentLoaded', () => {
  // Inject mobile stylesheet for iPhone-like appearance
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'mobile.css';
  document.head.appendChild(link);
  showScreen('search');
});
