from modules.hotels.schemas import HotelCreate, HotelResponse  
from modules.hotels.repository import HotelRepository




class HotelService:
    def __init__(self, repository: HotelRepository):
        self.repository = repository
        
    def create_hotel(self, hotel: HotelCreate) -> HotelResponse:
        if hotel.rating < 0 or hotel.rating > 5:
            raise ValueError("Рейтинг должен быть от 0 до 5")
        
        created_hotel = self.repository.create_hotel(hotel)

        return HotelResponse(
            id=created_hotel.id,
            name=created_hotel.name,
            address=created_hotel.address,
            rating=created_hotel.rating
        )
        
        
    def get_hotel(self, hotel_id: int) -> HotelResponse:    
        hotel = self.repository.get_by_id(hotel_id)
        if hotel is None:
            raise ValueError(f"Такого {hotel_id}не найдено")
        
        return HotelResponse(
            id=hotel.id,
            name=hotel.name,
            address=hotel.address,
            rating=hotel.rating     
        )
    
    def update_hotel(self, hotel_id: int, update_data: dict) -> HotelResponse:
        
        if "rating" in update_data:
            rating = update_data["rating"]
            if not isinstance(rating, (int, float)):
                raise ValueError("Рейтинг должен быть числом")
            if rating < 0 or rating > 5:
                raise ValueError("Рейтинг должен быть от 0 до 5")
        
        if "name" in update_data:
            name = update_data["name"]
            if not isinstance(name, str):
                raise ValueError("Название должно быть строкой")
            if not name.strip():   
                raise ValueError("Название не может быть пустым")
        
        if "address" in update_data:
            address = update_data["address"]
            if not isinstance(address, str):
                raise ValueError("Адрес должен быть строкой")
            if not address.strip(): 
                raise ValueError("Адрес не может быть пустым")
            
        updated_hotel = self.repository.update_hotel(hotel_id, update_data)

        if updated_hotel is None:
            raise ValueError(f"Отель с ID {hotel_id} не найден")
        
        return HotelResponse(
            id=updated_hotel.id,
            name=updated_hotel.name,
            address=updated_hotel.address,
            rating=updated_hotel.rating     
        )
        
        
    def delete_hotel(self, hotel_id: int) -> bool:
        hotel = self.get_hotel(hotel_id)
        
        if hotel is None:
            return False
        
        return self.repository.delete_hotel(hotel_id)
    
    def get_hotels(self, page: int = 1, limit: int = 10) -> list[HotelResponse]:
        if page < 1:
            raise ValueError("Номер страницы должен быть положительным") 
        
        hotels = self.repository.get_all(page,limit)
        
        hotel_responses = []
        for hotel in hotels:
            hotel_response = HotelResponse(
                id=hotel.id,
                name=hotel.name,
                address=hotel.address,
                rating=hotel.rating  
            )   
            hotel_responses.append(hotel_response)
            
        return hotel_responses