/**
 * auth.js — Authentication logic, localStorage helpers, and auth views.
 */

import { apiLogin, apiRegister, apiGetMe } from './api.js';
import { navigate } from './utils.js';

const TOKEN_KEY = 'carhub_token';
const USER_KEY = 'carhub_user';
const ROLE_KEY = 'role';
export function getRole() {
  // Si hay usuario cacheado, prioriza su rol
  const user = getCachedUser();
  if (user && user.role) return user.role;
  // Si no, revisa localStorage
  return localStorage.getItem(ROLE_KEY) || null;
}

export function setRole(role) {
  localStorage.setItem(ROLE_KEY, role);
}

export function removeRole() {
  localStorage.removeItem(ROLE_KEY);
}

// ─── Token / User helpers ─────────────────────────────────────────────────────

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function isLoggedIn() {
  return !!getToken();
}

export function getCachedUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY));
  } catch (_) {
    return null;
  }
}

export function setCachedUser(user) {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function isSuperadmin() {
  const user = getCachedUser();
  return user && user.role === 'superadmin';
}

/**
 * Fetch the /me endpoint and cache the result.
 * Returns the user object or null on failure.
 */
export async function refreshCurrentUser() {
  try {
    const user = await apiGetMe();
    setCachedUser(user);
    return user;
  } catch (_) {
    removeToken();
    return null;
  }
}

export function logout() {
  removeToken();
  removeRole();
  navigate('#login');
}

// ─── Auth views ──────────────────────────────────────────────────────────────

/**
 * Render the login/register view into the given container element.
 */
export function renderAuthView(container) {
  container.innerHTML = `
    <section class="auth-section">
      <div class="auth-card glass-card animate-fade-in">
        <div class="auth-logo">
          <span class="logo-icon">🏎</span>
          <h1 class="logo-text">Car<span class="accent">Hub</span></h1>
          <p class="auth-tagline">La plataforma de coches de lujo</p>
        </div>

        <div class="auth-tabs">
          <button class="auth-tab active" data-tab="login">Iniciar sesión</button>
          <button class="auth-tab" data-tab="register">Registrarse</button>
        </div>

        <!-- LOGIN FORM -->
        <form id="loginForm" class="auth-form" autocomplete="off">
          <div class="form-group">
            <label for="loginUsername">Usuario</label>
            <input type="text" id="loginUsername" placeholder="Tu nombre de usuario" required />
          </div>
          <div class="form-group">
            <label for="loginPassword">Contraseña</label>
            <div class="input-password-wrap">
              <input type="password" id="loginPassword" placeholder="Tu contraseña" required />
              <button type="button" class="toggle-password" aria-label="Mostrar contraseña">👁</button>
            </div>
          </div>
          <div class="form-error" id="loginError"></div>
          <button type="submit" class="btn btn-primary btn-full" id="loginBtn">
            <span class="btn-text">Entrar</span>
            <span class="btn-loader hidden"></span>
          </button>
        </form>

        <!-- REGISTER FORM -->
        <form id="registerForm" class="auth-form hidden" autocomplete="off">
          <div class="form-group">
            <label for="regUsername">Usuario</label>
            <input type="text" id="regUsername" placeholder="Elige un nombre de usuario" required />
          </div>
          <div class="form-group">
            <label for="regPassword">Contraseña</label>
            <div class="input-password-wrap">
              <input type="password" id="regPassword" placeholder="Mínimo 8 caracteres" required minlength="8" />
              <button type="button" class="toggle-password" aria-label="Mostrar contraseña">👁</button>
            </div>
          </div>
          <div class="form-group">
            <label for="regPasswordConfirm">Confirmar contraseña</label>
            <input type="password" id="regPasswordConfirm" placeholder="Repite la contraseña" required />
          </div>
          <div class="form-error" id="registerError"></div>
          <button type="submit" class="btn btn-primary btn-full" id="registerBtn">
            <span class="btn-text">Crear cuenta</span>
            <span class="btn-loader hidden"></span>
          </button>
        </form>

        <div class="guest-access-row">
          <button id="guestAccessBtn" class="btn btn-secondary btn-full" type="button">Explorar como invitado</button>
        </div>
      </div>
    </section>
  `;

  _attachAuthEvents(container);
}

function _attachAuthEvents(container) {
  // Tab switching
  container.querySelectorAll('.auth-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      container.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.tab;
      container.querySelectorAll('.auth-form').forEach(f => f.classList.add('hidden'));
      container.querySelector(target === 'login' ? '#loginForm' : '#registerForm').classList.remove('hidden');
    });
  });

  // Toggle password visibility
  container.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.previousElementSibling;
      input.type = input.type === 'password' ? 'text' : 'password';
      btn.textContent = input.type === 'password' ? '👁' : '🙈';
    });
  });

  // Login submit
  container.querySelector('#loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = container.querySelector('#loginBtn');
    const errorEl = container.querySelector('#loginError');
    const username = container.querySelector('#loginUsername').value.trim();
    const password = container.querySelector('#loginPassword').value;

    errorEl.textContent = '';
    _setLoading(btn, true);

    try {
      const data = await apiLogin(username, password);
      setToken(data.access_token);
      await refreshCurrentUser();
      navigate('#catalog');
    } catch (err) {
      errorEl.textContent = err.message || 'Credenciales incorrectas';
    } finally {
      _setLoading(btn, false);
    }
  });

  // Register submit
  container.querySelector('#registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = container.querySelector('#registerBtn');
    const errorEl = container.querySelector('#registerError');
    const username = container.querySelector('#regUsername').value.trim();
    const password = container.querySelector('#regPassword').value;
    const confirm = container.querySelector('#regPasswordConfirm').value;

    errorEl.textContent = '';

    if (password !== confirm) {
      errorEl.textContent = 'Las contraseñas no coinciden';
      return;
    }

    _setLoading(btn, true);

    try {
      await apiRegister(username, password);
      // Auto-login after register
      const data = await apiLogin(username, password);
      setToken(data.access_token);
      await refreshCurrentUser();
      navigate('#catalog');
    } catch (err) {
      errorEl.textContent = err.message || 'Error al registrarse';
    } finally {
      _setLoading(btn, false);
    }
  });

  // Guest access
  container.querySelector('#guestAccessBtn').addEventListener('click', () => {
    removeToken();
    removeRole();
    setRole('guest');
    navigate('#catalog');
  });
}

function _setLoading(btn, loading) {
  btn.disabled = loading;
  btn.querySelector('.btn-text').classList.toggle('hidden', loading);
  btn.querySelector('.btn-loader').classList.toggle('hidden', !loading);
}
