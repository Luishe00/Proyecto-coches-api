import pytest
from unittest.mock import MagicMock
from app.services import favorite_service
from app.repositories.favorite_repository import IFavoriteRepository
from app.domain.entities import Favorite
from app.core.exceptions import EntityNotFoundError

@pytest.fixture
def mock_repo():
    return MagicMock(spec=IFavoriteRepository)

def test_get_user_favorites(mock_repo):
    """Verifica la recuperación de favoritos de un usuario."""
    fake_list = [Favorite(user_id=1, car_id=2)]
    mock_repo.get_by_user.return_value = fake_list

    result = favorite_service.get_user_favorites(mock_repo, 1)
    
    assert result == fake_list
    mock_repo.get_by_user.assert_called_once_with(1)

def test_create_favorite_success(mock_repo):
    """Prueba el flujo correcto de guardar un coche en favoritos."""
    mock_repo.car_exists.return_value = True
    fake_fav = Favorite(user_id=1, car_id=2, selected_color="Rojo")
    mock_repo.create.return_value = fake_fav

    result = favorite_service.create_favorite(mock_repo, 1, 2, "Rojo")
    
    assert result == fake_fav
    mock_repo.car_exists.assert_called_once_with(2)
    mock_repo.create.assert_called_once_with(user_id=1, car_id=2, selected_color="Rojo")

def test_create_favorite_car_not_found(mock_repo):
    """Impide agregar a favoritos un coche que no existe."""
    mock_repo.car_exists.return_value = False

    with pytest.raises(EntityNotFoundError):
        favorite_service.create_favorite(mock_repo, 1, 99)
    mock_repo.create.assert_not_called()

def test_update_favorite_color_success(mock_repo):
    """Permite el cambio del color de un coche que ya es favorito."""
    fake_fav = Favorite(id=10, user_id=1, car_id=2)
    mock_repo.get_by_user_and_car.return_value = fake_fav
    
    updated_fav = Favorite(id=10, user_id=1, car_id=2, selected_color="Azul")
    mock_repo.update_color.return_value = updated_fav

    result = favorite_service.update_favorite_color(mock_repo, 1, 2, "Azul")

    assert result == updated_fav
    mock_repo.get_by_user_and_car.assert_called_once_with(user_id=1, car_id=2)
    mock_repo.update_color.assert_called_once_with(10, "Azul")

def test_update_favorite_color_not_found(mock_repo):
    """Impide alterar color en un vínculo usuario-coche inexistente."""
    mock_repo.get_by_user_and_car.return_value = None

    with pytest.raises(EntityNotFoundError):
        favorite_service.update_favorite_color(mock_repo, 1, 99, "Azul")
    mock_repo.update_color.assert_not_called()

def test_remove_favorite_success(mock_repo):
    """Remueve correctamente un favorito validando existencia."""
    fake_fav = Favorite(id=10, user_id=1, car_id=2)
    mock_repo.get_by_user_and_car.return_value = fake_fav

    result = favorite_service.remove_favorite(mock_repo, 1, 2)
    
    assert result == fake_fav
    mock_repo.delete.assert_called_once_with(fake_fav)

def test_remove_favorite_not_found(mock_repo):
    """Falla al intentar remover algo que no estaba en la base de datos."""
    mock_repo.get_by_user_and_car.return_value = None

    with pytest.raises(EntityNotFoundError):
        favorite_service.remove_favorite(mock_repo, 1, 99)
    mock_repo.delete.assert_not_called()

# --- BLACK-BOX: Equivalence Classes ---
@pytest.mark.parametrize("color, expected_result", [
    ("Rojo", "Rojo"),
    (None, None),
    ("", "")
])
def test_create_favorite_equivalence_classes(mock_repo, color, expected_result):
    mock_repo.car_exists.return_value = True
    fake_fav = Favorite(user_id=1, car_id=2, selected_color=color)
    mock_repo.create.return_value = fake_fav

    result = favorite_service.create_favorite(mock_repo, 1, 2, color)
    assert result.selected_color == expected_result

# --- BLACK-BOX: Decision Tables ---
@pytest.mark.parametrize("car_exists, selected_color, should_fail", [
    (True, "Verde", False),
    (True, None, False),
    (False, "Verde", True)
])
def test_create_favorite_decision_table(mock_repo, car_exists, selected_color, should_fail):
    mock_repo.car_exists.return_value = car_exists
    if not should_fail:
        mock_repo.create.return_value = Favorite(user_id=1, car_id=2, selected_color=selected_color)

    if should_fail:
        with pytest.raises(EntityNotFoundError):
            favorite_service.create_favorite(mock_repo, 1, 2, selected_color)
    else:
        result = favorite_service.create_favorite(mock_repo, 1, 2, selected_color)
        assert result.selected_color == selected_color

# --- WHITE-BOX: Decision Coverage ---
def test_remove_favorite_branches(mock_repo):
    # Caso 1: Favorito existe (rama positiva)
    mock_repo.get_by_user_and_car.return_value = Favorite(id=1, user_id=1, car_id=1)
    res = favorite_service.remove_favorite(mock_repo, 1, 1)
    assert res is not None
    mock_repo.delete.assert_called_once()

    # Caso 2: Favorito no existe (rama if not favorite)
    mock_repo.get_by_user_and_car.return_value = None
    with pytest.raises(EntityNotFoundError):
        favorite_service.remove_favorite(mock_repo, 1, 2)
