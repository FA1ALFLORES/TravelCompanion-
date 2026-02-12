from modules.places.models import Place
import sqlite3
from core.database import DB_PATH
from typing import List 
import logging



logger = logging.getLogger(__name__)


class PlaceRepository:
    def create_place(self, place: Place) -> Place:
        sql = """INSERT INTO places (name, type, address, rating) VALUES(?, ?, ?, ?)"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            type_str = place.type.value if hasattr(place.type, 'value') else place.type
            
            cursor.execute(sql,(place.name, type_str, place.address, place.rating))
            place_id = cursor.lastrowid
            conn.commit()
        
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
 
        return Place(id=place_id, 
                     name=place.name, 
                     type=type_str, 
                     address=place.address, 
                     rating=place.rating) 
    
    def get_by_id(self, place_id: int) -> Place | None:
        sql = """Select * From places where id = ?"""         
        try: 
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql,(place_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            
            place = Place(id=row[0], name=row[1], type=row[2], address=row[3], rating=row[4])

            return place
        except sqlite3.Error as e:          
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:
            if conn:
                conn.close()
                
    def get_all(self, page: int = 1, limit: int = 10) -> List[Place]:
        offset = (page - 1) * limit 
        sql = """select * from places LIMIT ? OFFSET ?""" 
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()          
        
        cursor.execute(sql,(limit, offset))
        rows = cursor.fetchall() 
        
        places = []
        for row in rows:
            place = Place(id=row[0], name=row[1], type=row[2], address=row[3], rating=row[4])
            places.append(place)
        
        conn.close()
        return places
    
    def update_place(self, place_id: int, update_data: dict) -> Place | None:
        
        current_place = self.get_by_id(place_id) 
        
        if current_place is None:
            return None
        
        updated_name = update_data.get("name",current_place.name)
        updated_type = update_data.get("type", current_place.type)
        updated_address = update_data.get("address", current_place.address)
        updated_rating = update_data.get("rating", current_place.rating)  
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()       
        
        sql = """UPDATE places SET name = ?, type = ? ,address = ?, rating = ? WHERE id = ? """  
        cursor.execute(sql,(updated_name, updated_type, updated_address, updated_rating, place_id)) 
          
        conn.commit()
        conn.close()
        
        return Place(
            id=place_id,
            name=updated_name,
            type=updated_type,
            address=updated_address,
            rating=updated_rating
        )  
        
    def delete_place(self, place_id: int) -> bool:
        current_place = self.get_by_id(place_id)
        
        if current_place is None:
            return False
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        sql = """DELETE from places where id = ?"""
        cursor.execute(sql, (place_id,))

        conn.commit()
        conn.close()
        
        return True  

                