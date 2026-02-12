from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re


class UserBase(BaseModel):
    """Базовая модель пользователя"""
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Модель для создания пользователя"""
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Пароль должен содержать минимум 8 символов, хотя бы одну букву и одну цифру"
    )
    password_confirm: str = Field(..., description="Подтверждение пароля")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        """Проверка имени пользователя"""
        if not re.match(r'^[a-zA-Z0-9_.-]+$', value):
            raise ValueError(
                'Имя пользователя может содержать только буквы, цифры, точку, дефис и подчеркивание'
            )
        if value.isdigit():
            raise ValueError('Имя пользователя не может состоять только из цифр')
        return value.strip()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Проверка сложности пароля"""
        if len(value) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        if not re.search(r'[a-zA-Z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        # Дополнительная проверка на безопасность
        if value.lower() in ['password', '12345678', 'qwerty123']:
            raise ValueError('Пароль слишком простой')
        return value
    
    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, value: str, info) -> str:
        """Проверка совпадения паролей"""
        if 'password' in info.data and value != info.data['password']:
            raise ValueError('Пароли не совпадают')
        return value


class UserLogin(BaseModel):
    """Модель для входа пользователя"""
    email: EmailStr
    password: str = Field(..., min_length=1)
    
    @field_validator('password')
    @classmethod
    def password_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Пароль не может быть пустым')
        return value


class UserUpdate(BaseModel):
    """Модель для обновления пользователя"""
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    
    @field_validator('username')
    @classmethod
    def validate_username_update(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip()
            if len(value) < 2:
                raise ValueError('Имя пользователя должно содержать минимум 2 символа')
            if not re.match(r'^[a-zA-Z0-9_.-]+$', value):
                raise ValueError(
                    'Имя пользователя может содержать только буквы, цифры, точку, дефис и подчеркивание'
                )
        return value


class UserChangePassword(BaseModel):
    """Модель для смены пароля"""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    new_password_confirm: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Новый пароль должен содержать минимум 8 символов')
        if not re.search(r'[a-zA-Z]', value):
            raise ValueError('Новый пароль должен содержать хотя бы одну букву')
        if not re.search(r'\d', value):
            raise ValueError('Новый пароль должен содержать хотя бы одну цифру')
        return value
    
    @field_validator('new_password_confirm')
    @classmethod
    def new_passwords_match(cls, value: str, info) -> str:
        """Проверка совпадения новых паролей"""
        if 'new_password' in info.data and value != info.data['new_password']:
            raise ValueError('Новые пароли не совпадают')
        return value


class UserResponse(UserBase):
    """Модель для ответа с данными пользователя"""
    id: int
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class UserInDB(UserResponse):
    """Модель пользователя в БД (с хэшем пароля)"""
    hashed_password: str


class Token(BaseModel):
    """Модель токена"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = Field(
        3600,
        description="Время жизни токена в секундах"
    )


class TokenData(BaseModel):
    """Данные, хранящиеся в токене"""
    user_id: int
    username: str
    email: Optional[str] = None
    exp: Optional[int] = None
    scopes: list[str] = []


class RefreshTokenRequest(BaseModel):
    """Модель для запроса обновления токена"""
    refresh_token: str


class LoginResponse(BaseModel):
    """Ответ на успешный вход"""
    user: UserResponse
    token: Token


class RegisterResponse(BaseModel):
    """Ответ на успешную регистрацию"""
    user: UserResponse
    token: Token
    message: str = "Регистрация прошла успешно"



class OAuth2PasswordRequestForm(BaseModel):
    """Альтернатива форме OAuth2 из FastAPI"""
    username: Optional[str] = None
    email: Optional[str] = None
    password: str
    scope: str = ""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    grant_type: Optional[str] = "password"