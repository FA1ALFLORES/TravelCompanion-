from modules.reviews.models import Review
import sqlite3
from core.database import DB_PATH
from typing import List 
import logging

logger = logging.getLogger(__name__)

class ReviewRepository:
    def create_review(self, review: Review) -> Review:
        sql = """INSERT INTO reviews (hotel_id, place_id, user_id, text, rating)
        VALUES(?, ?, ?, ?, ?)"""
        try: 
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql,(review.hotel_id, 
                                review.place_id, 
                                review.user_id, 
                                review.text, 
                                review.rating))
            review_id = cursor.lastrowid
            conn.commit()
            
            cursor.execute("SELECT created_at FROM reviews WHERE id = ?", (review_id,))
            created_at_row = cursor.fetchone()[0]
            
            if created_at_row is None:
                raise sqlite3.Error("Не удалось получить created_at для созданного отзыва")
        
            created_at = created_at_row[0]

        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
                
        return Review(
                      id=review_id, 
                      hotel_id=review.hotel_id, 
                      place_id=review.place_id, 
                      user_id=review.user_id, 
                      text=review.text, 
                      rating=review.rating,
                      created_at=created_at
                      )          
                
    def get_by_id(self, review_id: int) -> Review | None:
        sql = """Select * From reviews where id = ?"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql, (review_id,))
            row = cursor.fetchone()
            if row is None: 
                return None
            
            review = Review(
                            id=row[0],
                            hotel_id=row[1],
                            place_id=row[2],
                            user_id=row[3],
                            text=row[4],
                            rating=row[5],
                            created_at=row[6]
                            )
            return review
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:
            if conn:
                conn.close()
        
    def get_by_hotel_id(self, hotel_id: int, page: int = 1, limit: int = 10) -> list[Review]:
        offset = (page - 1) * limit
        sql = """select * from reviews where hotel_id = ? limit ? offset ?"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql,(hotel_id, limit, offset))
            rows = cursor.fetchall()
            
            reviews = []
            for row in rows:
                review = Review(
                        id=row[0],
                        hotel_id=row[1],
                        place_id=row[2],
                        user_id=row[3],
                        text=row[4],
                        rating=row[5],
                        created_at=row[6]
                         )    
                reviews.append(review)    
            return reviews
        
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:
            if conn:
                conn.close()     
            
    
    def get_by_place_id(self, place_id: int, page: int = 1, limit: int = 10) -> list[Review]:
        offset = (page - 1) * limit
        sql = """SELECT * FROM reviews WHERE place_id = ? LIMIT ? OFFSET ?"""
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql, (place_id, limit, offset))
            rows = cursor.fetchall()
            
            reviews = []
            for row in rows:
                review = Review(
                    id=row[0],
                    hotel_id=row[1],
                    place_id=row[2],
                    user_id=row[3],
                    text=row[4],
                    rating=row[5],
                    created_at=row[6]
                )
                reviews.append(review)
            
            return reviews
            
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:
            if conn:
                conn.close()
                
    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> list[Review]: 
        offset = (page - 1) * limit
        sql = """SELECT * FROM reviews WHERE user_id = ? LIMIT ? OFFSET ?"""
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql, (user_id, limit, offset))
            rows = cursor.fetchall()
            
            reviews = []
            for row in rows:
                review = Review(
                    id=row[0],
                    hotel_id=row[1],
                    place_id=row[2],
                    user_id=row[3],
                    text=row[4],
                    rating=row[5],
                    created_at=row[6]
                )
                reviews.append(review)
            
            return reviews
            
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:
            if conn:
                conn.close()
                            
                
    def update_review(self, review_id: int, update_data: dict) -> Review | None:
        current_review = self.get_by_id(review_id)
        
        if current_review is None:
            return None
        
        updated_text = update_data.get("text", current_review.text)
        updated_rating = update_data.get("rating", current_review.rating)
        
        sql = """UPDATE reviews Set text = ?, rating = ? WHERE id = ?"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute(sql,(updated_text, updated_rating, review_id))
            conn.commit()
            
            return Review(
                id=review_id,
                hotel_id=current_review.hotel_id,
                place_id=current_review.place_id,
                user_id=current_review.user_id,
                text=updated_text,
                rating=updated_rating,
                created_at=current_review.created_at
            )
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            if conn:
                conn.rollback()
                raise e
        finally:
            if conn:
                conn.close()    
        
    def delete_review(self,review_id: int) -> bool:        
        current_review = self.get_by_id(review_id)
        if current_review is None:
            return False
        
  
        sql = """DELETE FROM reviews WHERE id = ?"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql, (review_id,))
            conn.commit()
            
            return cursor.rowcount > 0  
            
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def get_all(self, page: int = 1, limit: int = 10) -> list[Review]: # все отзывы 
        
        offset = (page - 1) * limit
        sql = """SELECT * FROM reviews LIMIT ? OFFSET ?"""
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql, (limit, offset))
            rows = cursor.fetchall()
            
            reviews = []
            for row in rows:
                review = Review(
                    id=row[0],
                    hotel_id=row[1],
                    place_id=row[2],
                    user_id=row[3],
                    text=row[4],
                    rating=row[5],
                    created_at=row[6]
                )
                reviews.append(review)
            
            return reviews
            
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:
            if conn:
                conn.close()                    