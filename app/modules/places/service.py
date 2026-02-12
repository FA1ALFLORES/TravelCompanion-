from modules.places.schemas import PlaceCreate, PlaceResponse, PlaceType
from modules.places.repository import PlaceRepository
from modules.places.models import Place 

class PlaceService:
    def __init__(self, repository: PlaceRepository):
        self.repository = repository
        
    def create_place(self, place_data: PlaceCreate) -> PlaceResponse:
        
        place_model = Place(
            id=0,
            name=place_data.name,
            type=place_data.type.value,
            address=place_data.address,
            rating=place_data.rating
        )

        created_place = self.repository.create_place(place_model)
        
        return PlaceResponse(
            id=created_place.id,
            name=created_place.name,
            type=PlaceType(created_place.type),
            address=created_place.address,
            rating=created_place.rating
        )   
        
    def get_place(self, place_id: int) -> PlaceResponse:
        place = self.repository.get_by_id(place_id)
        if place is None:
            raise ValueError(f"Место с ID {place_id} не найдено")     
        
        return PlaceResponse(
            id=place_id,
            name=place.name,
            type=PlaceType(place.type),
            address=place.address,
            rating=place.rating
        )
        
    def update_place(self, place_id: int, update_data: dict) -> PlaceResponse:
       
        if "type" in update_data:
            place_type = update_data["type"]
            if not isinstance(place_type, str):
                raise ValueError("Тип должно быть строкой")
            if not place_type.strip():
                raise ValueError("Тип не может быть пустым")
            
       
            
        updated_place = self.repository.update_place(place_id, update_data)
         
        if updated_place is None:
            raise ValueError(f"Место с ID {place_id} не найден")    
        
        return PlaceResponse(
            id=updated_place.id,
            name=updated_place.name,
            type=PlaceType(updated_place.type),
            address=updated_place.address,
            rating=updated_place.rating
        )
        
    def delete_place(self, place_id: int) -> bool:
        place = self.get_place(place_id)   
        
        if place is None:
            return False
        
        return self.repository.delete_place(place_id)
    
    def get_places(self, page: int = 1, limit: int = 10) -> list[PlaceResponse]:
        if page < 1:
            raise ValueError("Номер страницы должен быть положительным") 
        
        places = self.repository.get_all(page, limit)
    
        return [
        PlaceResponse(
            id=place.id,
            name=place.name,
            type=PlaceType(place.type),  # Конвертация
            address=place.address,
            rating=place.rating
        )
        for place in places
    ]