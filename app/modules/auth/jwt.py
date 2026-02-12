import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from core.confing import settings

def create_tokens(user_data: Dict) -> Dict[str, str]:
    access_expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES)
    
    access_payload = {
        **user_data,
        "exp": access_expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    refresh_expire = datetime.utcnow() + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    refresh_payload = {
        "user_id": user_data["user_id"],
        "exp": refresh_expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    access_token = jwt.encode(
        access_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITM
    )
    
    refresh_token = jwt.encode(
        refresh_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITM 
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
def verify_token(token: str, token_type: str = "access") -> Optional[Dict]:
    try:
        paylaod = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )    
        
        if paylaod.get("type") != token_type:
            return None
        
        return paylaod
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None