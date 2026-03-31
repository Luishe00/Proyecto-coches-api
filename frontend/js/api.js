/**
 * api.js — Centralised API client for CarHub.
 * Wraps every fetch call, injects the Bearer token and normalises errors.
 */

export const API_BASE = 'http://localhost:8000/api/v1';
export const API_ORIGIN = new URL(API_BASE).origin;

/**
 * Core fetch wrapper.
 * @param {string} endpoint  - Path relative to API_BASE (e.g. '/cars/')
 * @param {RequestInit} opts - Standard fetch options (method, body, headers…)
 * @returns {Promise<any>}   - Parsed JSON response
 */
async function request(endpoint, opts = {}) {
  const token = localStorage.getItem('carhub_token');

  const headers = {
    ...(opts.headers || {}),
  };

  const hasContentType = Object.keys(headers).some(
    (key) => key.toLowerCase() === 'content-type'
  );

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Only set JSON when caller did not provide a specific content type.
  if (
    !(opts.body instanceof FormData) &&
    opts.body &&
    typeof opts.body === 'string' &&
    !hasContentType
  ) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...opts,
    headers,
  });

  if (!response.ok) {
    let errorDetail = `HTTP ${response.status}`;
    try {
      const data = await response.json();
      errorDetail = data.detail || JSON.stringify(data);
    } catch (_) {
      // ignore parse errors
    }
    const err = new Error(errorDetail);
    err.status = response.status;
    throw err;
  }

  // 204 No Content
  if (response.status === 204) return null;

  return response.json();
}

// ─── Auth ────────────────────────────────────────────────────────────────────

/**
 * Authenticate and return { access_token, token_type }.
 * The /login endpoint requires application/x-www-form-urlencoded.
 */
export function apiLogin(username, password) {
  const body = new URLSearchParams({ username, password });
  return request('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
}

/**
 * Register a new user and return UserOut.
 */
export function apiRegister(username, password) {
  return request('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
}

/**
 * Fetch the currently authenticated user.
 */
export function apiGetMe() {
  return request('/auth/me');
}

// ─── Cars ─────────────────────────────────────────────────────────────────────

/**
 * List cars with optional filters.
 * @param {Object} filters - { marca, modelo, anio_min, anio_max, precio_max, velocidad_min, color_fabrica, skip, limit }
 */
export function apiGetCars(filters = {}) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') params.append(k, v);
  });
  const qs = params.toString();
  return request(`/cars/${qs ? `?${qs}` : ''}`);
}

/**
 * Get a single car by id.
 */
export function apiGetCar(id) {
  return request(`/cars/${id}`);
}

/**
 * Create a new car (superadmin only).
 */
export function apiCreateCar(data) {
  return request('/cars/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

function buildCarPayloadFromFormData(formData) {
  return {
    marca: String(formData.get('marca') || '').trim(),
    modelo: String(formData.get('modelo') || '').trim(),
    anio_fabricacion: parseInt(String(formData.get('anio_fabricacion') || ''), 10),
    cv: parseInt(String(formData.get('cv') || ''), 10),
    peso: parseFloat(String(formData.get('peso') || '')),
    velocidad_max: parseInt(String(formData.get('velocidad_max') || ''), 10),
    precio: parseFloat(String(formData.get('precio') || '')),
    color_fabrica: String(formData.get('color_fabrica') || '').trim(),
  };
}

function getImageFileFromFormData(formData) {
  const file = formData.get('image_file');
  if (!(file instanceof File)) return null;
  if (!file.name || file.size === 0) return null;
  return file;
}

export async function apiCreateCarFromFormData(formData) {
  const payload = buildCarPayloadFromFormData(formData);
  const imageFile = getImageFileFromFormData(formData);

  let savedCar = await apiCreateCar(payload);
  if (imageFile) {
    savedCar = await apiUploadCarImage(savedCar.id, imageFile);
  }
  return savedCar;
}

/**
 * Update a car (superadmin only).
 */
export function apiUpdateCar(id, data) {
  return request(`/cars/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function apiUpdateCarFromFormData(id, formData) {
  const payload = buildCarPayloadFromFormData(formData);
  const imageFile = getImageFileFromFormData(formData);

  let savedCar = await apiUpdateCar(id, payload);
  if (imageFile) {
    savedCar = await apiUploadCarImage(id, imageFile);
  }
  return savedCar;
}

/**
 * Delete a car (superadmin only).
 */
export function apiDeleteCar(id) {
  return request(`/cars/${id}`, { method: 'DELETE' });
}

/**
 * Upload an image for a car (superadmin only).
 */
export function apiUploadCarImage(id, file) {
  const form = new FormData();
  form.append('file', file);
  return request(`/cars/${id}/image`, { method: 'POST', body: form });
}

// ─── Favorites ───────────────────────────────────────────────────────────────

/**
 * Get the authenticated user's favorites.
 */
export function apiGetFavorites() {
  return request('/favorites/');
}

/**
 * Add a car to favorites.
 */
export function apiAddFavorite(carId, selectedColor = null) {
  return request('/favorites/', {
    method: 'POST',
    body: JSON.stringify({ car_id: carId, selected_color: selectedColor }),
  });
}

/**
 * Update the custom colour of a favorite.
 */
export function apiUpdateFavoriteColor(carId, selectedColor) {
  return request(`/favorites/${carId}/color`, {
    method: 'PATCH',
    body: JSON.stringify({ selected_color: selectedColor }),
  });
}

/**
 * Remove a car from favorites.
 */
export function apiRemoveFavorite(carId) {
  return request(`/favorites/${carId}`, { method: 'DELETE' });
}
