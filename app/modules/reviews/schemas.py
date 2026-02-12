from pydantic import BaseModel, Field, validator




class ReviewCreate(BaseModel):
    hotel_id: int | None = None
    place_id: int | None = None
    user_id: int 
    text: str
    rating: int = Field(ge=1 , le=5)
    
    @validator('hotel_id')
    def validate_hotel_id(cls, hotel_id, values):
        place_id = values.get('place_id')
        if hotel_id is not None and place_id is not None:
            raise ValueError('Можно указать только hotel_id или place_id')
        return hotel_id
    
    @validator('place_id')
    def validate_place_id(cls, place_id, values):
        hotel_id = values.get('hotel_id')
        if place_id is not None and hotel_id is not None:
            raise ValueError('Можно указать только hotel_id или place_id')
        return place_id
    
    @validator('hotel_id', 'place_id', always=True)
    def validate_one_method(cls, values):
        hotel_id = values.get('hotel_id')
        place_id = values.get('place_id')
        if hotel_id is None and place_id is None:
            raise ValueError('Должен быть указан hotel_id или place_id')
        return values
    
class HotelReviewCreate(BaseModel):
    """Специальная схема для отзыва на отель"""
    hotel_id: int
    user_id: int
    text: str
    rating: int = Field(ge=1, le=5)

class PlaceReviewCreate(BaseModel):
    """Специальная схема для отзыва на место"""
    place_id: int
    user_id: int
    text: str
    rating: int = Field(ge=1, le=5)
    
class ReviewUpdate(BaseModel):
    text: str | None = None
    rating: int | None = Field(None,ge=1, le=5) 
    
class ReviewResponse(BaseModel):
    id: int
    hotel_id: int | None
    place_id: int | None
    user_id: int 
    text: str  
    rating: int 
    created_at: str 
            
    class Config:
        from_attributes = True            