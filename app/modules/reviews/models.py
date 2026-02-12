"""ОТЗЫВЫ НА ОТЕЛИ И РАЗНЫЕ МЕСТА"""

class Review:
    def __init__(self, id: int, hotel_id: int | None, place_id: int | None, user_id: int, text: str, rating: int, created_at: str):
        self.id = id
        self.hotel_id = hotel_id 
        self.place_id = place_id 
        self.user_id = user_id
        self.text = text 
        self.rating = rating 
        self.created_at = created_at
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "text": self.text,
            "rating": self.rating,
            "created_at": self.created_at
        }    
        
    @classmethod
    def from_dict(cls, data: dict):
        return cls (
            id=data["id"],
            hotel_id=data.get("hotel_id"),
            place_id=data.get("place_id"),
            user_id=data["user_id"],
            text=data["text"], 
            rating=data["rating"],
            created_at=data["created_at"]
        )
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row[0],
            hotel_id=row[1],
            place_id=row[2],
            user_id=row[3],
            text=row[4],
            rating=row[5],
            created_at=row[6]
        ) 
        
        
    def validate(self):
        """Проверка отзыва на корректность"""
        if self.hotel_id is None and self.place_id is None:
            raise ValueError("Отзыв должен быть привязон к отелю или достапримечательности") 
        if self.hotel_id is not None and self.place_id is not None:
            raise ValueError("Отзыв не может быть на два места одновреммено") 
        if not 1 <= self.rating <= 5:
            raise ValueError("Отзыв должен быть от 1 до 5")  