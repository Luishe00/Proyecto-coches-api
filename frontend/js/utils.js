/**
 * utils.js — Shared utilities used across all modules.
 * Kept separate to avoid circular imports between app.js, auth.js and cars.js.
 */

/**
 * Navigate to a hash route (e.g. '#catalog', '#favorites', '#login').
 */
export function navigate(hash) {
  window.location.hash = hash;
}

let _toastTimeout = null;

/**
 * Show a brief toast notification.
 * @param {string} msg
 * @param {'info'|'error'|'success'} type
 */
export function showToast(msg, type = 'info') {
  let toast = document.getElementById('toastNotification');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toastNotification';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.className = `toast toast--${type} visible`;
  clearTimeout(_toastTimeout);
  _toastTimeout = setTimeout(() => toast.classList.remove('visible'), 3000);
}
