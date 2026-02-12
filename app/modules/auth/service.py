import bcrypt 
import logging 
from modules.auth.models import User 
from modules.auth.schemas import UserCreate, UserLogin, Token, UserResponse
from modules.auth.repository import UserRepository
from modules.auth.jwt import create_tokens, verify_token

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    def register_user(self, user_data: UserCreate) -> UserResponse:
        
        hashed_password = self._hash_password(user_data.password) 
        
        user = User(
            id=0,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=False
        )   
        
        created_user = self.repository.create_user(user)
        
        return UserResponse(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            is_active=created_user.is_active,
            is_admin=created_user.is_admin,
            created_at=created_user.created_at.isoformat()
        )
        
    def get_current_user(self, user_id: int) -> UserResponse:   
        user = self.repository.get_by_id(user_id) 
        
        if not user:
            raise ValueError(f"Пользователь с {user_id} не найден")
        
        if not user.is_active:
            raise ValueError("Пользователь неактивирован")
        
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at.isoformat()
        )
        
        
    def login_user(self, login_data: UserLogin) -> Token:
        user = self.repository.get_by_email(login_data.email)
        
        fake_hash = "$5b$34$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        hash_to_check = user.hashed_password if user else fake_hash
        password_correct = self._verify_password(login_data.password, hash_to_check)
        
        if not user or not password_correct:
            raise ValueError("Неверный email или пароль")
        
        if not user.is_active:
            raise ValueError("Пользователь неактивирован")
        
        user_data = {
            "user_id": user.id,
            "email": user.email,
            "is_admin": user.is_admin
        }
        
        tokens = create_tokens(user_data) 
        
        return Token(**tokens) 
    
    def resrefh_tokens(self, refresh_token: str) -> Token:
        
        payload = verify_token(refresh_token, token_type="refresh")
        
        if not payload:
            raise ValueError("Невалидный или истёкший refresh токен")      
        
        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("Токен не содержит used_id")
        
        user =self.repository.get_by_id(user_id)
        
        if not user:
            raise ValueError("Пользователь не найден")
        
        if not user.is_active:
            raise ValueError("Пользователь неактивирован")
        
        user_data = {
            "user_id": user.id,
            "email": user.email,
            "is_admin": user.is_admin
        }
        
        tokens = create_tokens(user_data) 
        
        return Token(**tokens)