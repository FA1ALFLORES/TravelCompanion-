from pydantic import BaseModel, Field

class HotelCreate(BaseModel):
    """Схема для создания отеля (валидация входящих данных)"""
    name: str
    address: str
    rating: float = Field(ge=0, le=5, description="Рейтинг от 0 до 5")

class HotelUpdate(BaseModel):
    """Схема для обновления отеля (все поля опциональны)"""
    name: str | None = None
    address: str | None = None
    rating: float | None = Field(None, ge=0, le=5)

class HotelResponse(BaseModel):
    """Схема для ответа API (включает id)"""
    id: int
    name: str
    address: str
    rating: float