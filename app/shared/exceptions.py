from fastapi import HTTPException, status


class TravelCompanionException(HTTPException):
    pass

class NotFoundExeption(TravelCompanionException):
    def __init__(self, detail: str = "Ресурс не найден"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail 
        )
        
class UnauthorizedException(TravelCompanionException):
    def __init__(self, detail: str = "Требуется авторизация"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail 
        )
        
class ForbiddenException(TravelCompanionException):
    def __init__(self, detail: str = "Недостаточно прав"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail 
        )
        
class ValidationException(TravelCompanionException):
    def __init__(self, detail: str = "Ошибка валидации"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail 
        )