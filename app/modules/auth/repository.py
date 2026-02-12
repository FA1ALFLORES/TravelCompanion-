from passlib.context import CryptContext
from modules.auth.models import User
from modules.auth.schemas import UserCreate
import sqlite3
from core.database import DB_PATH
import logging  

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository: 
    def __init__(self):
        self.pwd_context = pwd_context
    
    
    def create_user(self, user_data: UserCreate) -> User:
        sql = """INSERT INTO  users(username, email, hashed_password) VALUES(?, ?, ?)"""
        try: 
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if self.get_by_username(user_data.username):
                raise ValueError(f"Имя пользователя {user_data.username} уже занято")    
            if self.get_by_email(user_data.email):
                raise ValueError(f"Email {user_data.email} уже используется")        
            
            hashed_password = self.pwd_context.hash(user_data.password)

            cursor.execute(sql, (user_data.username, user_data.email, hashed_password))
            user_id = cursor.lastrowid
            
            cursor.execute("SELECT created_at From users WHERE id =?", (user_id,))
            created_at_row = cursor.fetchone()
            created_at = created_at_row[0] if created_at_row else "" 
        
        except sqlite3.Error as e:
            logger.error(f"Ошибка бд в создание пользователя: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
        
        return User(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            created_at=created_at,
            deleted_at=None
        )               
        
    def get_by_id(self, user_id: int) -> User | None:
        sql = """SELECT * FROM users where id = ?"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql,(user_id,))
            row = cursor.fetchone()
            if row is None:
                return None 
            
            user = User(id=row[0], username=row[1], email=row[2], hashed_password=row[3])
            
            return user
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе: {e}")
            raise e
        finally:
            if conn:
                conn.close()
            
        
    def get_by_email(self, email: str) -> User | None:
        sql = """SELECT * FROM users WHERE email = ? AND deleted_at IS NULL"""

        try: 
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql,(email,))
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            return User.from_db_row(row)
        
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе по email: {e}")
            raise e
        finally:
            if conn:
                conn.close()    
            
    def get_by_username(self, username: str) -> User | None:
        sql = """SELECT * FROM users WHERE username = ? AND deleted_at IS NULL"""

        try: 
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(sql,(username,))
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            return User.from_db_row(row)
        
        except sqlite3.Error as e:
            logger.error(f"Ошибка в базе по username: {e}")
            raise e
        finally:
            if conn:
                conn.close()  
        
    
    def update_user(self, user_id: int, update_data: dict) -> User | None:
        
        current_user = self.get_by_id(user_id)
        
        if current_user is None:
            return None
        
        updated_email = update_data.get("email", current_user.email)
        updated_username = update_data.get("username", current_user.username)
        updated_hashed_password = update_data.get("hashed_password", current_user.hashed_password)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        sql = """UPDATE users SET email = ?, username = ?, hashed_password = ? WHERE id = ?""" 
        cursor.execute(sql, (updated_email, updated_username, updated_hashed_password, user_id))
        
        conn.commit()
        conn.close()
        
        return User(
            id=user_id,
            username=updated_username,
            email=updated_email,
            hashed_password=updated_hashed_password
        )
        
    def delete_user(self, user_id: int) -> bool:
        current_user = self.get_by_id(user_id) 
        
        if current_user is None:
            return False
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            sql = "UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(sql,(user_id,)) 
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Ошибка БД при удалении пользователя: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()    
        
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)