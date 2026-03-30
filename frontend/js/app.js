/**
 * app.js — SPA router, navigation guards and app shell.
 */

import { isLoggedIn, logout, refreshCurrentUser, getCachedUser, isSuperadmin } from './auth.js';
import { renderAuthView } from './auth.js';
import { renderCatalogView, renderFavoritesView } from './cars.js';
import { navigate } from './utils.js';

// ─── App shell ────────────────────────────────────────────────────────────────

function renderShell() {
  document.body.innerHTML = `
    <div id="app">
      <header class="site-header">
        <a href="#catalog" class="site-logo">
          <span class="logo-icon">🏎</span>
          <span class="logo-text">Car<span class="accent">Hub</span></span>
        </a>
        <nav class="site-nav" id="siteNav"></nav>
        <button class="nav-toggle" id="navToggle" aria-label="Menú">☰</button>
      </header>
      <main class="main-content" id="viewContainer"></main>
      <footer class="site-footer">
        <p>© ${new Date().getFullYear()} CarHub — Todos los derechos reservados</p>
      </footer>
    </div>
  `;

  // Mobile nav toggle
  document.getElementById('navToggle').addEventListener('click', () => {
    document.getElementById('siteNav').classList.toggle('open');
  });
}

function updateNav() {
  const nav = document.getElementById('siteNav');
  if (!nav) return;

  const user = getCachedUser();
  const loggedIn = isLoggedIn();

  nav.innerHTML = `
    ${loggedIn ? `
      <a href="#catalog" class="nav-link">Catálogo</a>
      <a href="#favorites" class="nav-link">❤️ Favoritos</a>
      ${isSuperadmin() ? `<span class="nav-badge">Admin</span>` : ''}
      <span class="nav-user">👤 ${user?.username || ''}</span>
      <button class="btn btn-outline btn-sm" id="logoutBtn">Salir</button>
    ` : `
      <a href="#login" class="nav-link">Iniciar sesión</a>
    `}
  `;

  document.getElementById('logoutBtn')?.addEventListener('click', () => {
    logout();
    updateNav();
  });
}

// ─── Router ───────────────────────────────────────────────────────────────────

async function handleRoute() {
  const hash = window.location.hash || '#catalog';
  const container = document.getElementById('viewContainer');
  if (!container) return;

  // Close any open modals on route change
  document.getElementById('carModal')?.remove();
  document.getElementById('carFormModal')?.remove();

  // Auth guard
  if (!isLoggedIn() && hash !== '#login') {
    navigate('#login');
    return;
  }

  updateNav();

  // Highlight active nav link
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === hash);
  });

  if (hash === '#login') {
    if (isLoggedIn()) { navigate('#catalog'); return; }
    renderAuthView(container);
    return;
  }

  if (hash === '#catalog') {
    await renderCatalogView(container);
    return;
  }

  if (hash === '#favorites') {
    await renderFavoritesView(container);
    return;
  }

  // 404 fallback
  container.innerHTML = `
    <div class="not-found animate-fade-in">
      <span>🚗</span>
      <h2>Página no encontrada</h2>
      <a href="#catalog" class="btn btn-primary">Ir al catálogo</a>
    </div>
  `;
}

// ─── Boot ─────────────────────────────────────────────────────────────────────

async function init() {
  renderShell();

  // Try to refresh user info if we have a token
  if (isLoggedIn()) {
    await refreshCurrentUser();
  }

  // Listen for hash changes
  window.addEventListener('hashchange', handleRoute);

  // Initial route
  await handleRoute();
}

init();
