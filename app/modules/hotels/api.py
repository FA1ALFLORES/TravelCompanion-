from fastapi import APIRouter, HTTPException, Depends, Query
from .schemas import HotelCreate, HotelUpdate, HotelResponse
from .service import HotelService
from .repository import HotelRepository



router = APIRouter(prefix="/hotels", tags=["hotels"])

def get_hotel_service():
    repository = HotelRepository()
    return HotelService(repository)

@router.post("/", response_model=HotelResponse)
def create_hotel(
    hotel_data: HotelCreate,
    service: HotelService = Depends(get_hotel_service)
):
    try:
        return service.create_hotel(hotel_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{hotel_id}", response_model=HotelResponse)
def get_hotel(
    hotel_id: int,
    service: HotelService = Depends(get_hotel_service)
):
    try:
        return service.get_hotel(hotel_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[HotelResponse])
def get_hotels(
    page: int = Query(1, ge=1, description="Номер стр"),
    limit: int = Query(10, ge=1, le=100, description="Количество на стр"),
    service: HotelService = Depends(get_hotel_service)
):
    try:
        return service.get_hotels(page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.put("/{hotel_id}", response_model=HotelResponse)
def updated_hotel(
    hotel_id: int,
    update_data: HotelUpdate,
    service: HotelService = Depends(get_hotel_service)
):
    try:
        return service.updated_hotel(hotel_id, update_data.dict())
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))  

@router.delete("/{hotel_id}")
def deleted_hotel(
    hotel_id:int, 
    service: HotelService = Depends(get_hotel_service)
):
    try:
        deleted = service.delete_hotel(hotel_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Отель с ID {hotel_id} не найдено")
        return {"message": f"Отель с ID {hotel_id} удален","успех": True }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))