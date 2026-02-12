import sqlite3
from typing import List
from modules.hotels.models import Hotel
from core.database import DB_PATH
import logging


logger = logging.getLogger(__name__)


class HotelRepository:
    def create_hotel(self, hotel: Hotel) -> Hotel:
        sql = """INSERT INTO hotels (name, address, rating) VALUES(?, ?, ?)"""
        try:        
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql, (hotel.name, hotel.address, hotel.rating))
            hotel_id = cursor.lastrowid
            conn.commit()
            
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:  
                conn.close()
        
        return Hotel(id=hotel_id, 
                     name=hotel.name, 
                     address=hotel.address, 
                     rating=hotel.rating)
                 
    def get_by_id(self, hotel_id: int) -> Hotel | None:
        sql = """Select * From hotels where id = ?"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute(sql, (hotel_id,)) 
            row = cursor.fetchone() #одну строку
            if row is None:
                return None
            
            hotel = Hotel(id=row[0], name=row[1], address=row[2], rating=row[3])
            
            return hotel 
        except sqlite3.Error as e:    
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:   
            if conn:
                conn.close()
        
                   
    def get_all(self, page: int=1, limit: int=10) -> List[Hotel]:
        offset = (page - 1) * limit
        sql = """select * from hotels LIMIT ? OFFSET ?""" 
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
       
        cursor.execute(sql,(limit, offset))
        rows = cursor.fetchall() #все строки
        
        hotels = []
        for row in rows:
            hotel = Hotel(id=row[0], name=row[1], address=row[2], rating=row[3])
            hotels.append(hotel)
        
        conn.close()    
        return hotels   
        
        
    def update_hotel(self, hotel_id: int, update_data: dict) -> Hotel | None:
     
        current_hotel = self.get_by_id(hotel_id)

        if current_hotel is None:
            return None
        
        updated_name = update_data.get("name", current_hotel.name)
        updated_address = update_data.get("address", current_hotel.address)
        updated_rating = update_data.get("rating", current_hotel.rating)    
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        sql = """UPDATE hotels SET name = ?, address = ?, rating = ? WHERE id = ?"""
        cursor.execute(sql, (updated_name, updated_address, updated_rating, hotel_id))
        
        conn.commit()
        conn.close()
        
        return Hotel(
            id=hotel_id,
            name=updated_name,
            address=updated_address,
            rating=updated_rating
        )
    
        
    def delete_hotel(self, hotel_id: int) -> bool:
        current_hotel = self.get_by_id(hotel_id)

        if current_hotel is None:
            return False

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        sql = "DELETE FROM hotels WHERE id = ?"
        cursor.execute(sql, (hotel_id,))

        conn.commit()
        conn.close()

        return True