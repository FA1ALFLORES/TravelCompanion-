class Hotel:
    def __init__(self,id: int, name: str, address: str, rating: float):
        self.id = id
        self.name = name
        self.address = address
        self.rating = rating
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "rating": self.rating 
        }
     
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            address=data["address"],
            rating=data["rating"]
        )         