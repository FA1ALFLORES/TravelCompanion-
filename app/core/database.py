import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "travel_db.sqlite"


def init_db():
    """Инициализируем подключение к бд"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS hotels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, 
            address TEXT, 
            rating REAL)"""
    )
    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS places(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL, 
           type TEXT, 
           rating REAL)"""
    )
    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
    
    conn.commit()
    conn.close()
    print(f"Инициализация  {DB_PATH}")