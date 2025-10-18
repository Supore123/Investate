// Modular page loader for Investate
function loadPage(page) {
  fetch(page)
    .then(res => res.text())
    .then(html => {
      document.getElementById('main-content').innerHTML = html;
      if (window.afterPageLoad) window.afterPageLoad(page);
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
  loadPage(pageMap[screen] || 'search.html');
}

window.addEventListener('DOMContentLoaded', () => {
  showScreen('search');
});
