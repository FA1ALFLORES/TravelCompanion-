from  enum import Enum
from pydantic import BaseModel, Field

class PlaceType(str,Enum):
    MUSEUM = "museum"
    PARK = "park"
    RESTAURANT = "restaurant"
    SQUARE = "square"
    THEATER = "theater"
    SHOPPING = "shopping"
    OTHER = "other"

class PlaceCreate(BaseModel):
    name: str
    type: PlaceType
    address: str
    rating: float = Field(ge=0, le=5)

class PlaceUpdate(BaseModel):
    name: str | None = None
    type: PlaceType | None = None
    address: str | None = None
    rating: float | None = Field(None, ge=0, le=5)

class PlaceResponse(BaseModel):
    id: int
    name: str
    type: PlaceType
    address: str
    rating: float
    
    class Config:
        from_attributes = True # Для перехода на sqlalchemy     