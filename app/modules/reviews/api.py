from fastapi import APIRouter, HTTPException, Depends, Query
from .schemas import ReviewCreate, ReviewUpdate, ReviewResponse, HotelReviewCreate, PlaceReviewCreate
from .service import ReviewService
from .repository import ReviewRepository

router = APIRouter(prefix="/reviews", tags=["reviews"])

def get_review_service():
    repository = ReviewRepository()
    
    
    return ReviewService(repository, hotel_service=None, place_service=None)

@router.post("/", response_model=ReviewResponse)
def create_review(
    review_data: ReviewCreate,
    service: ReviewService = Depends(get_review_service)
):
    try:
        return service.create_review(review_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/hotel/", response_model=ReviewResponse) 
def create_review_hotel(
    review_data: HotelReviewCreate,
    service: ReviewService = Depends(get_review_service)
):
    try:
        return service.create_hotel_review(review_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))   

@router.post("/place/", response_model=ReviewResponse)
def create_review_place(
    review_data: PlaceReviewCreate,
    service: ReviewService = Depends(get_review_service)
):
    try:
        return service.create_place_review(review_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int, 
    service: ReviewService = Depends(get_review_service)
):
    try:
        return service.get_review(review_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@router.get("/", response_model=list[ReviewResponse])
def get_all_reviews(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(1, ge=1, le=100, description="Количество на стр"),
    service: ReviewService = Depends(get_review_service)
):
    try:
        return service.get_all_reviews(page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/hotel/{hotel_id}",response_model=list[ReviewResponse])
def get_hotel_reviews(
    hotel_id: int,
    page: int = Query(1,ge=1),
    limit: int = Query(1, ge=1, le=100),
    service: ReviewService = Depends(get_review_service)
):
    try:
        return service.get_hotel_reviews(hotel_id, page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/place/{place_id}",response_model=list[ReviewResponse])
def get_place_reviews(
    place_id: int,
    page: int = Query(1,ge=1),
    limit: int = Query(1, ge=1, le=100),
    service: ReviewService = Depends(get_review_service)
):
    try:
        return service.get_place_reviews(place_id, page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{review_id}",response_model=ReviewResponse)
def update_review(
    review_id: int,
    update_data: ReviewUpdate,
    service: ReviewService = Depends(get_review_service)
):
    try:
        return get_review_service(review_id, update_data.dict(exclude_unset=True)) 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service)
):
    try:
        deleted = service.delete_review(review_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Отзыв {review_id} не  айден")
        return {"message": f"Отзыв с ID {review_id} удален", "успех": True}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))