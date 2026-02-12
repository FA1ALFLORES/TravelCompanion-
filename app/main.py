from fastapi import FastAPI, HTTPException
from core.database import init_db 
from fastapi.middleware.cors import CORSMiddleware
from modules.hotels.api import router as hotels_router 
from modules.places.api import router as places_router 
from modules.reviews.api import router as reviews_router 
from modules.auth.api import router as auth_router 
from fastapi.responses import JSONResponse
from fastapi.requests import Request




app = FastAPI(title="TravelCompanion API",  version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotels_router, prefix="/hotels", tags=["hotels"])
app.include_router(places_router, prefix="/places", tags=["places"])
app.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/health")
def health():
    return {"status": "Ok"}

@app.on_event("startup")
async def startup_event():
    print("Начало работы")
    
init_db()
    

@app.on_event("shutdown")
async def shutdown_event():
    print("Конец работы")    
    

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        )   
    
    
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    
    