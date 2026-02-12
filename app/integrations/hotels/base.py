from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseHotelProvider(ABC):
    """Базовый класс для провайдеров отелей"""
    
    @abstractmethod
    async def search_hotels(
        self, 
        city: str, 
        check_in: str, 
        check_out: str, 
        guests: int = 2
    ) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_hotel_details(
        self, 
        hotel_id: str
    ) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def check_availability(
        self,
        hotel_id: str,
        check_in: str,
        check_out: str
    ) -> bool:
        pass