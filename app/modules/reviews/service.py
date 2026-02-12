from modules.hotels.service import HotelService
from modules.places.service import PlaceService
from modules.reviews.schemas import ReviewCreate, ReviewUpdate, ReviewResponse, HotelReviewCreate, PlaceReviewCreate
from modules.reviews.repository import ReviewRepository
from modules.reviews.models import Review




class ReviewService:
    def __init__(self, repository: ReviewRepository, 
                 hotel_service: HotelService | None = None,
                 place_service: PlaceService | None = None
                ):
        self.repository = repository
        self.hotel_service = hotel_service 
        self.place_service = place_service 
        
    def create_review(self, review_data: ReviewCreate) -> ReviewResponse:
        
        if not 1 <= review_data.rating <= 5:
            raise ValueError("Рейтинг должен быть от 1 до 5")
    
        if not review_data.text.strip():
            raise ValueError("Текст отзыва не может быть пустым")
    
        review_model = Review(
            id=0,
            hotel_id=review_data.hotel_id,
            place_id=review_data.place_id,
            user_id=review_data.user_id,
            text=review_data.text,
            rating=review_data.rating,
            created_at= "" # сгенерирует бд 
        )    
        
        created_review = self.repository.create_review(review_model)
        
        return ReviewResponse(
            id=created_review.id,
            hotel_id=created_review.hotel_id,
            place_id=created_review.place_id,
            user_id=created_review.user_id,
            text=created_review.text,
            rating=created_review.rating,
            created_at=created_review.created_at
        )
        
    def create_hotel_review(self, data: HotelReviewCreate) -> ReviewResponse:    
        
        review_data = ReviewCreate(
            hotel_id=data.hotel_id,
            place_id=None,
            user_id=data.user_id,
            text=data.text,
            rating=data.rating
        )
        
        return self.create_review(review_data)
    
    def create_place_review(self, data: PlaceReviewCreate) -> ReviewResponse:
        
        review_data = ReviewCreate(
            hotel_id=None,
            place_id=data.place_id,
            user_id=data.user_id,
            text=data.text,
            rating=data.rating
        )    
        
        return self.create_review(review_data)
        
    def get_hotel_reviews(self, hotel_id: int, page: int = 1, limit: int = 10) -> list[ReviewResponse]:
        
        if self.hotel_service:
            try:
                self.hotel_service.get_hotel(hotel_id)
            except ValueError:
                raise ValueError(f"Отель с {hotel_id} не найден")    
            
        reviews = self.repository.get_by_hotel_id(hotel_id, page, limit)
        
        return [
            ReviewResponse(
                id=review.id,
                hotel_id=review.hotel_id,
                place_id=review.place_id,
                user_id=review.user_id,
                text=review.text,
                rating=review.rating,
                created_at=review.created_at
            )
            for review in reviews
        ]
        
    def get_place_reviews(self, place_id: int, page: int = 1, limit: int = 10) -> list[ReviewResponse]:    
            
        if self.place_service:
            try:
                self.place_service.get_place(place_id)
            except ValueError:
                raise ValueError(f"Место с {place_id} не найден")    
            
        reviews = self.repository.get_by_place_id(place_id, page, limit)
        
        return [
        ReviewResponse(
            id=review.id,
            hotel_id=review.hotel_id,
            place_id=review.place_id,
            user_id=review.user_id,
            text=review.text,
            rating=review.rating,
            created_at=review.created_at
        )
        for review in reviews
    ]
     
    def get_review(self, review_id: int) -> ReviewResponse:
        review = self.repository.get_by_id(review_id)
        if review is None:
            raise ValueError("Отзыв не найден")  
        
        return ReviewResponse(
            id=review.id,
            hotel_id=review.hotel_id,
            place_id=review.place_id,
            user_id=review.user_id,
            text=review.text,
            rating=review.rating,
            created_at=review.created_at
        ) 
       
    def update_review(self, review_id: int, update_data: dict) -> ReviewResponse:
        
        if "text" in update_data:
            text = update_data["text"]
            if not isinstance(text, str):
                raise ValueError("Текст должно быть строкой")
            if not text.strip():
                raise ValueError("Текст не может быть пустой строкой или состоять только из пробелов")
        
        if "rating" in update_data:
            rating = update_data["rating"]
            if not isinstance(rating, (int, float)):
                raise ValueError("Рейтинг должен быть числом")
            if not 1 <= rating <=5:
                raise ValueError("Рейтинг должен быть от 1 до 5")
            
        updated_review = self.repository.update_review(review_id, update_data)    
        
        if updated_review is None:
            raise ValueError(f"Отзыв  {review_id} не найден")
        
        
        return ReviewResponse(
            id=updated_review.id,
            hotel_id=updated_review.hotel_id,
            place_id=updated_review.place_id,
            user_id=updated_review.user_id,
            text=updated_review.text,
            rating=updated_review.rating,
            created_at=updated_review.created_at
        )
    
    
    def delete_review(self, review_id: int) -> bool:
        
        return self.repository.delete_review(review_id)
        
    def get_all_reviews(self, page: int = 1, limit: int = 100) -> list[ReviewResponse]:           
        
        if page < 1:
            raise ValueError("Номер страницы должен быть положительным") 
        if not 1 <= limit <= 100:
            raise ValueError("Лимит должен быть 1 до 100")
        
        reviews = self.repository.get_all(page, limit)
        
        return [
        ReviewResponse(
            id=review.id,
            hotel_id=review.hotel_id,
            place_id=review.place_id,
            user_id=review.user_id,
            text=review.text,
            rating=review.rating,
            created_at=review.created_at   
        )
        for review in reviews 
        ]