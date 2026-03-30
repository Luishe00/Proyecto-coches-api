/**
 * cars.js — Car catalog, car detail modal, favorites and admin CRUD views.
 */

import {
  apiGetCars,
  apiGetCar,
  apiCreateCar,
  apiUpdateCar,
  apiDeleteCar,
  apiUploadCarImage,
  apiGetFavorites,
  apiAddFavorite,
  apiRemoveFavorite,
  apiUpdateFavoriteColor,
} from './api.js';
import { isSuperadmin, isLoggedIn } from './auth.js';
import { showToast } from './utils.js';

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatPrice(price) {
  return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(price);
}

function carImageSrc(car) {
  if (!car.image_url) return '';
  // Relative paths served from FastAPI /static
  if (car.image_url.startsWith('/') || car.image_url.startsWith('http')) return car.image_url;
  return `http://localhost:8000/${car.image_url}`;
}

function carPlaceholderSvg(marca) {
  const letter = (marca || 'C').charAt(0).toUpperCase();
  return `<div class="car-placeholder"><span>${letter}</span></div>`;
}

// ─── Car Card ─────────────────────────────────────────────────────────────────

function buildCarCard(car, favSet) {
  const isFav = favSet.has(car.id);
  const imgHtml = car.image_url
    ? `<img src="${carImageSrc(car)}" alt="${car.marca} ${car.modelo}" loading="lazy" />`
    : carPlaceholderSvg(car.marca);

  return `
    <article class="car-card glass-card animate-fade-in" data-id="${car.id}">
      <div class="car-card__img">${imgHtml}</div>
      <div class="car-card__body">
        <div class="car-card__brand">${car.marca}</div>
        <h3 class="car-card__model">${car.modelo}</h3>
        <div class="car-card__year">${car.anio_fabricacion}</div>
        <div class="car-card__stats">
          <span title="Potencia">⚡ ${car.cv} cv</span>
          <span title="Velocidad máxima">🏁 ${car.velocidad_max} km/h</span>
        </div>
        <div class="car-card__footer">
          <span class="car-card__price">${formatPrice(car.precio)}</span>
          <div class="car-card__actions">
            ${isLoggedIn() ? `
              <button class="btn-icon btn-fav ${isFav ? 'active' : ''}" data-car-id="${car.id}" title="${isFav ? 'Quitar de favoritos' : 'Añadir a favoritos'}">
                ${isFav ? '❤️' : '🤍'}
              </button>
            ` : ''}
            <button class="btn-icon btn-detail" data-car-id="${car.id}" title="Ver detalles">🔍</button>
            ${isSuperadmin() ? `
              <button class="btn-icon btn-edit" data-car-id="${car.id}" title="Editar">✏️</button>
              <button class="btn-icon btn-delete" data-car-id="${car.id}" title="Eliminar">🗑️</button>
            ` : ''}
          </div>
        </div>
      </div>
    </article>
  `;
}

// ─── Car Detail Modal ─────────────────────────────────────────────────────────

function openCarModal(car, favSet) {
  closeCarModal();

  const isFav = favSet.has(car.id);
  const imgHtml = car.image_url
    ? `<img src="${carImageSrc(car)}" alt="${car.marca} ${car.modelo}" />`
    : carPlaceholderSvg(car.marca);

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay animate-fade-in';
  overlay.id = 'carModal';
  overlay.innerHTML = `
    <div class="modal-card glass-card">
      <button class="modal-close" id="modalClose">✕</button>
      <div class="modal-img">${imgHtml}</div>
      <div class="modal-body">
        <div class="modal-brand">${car.marca}</div>
        <h2 class="modal-model">${car.modelo} <span class="modal-year">${car.anio_fabricacion}</span></h2>
        <div class="modal-price">${formatPrice(car.precio)}</div>
        <div class="modal-specs">
          <div class="spec-item"><span class="spec-label">Potencia</span><span class="spec-value">${car.cv} cv</span></div>
          <div class="spec-item"><span class="spec-label">Peso</span><span class="spec-value">${car.peso} kg</span></div>
          <div class="spec-item"><span class="spec-label">Vel. máx.</span><span class="spec-value">${car.velocidad_max} km/h</span></div>
          <div class="spec-item"><span class="spec-label">Color fábrica</span><span class="spec-value">${car.color_fabrica}</span></div>
        </div>
        <div class="modal-footer">
          ${isLoggedIn() ? `
            <button class="btn btn-fav-modal ${isFav ? 'active' : ''}" id="modalFavBtn" data-car-id="${car.id}">
              ${isFav ? '❤️ Quitar de favoritos' : '🤍 Añadir a favoritos'}
            </button>
          ` : ''}
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);

  overlay.querySelector('#modalClose').addEventListener('click', closeCarModal);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeCarModal(); });

  const favBtn = overlay.querySelector('#modalFavBtn');
  if (favBtn) {
    favBtn.addEventListener('click', async () => {
      const carId = parseInt(favBtn.dataset.carId, 10);
      await _toggleFav(carId, favSet, favBtn);
    });
  }

  requestAnimationFrame(() => overlay.classList.add('visible'));
}

function closeCarModal() {
  const existing = document.getElementById('carModal');
  if (existing) existing.remove();
}

async function _toggleFav(carId, favSet, btn) {
  try {
    if (favSet.has(carId)) {
      await apiRemoveFavorite(carId);
      favSet.delete(carId);
      btn.textContent = '🤍 Añadir a favoritos';
      btn.classList.remove('active');
      showToast('Eliminado de favoritos');
    } else {
      await apiAddFavorite(carId);
      favSet.add(carId);
      btn.textContent = '❤️ Quitar de favoritos';
      btn.classList.add('active');
      showToast('Añadido a favoritos ❤️');
    }
    // Refresh inline card fav button too
    const cardFavBtn = document.querySelector(`.btn-fav[data-car-id="${carId}"]`);
    if (cardFavBtn) {
      cardFavBtn.classList.toggle('active', favSet.has(carId));
      cardFavBtn.textContent = favSet.has(carId) ? '❤️' : '🤍';
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// ─── Filter Bar ──────────────────────────────────────────────────────────────

function buildFilterBar() {
  return `
    <div class="filter-bar glass-card animate-fade-in">
      <div class="filter-row">
        <div class="filter-group">
          <label for="filterMarca">Marca</label>
          <input type="text" id="filterMarca" placeholder="Ej: Ferrari" />
        </div>
        <div class="filter-group">
          <label for="filterModelo">Modelo</label>
          <input type="text" id="filterModelo" placeholder="Ej: 488" />
        </div>
        <div class="filter-group">
          <label for="filterAnioMin">Año desde</label>
          <input type="number" id="filterAnioMin" placeholder="2000" min="1886" max="2027" />
        </div>
        <div class="filter-group">
          <label for="filterAnioMax">Año hasta</label>
          <input type="number" id="filterAnioMax" placeholder="2025" min="1886" max="2027" />
        </div>
        <div class="filter-group">
          <label for="filterPrecioMax">Precio máx (€)</label>
          <input type="number" id="filterPrecioMax" placeholder="500000" min="0" />
        </div>
        <div class="filter-group">
          <label for="filterVelMin">Vel. mín (km/h)</label>
          <input type="number" id="filterVelMin" placeholder="200" min="0" />
        </div>
        <div class="filter-group">
          <label for="filterColor">Color</label>
          <input type="text" id="filterColor" placeholder="Rojo" />
        </div>
      </div>
      <div class="filter-actions">
        <button class="btn btn-secondary" id="filterClearBtn">Limpiar</button>
        <button class="btn btn-primary" id="filterApplyBtn">🔍 Buscar</button>
      </div>
    </div>
  `;
}

function collectFilters(container) {
  const get = (id) => container.querySelector(`#${id}`)?.value?.trim() || undefined;
  return {
    marca: get('filterMarca'),
    modelo: get('filterModelo'),
    anio_min: get('filterAnioMin'),
    anio_max: get('filterAnioMax'),
    precio_max: get('filterPrecioMax'),
    velocidad_min: get('filterVelMin'),
    color_fabrica: get('filterColor'),
  };
}

// ─── Admin Car Form Modal ─────────────────────────────────────────────────────

function openCarFormModal(car = null, onSaved) {
  const isEdit = !!car;
  const existing = document.getElementById('carFormModal');
  if (existing) existing.remove();

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay animate-fade-in';
  overlay.id = 'carFormModal';
  overlay.innerHTML = `
    <div class="modal-card glass-card modal-form-card">
      <button class="modal-close" id="carFormClose">✕</button>
      <h2 class="modal-title">${isEdit ? 'Editar coche' : 'Nuevo coche'}</h2>
      <form id="carForm" class="car-form" autocomplete="off">
        <div class="form-grid">
          <div class="form-group">
            <label>Marca *</label>
            <input type="text" name="marca" value="${car?.marca || ''}" required minlength="2" maxlength="50" />
          </div>
          <div class="form-group">
            <label>Modelo *</label>
            <input type="text" name="modelo" value="${car?.modelo || ''}" required minlength="1" maxlength="100" />
          </div>
          <div class="form-group">
            <label>Año fabricación *</label>
            <input type="number" name="anio_fabricacion" value="${car?.anio_fabricacion || ''}" required min="1886" max="2027" />
          </div>
          <div class="form-group">
            <label>Potencia (cv) *</label>
            <input type="number" name="cv" value="${car?.cv || ''}" required min="1" />
          </div>
          <div class="form-group">
            <label>Peso (kg) *</label>
            <input type="number" name="peso" value="${car?.peso || ''}" required min="1" step="0.1" />
          </div>
          <div class="form-group">
            <label>Velocidad máx (km/h) *</label>
            <input type="number" name="velocidad_max" value="${car?.velocidad_max || ''}" required min="1" />
          </div>
          <div class="form-group">
            <label>Precio (€) *</label>
            <input type="number" name="precio" value="${car?.precio || ''}" required min="0.01" step="0.01" />
          </div>
          <div class="form-group">
            <label>Color fábrica *</label>
            <input type="text" name="color_fabrica" value="${car?.color_fabrica || ''}" required minlength="2" maxlength="50" />
          </div>
        </div>
        ${isEdit ? `
          <div class="form-group form-group--full">
            <label>Subir imagen</label>
            <input type="file" id="carImageFile" accept="image/*" />
          </div>
        ` : ''}
        <div class="form-error" id="carFormError"></div>
        <div class="form-actions">
          <button type="button" class="btn btn-secondary" id="carFormCancel">Cancelar</button>
          <button type="submit" class="btn btn-primary" id="carFormSubmit">
            <span class="btn-text">${isEdit ? 'Guardar cambios' : 'Crear coche'}</span>
            <span class="btn-loader hidden"></span>
          </button>
        </div>
      </form>
    </div>
  `;

  document.body.appendChild(overlay);
  requestAnimationFrame(() => overlay.classList.add('visible'));

  const close = () => overlay.remove();
  overlay.querySelector('#carFormClose').addEventListener('click', close);
  overlay.querySelector('#carFormCancel').addEventListener('click', close);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });

  overlay.querySelector('#carForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = overlay.querySelector('#carFormSubmit');
    const errorEl = overlay.querySelector('#carFormError');
    errorEl.textContent = '';
    _setLoading(submitBtn, true);

    const fd = new FormData(e.target);
    const data = {
      marca: fd.get('marca'),
      modelo: fd.get('modelo'),
      anio_fabricacion: parseInt(fd.get('anio_fabricacion'), 10),
      cv: parseInt(fd.get('cv'), 10),
      peso: parseFloat(fd.get('peso')),
      velocidad_max: parseInt(fd.get('velocidad_max'), 10),
      precio: parseFloat(fd.get('precio')),
      color_fabrica: fd.get('color_fabrica'),
    };

    try {
      let savedCar;
      if (isEdit) {
        savedCar = await apiUpdateCar(car.id, data);
        // Upload image if selected
        const imgFile = overlay.querySelector('#carImageFile')?.files?.[0];
        if (imgFile) {
          savedCar = await apiUploadCarImage(car.id, imgFile);
        }
        showToast('Coche actualizado ✅');
      } else {
        savedCar = await apiCreateCar(data);
        showToast('Coche creado ✅');
      }
      close();
      if (onSaved) onSaved(savedCar);
    } catch (err) {
      errorEl.textContent = err.message;
    } finally {
      _setLoading(submitBtn, false);
    }
  });
}

function _setLoading(btn, loading) {
  btn.disabled = loading;
  btn.querySelector('.btn-text')?.classList.toggle('hidden', loading);
  btn.querySelector('.btn-loader')?.classList.toggle('hidden', !loading);
}

// ─── Catalog View ─────────────────────────────────────────────────────────────

export async function renderCatalogView(container) {
  container.innerHTML = `
    <section class="catalog-section">
      <div class="catalog-header animate-fade-in">
        <h2 class="section-title">Catálogo <span class="accent">Premium</span></h2>
        <p class="section-sub">Descubre los coches más exclusivos del mundo</p>
        ${isSuperadmin() ? `<button class="btn btn-primary" id="newCarBtn">+ Nuevo coche</button>` : ''}
      </div>
      ${buildFilterBar()}
      <div class="cars-grid" id="carsGrid">
        <div class="loading-spinner"><div class="spinner"></div><p>Cargando catálogo…</p></div>
      </div>
    </section>
  `;

  let favSet = new Set();
  let currentCars = [];

  const grid = container.querySelector('#carsGrid');

  async function loadCars(filters = {}) {
    grid.innerHTML = `<div class="loading-spinner"><div class="spinner"></div><p>Cargando catálogo…</p></div>`;
    try {
      const [cars, favs] = await Promise.all([
        apiGetCars(filters),
        isLoggedIn() ? apiGetFavorites().catch(() => []) : Promise.resolve([]),
      ]);
      currentCars = cars;
      favSet = new Set(favs.map(f => f.car_id));
      renderGrid(cars, favSet);
    } catch (err) {
      grid.innerHTML = `<div class="error-msg">Error al cargar coches: ${err.message}</div>`;
    }
  }

  function renderGrid(cars, favSet) {
    if (!cars.length) {
      grid.innerHTML = `<div class="empty-state"><span>🚗</span><p>No se encontraron coches con estos filtros</p></div>`;
      return;
    }
    grid.innerHTML = cars.map(c => buildCarCard(c, favSet)).join('');
    _attachGridEvents(grid, favSet);
  }

  function _attachGridEvents(grid, favSet) {
    grid.querySelectorAll('.btn-detail').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.carId, 10);
        try {
          const car = await apiGetCar(id);
          openCarModal(car, favSet);
        } catch (err) {
          showToast(err.message, 'error');
        }
      });
    });

    grid.querySelectorAll('.btn-fav').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.carId, 10);
        await _toggleFav(id, favSet, btn);
        btn.textContent = favSet.has(id) ? '❤️' : '🤍';
      });
    });

    if (isSuperadmin()) {
      grid.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', async () => {
          const id = parseInt(btn.dataset.carId, 10);
          const car = currentCars.find(c => c.id === id) || await apiGetCar(id);
          openCarFormModal(car, () => loadCars(collectFilters(container)));
        });
      });

      grid.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', async () => {
          const id = parseInt(btn.dataset.carId, 10);
          const car = currentCars.find(c => c.id === id);
          if (!confirm(`¿Eliminar ${car?.marca} ${car?.modelo}?`)) return;
          try {
            await apiDeleteCar(id);
            showToast('Coche eliminado');
            loadCars(collectFilters(container));
          } catch (err) {
            showToast(err.message, 'error');
          }
        });
      });
    }
  }

  // Filter events
  container.querySelector('#filterApplyBtn').addEventListener('click', () => {
    loadCars(collectFilters(container));
  });
  container.querySelector('#filterClearBtn').addEventListener('click', () => {
    container.querySelectorAll('.filter-group input').forEach(i => (i.value = ''));
    loadCars();
  });
  // Apply filter on Enter key
  container.querySelectorAll('.filter-group input').forEach(input => {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') loadCars(collectFilters(container));
    });
  });

  // Admin new car
  container.querySelector('#newCarBtn')?.addEventListener('click', () => {
    openCarFormModal(null, () => loadCars(collectFilters(container)));
  });

  await loadCars();
}

// ─── Favorites View ───────────────────────────────────────────────────────────

export async function renderFavoritesView(container) {
  container.innerHTML = `
    <section class="favorites-section">
      <div class="catalog-header animate-fade-in">
        <h2 class="section-title">Mis <span class="accent">Favoritos</span></h2>
        <p class="section-sub">Tu colección personal de coches de ensueño</p>
      </div>
      <div class="cars-grid" id="favsGrid">
        <div class="loading-spinner"><div class="spinner"></div><p>Cargando favoritos…</p></div>
      </div>
    </section>
  `;

  const grid = container.querySelector('#favsGrid');

  async function loadFavs() {
    try {
      const favs = await apiGetFavorites();
      if (!favs.length) {
        grid.innerHTML = `<div class="empty-state"><span>🤍</span><p>Aún no tienes favoritos. Explora el <a href="#catalog">catálogo</a>!</p></div>`;
        return;
      }
      const favSet = new Set(favs.map(f => f.car_id));
      grid.innerHTML = favs.map(f => buildFavCard(f)).join('');
      _attachFavEvents(grid, favs, favSet);
    } catch (err) {
      grid.innerHTML = `<div class="error-msg">Error: ${err.message}</div>`;
    }
  }

  function buildFavCard(fav) {
    const car = fav.car;
    const imgHtml = car.image_url
      ? `<img src="${carImageSrc(car)}" alt="${car.marca} ${car.modelo}" loading="lazy" />`
      : carPlaceholderSvg(car.marca);

    return `
      <article class="car-card glass-card animate-fade-in fav-card" data-id="${car.id}" data-fav-id="${fav.id}">
        <div class="car-card__img">${imgHtml}</div>
        <div class="car-card__body">
          <div class="car-card__brand">${car.marca}</div>
          <h3 class="car-card__model">${car.modelo}</h3>
          <div class="car-card__year">${car.anio_fabricacion}</div>
          <div class="fav-color-row">
            <label>Color personalizado:</label>
            <div class="color-input-wrap">
              <input type="color" class="fav-color-input" data-car-id="${car.id}" value="${_colorToHex(fav.selected_color)}" title="Cambiar color" />
              <span class="fav-color-label">${fav.selected_color || 'Color original'}</span>
            </div>
          </div>
          <div class="car-card__footer">
            <span class="car-card__price">${formatPrice(car.precio)}</span>
            <div class="car-card__actions">
              <button class="btn-icon btn-detail" data-car-id="${car.id}" title="Ver detalles">🔍</button>
              <button class="btn-icon btn-remove-fav" data-car-id="${car.id}" title="Quitar de favoritos">❌</button>
            </div>
          </div>
        </div>
      </article>
    `;
  }

  function _attachFavEvents(grid, favs, favSet) {
    grid.querySelectorAll('.btn-detail').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.carId, 10);
        const car = await apiGetCar(id);
        openCarModal(car, favSet);
      });
    });

    grid.querySelectorAll('.btn-remove-fav').forEach(btn => {
      btn.addEventListener('click', async () => {
        const carId = parseInt(btn.dataset.carId, 10);
        try {
          await apiRemoveFavorite(carId);
          showToast('Eliminado de favoritos');
          loadFavs();
        } catch (err) {
          showToast(err.message, 'error');
        }
      });
    });

    grid.querySelectorAll('.fav-color-input').forEach(input => {
      let debounce;
      input.addEventListener('input', () => {
        clearTimeout(debounce);
        debounce = setTimeout(async () => {
          const carId = parseInt(input.dataset.carId, 10);
          const color = input.value;
          try {
            await apiUpdateFavoriteColor(carId, color);
            const label = input.nextElementSibling;
            if (label) label.textContent = color;
            showToast('Color actualizado 🎨');
          } catch (err) {
            showToast(err.message, 'error');
          }
        }, 600);
      });
    });
  }

  await loadFavs();
}

function _colorToHex(color) {
  if (!color) return '#c9a84c';
  if (color.startsWith('#')) return color;
  // Try named colour via canvas
  const ctx = document.createElement('canvas').getContext('2d');
  ctx.fillStyle = color;
  return ctx.fillStyle;
}
