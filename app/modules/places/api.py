from fastapi import APIRouter, HTTPException, Depends, Query
from .schemas import PlaceCreate, PlaceUpdate, PlaceResponse
from .service import PlaceService
from .repository import PlaceRepository


router = APIRouter(prefix="/places", tags=["places"])

def get_place_service():
    repository = PlaceRepository()
    return PlaceService(repository)

@router.post("/",response_model=PlaceResponse)
def create_place(
    place_data: PlaceCreate,
    service: PlaceService = Depends(get_place_service)
):
    try:
        return service.create_place(place_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{place_id}", response_model=PlaceResponse) 
def get_place(
    place_id: int,
    service: PlaceService = Depends(get_place_service)
):
    try:
        return service.get_place(place_id) 
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/", response_model=list[PlaceResponse])
def get_places(
    page: int = Query(1, ge=1, description="Номер стр"),
    limit: int = Query(10, ge=1 , le=100, description="Количество на стр"),
    service: PlaceService = Depends(get_place_service)
):
    try:
        return service.get_places(page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{place_id}", response_model=PlaceResponse) 
def update_place(
    place_id: int, 
    update_data: PlaceUpdate,
    service: PlaceService = Depends(get_place_service)
):
    try:
        return service.update_place(place_id, update_data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{place_id}")
def deleted_place(
    place_id: int, 
    service: PlaceService = Depends(get_place_service)
):
    try:
        deleted = service.delete_place(place_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Место с ID {place_id} не найдено")  
        return {"message": f"Место с ID {place_id} удалено","успех": True}          
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    