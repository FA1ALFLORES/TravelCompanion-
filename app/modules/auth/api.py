from fastapi import APIRouter, Depends, HTTPException
from typing import List

from modules.auth.schemas import (
    UserCreate, UserLogin, Token, 
    UserResponse, RefreshTokenRequest
)
from modules.auth.service import AuthService
from modules.auth.repository import UserRepository
from modules.auth.dependencies import get_current_user, check_admin

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service():
    repository = UserRepository()
    return AuthService(repository)

@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
   
    try:
        return service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
   
    try:
        return service.login_user(login_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh", response_model=Token)
def refresh(
    token_data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service)
):
   
    try:
        return service.refresh_tokens(token_data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: UserResponse = Depends(get_current_user)
):
    
    return current_user

@router.get("/admin-test")
def admin_test(
    admin_user = Depends(check_admin)
):

    return {"message": f"Добро пожаловать, админ {admin_user.username}!"}