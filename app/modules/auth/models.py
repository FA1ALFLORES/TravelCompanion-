class User:
    def __init__(self, id: int, username: str, email: str, hashed_password: str,
                 created_at: str = "", deleted_at: str | None = None):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = created_at
        self.deleted_at = deleted_at
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at
            # Никогда не возвращаем пароль!
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", 0),
            username=data["username"],
            email=data["email"],
            hashed_password=data["hashed_password"],
            created_at=data.get("created_at", ""),
            deleted_at=data.get("deleted_at")
        )
        
    @classmethod 
    def active(self) -> bool:
        return self.deleted_at is None       