from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple

class BasePlaceProvider(ABC):
    """Базовый класс для провайдеров мест"""
    
    @abstractmethod
    async def search_places(
        self,
        query: str,
        location: Optional[Tuple[float, float]] = None,
        radius: int = 1000,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Поиск мест по запросу"""
        pass
    
    @abstractmethod
    async def get_place_details(
        self,
        place_id: str
    ) -> Optional[Dict[str, Any]]:
        """Получить детальную информацию о месте"""
        pass
    
    @abstractmethod
    async def get_place_photos(
        self,
        photo_reference: str,
        max_width: int = 400
    ) -> Optional[bytes]:
        """Получить фото места"""
        pass
    
    @abstractmethod
    async def get_place_reviews(
        self,
        place_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Получить отзывы о месте"""
        pass