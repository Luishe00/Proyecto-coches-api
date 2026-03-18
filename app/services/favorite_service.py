from typing import List
from app.domain import entities as domain
from app.core.exceptions import EntityNotFoundError
from app.repositories.favorite_repository import IFavoriteRepository

def get_user_favorites(repository: IFavoriteRepository, user_id: int) -> List[domain.Favorite]:
    """
    Recupera todos los coches favoritos de un usuario.
    """
    return repository.get_by_user(user_id)

def create_favorite(repository: IFavoriteRepository, user_id: int, car_id: int) -> domain.Favorite:
    """
    Añade un coche a favoritos. Verifica la existencia del coche y evita duplicados.
    """
    # Verificar que el coche existe
    if not repository.car_exists(car_id):
        raise EntityNotFoundError(detail="El coche no existe.")
    
    return repository.create(user_id=user_id, car_id=car_id)

def remove_favorite(repository: IFavoriteRepository, user_id: int, car_id: int) -> domain.Favorite:
    """
    Elimina un coche de favoritos. Verifica que exista antes de intentar borrar.
    """
    favorite = repository.get_by_user_and_car(user_id=user_id, car_id=car_id)
    
    if not favorite:
        raise EntityNotFoundError(detail="No se encontró este favorito en tu lista.")
        
    repository.delete(favorite)
    return favorite
