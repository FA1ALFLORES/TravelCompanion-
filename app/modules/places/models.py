class Place:
    def __init__(self, id: int, name: str, type: str, address: str, rating: float):
        self.id = id
        self.name = name
        self.type = type
        self.address = address
        self.rating = rating
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "address": self.address,
            "rating": self.rating 
        }
     
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            address=data["address"],
            rating=data["rating"]
        )         
        
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row[0],
            name=row[1],
            type=row[2],
            address=row[3],
            rating=row[4]
        )   