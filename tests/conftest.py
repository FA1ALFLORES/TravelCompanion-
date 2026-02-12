import pytest
import sqlite3
from pathlib import Path
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from core.database import DB_PATH, init_db
from modules.auth.models import User
from modules.auth.repository import UserRepository
from modules.auth.jwt import create_access_token
from modules.hotels.repository import HotelRepository
from modules.hotels.models import Hotel
from modules.places.repository import PlaceRepository
from modules.places.models import Place
from modules.reviews.repository import ReviewRepository
from modules.reviews.models import Review


@pytest.fixture(scope="session")
def test_db():
    """Тестовая БД"""
    test_db_path = Path(__file__).parent / "test_travel_db.sqlite"
    original_db_path = DB_PATH
    
    
    import core.database
    core.database.DB_PATH = test_db_path
    
   
    init_db()
    
    yield test_db_path
    
   
    if test_db_path.exists():
        test_db_path.unlink()
    core.database.DB_PATH = original_db_path


@pytest.fixture
def client():
    """Тестовый клиент FastAPI"""
    return TestClient(app)


@pytest.fixture
def db_connection(test_db):
    """Соединение с тестовой БД"""
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture
def clear_db(db_connection):
    """Очистка БД после каждого теста"""
    yield
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM reviews")
    cursor.execute("DELETE FROM hotels")
    cursor.execute("DELETE FROM places")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM sqlite_sequence")  
    db_connection.commit()



@pytest.fixture
def hotel_repository():
    """Репозиторий отелей"""
    return HotelRepository()


@pytest.fixture
def test_hotel(hotel_repository):
    """Тестовый отель"""
    from modules.hotels.schemas import HotelCreate
    
    hotel_data = HotelCreate(
        name="Тестовый отель",
        address="ул. Тестовая, 1",
        rating=4.5
    )
    
    return hotel_repository.create_hotel(hotel_data)



@pytest.fixture
def place_repository():
    """Репозиторий мест"""
    return PlaceRepository()


@pytest.fixture
def test_place(place_repository):
    """Тестовое место"""
    from modules.places.schemas import PlaceCreate
    from modules.places.schemas import PlaceType
    
    place_data = PlaceCreate(
        name="Тестовое место",
        type=PlaceType.RESTAURANT,
        address="ул. Тестовая, 2",
        rating=4.8
    )
    
    return place_repository.create_place(place_data)



@pytest.fixture
def user_repository():
    """Репозиторий пользователей"""
    return UserRepository()


@pytest.fixture
def test_user(user_repository):
    """Тестовый пользователь"""
    from modules.auth.schemas import UserCreate
    
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="Test12345",
        password_confirm="Test12345"
    )
    
    return user_repository.create_user(user_data)


@pytest.fixture
def auth_headers(test_user):
    """Заголовки авторизации"""
    access_token = create_access_token({"user_id": test_user.id})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def review_repository():
    """Репозиторий отзывов"""
    return ReviewRepository()


@pytest.fixture
def test_hotel_review(review_repository, test_hotel, test_user):
    """Тестовый отзыв на отель"""
    from modules.reviews.models import Review
    
    review = Review(
        id=0,
        hotel_id=test_hotel.id,
        place_id=None,
        user_id=test_user.id,
        text="Отличный отель!",
        rating=5,
        created_at=""
    )
    
    return review_repository.create_review(review)


@pytest.fixture
def test_place_review(review_repository, test_place, test_user):
    """Тестовый отзыв на место"""
    from modules.reviews.models import Review
    
    review = Review(
        id=0,
        hotel_id=None,
        place_id=test_place.id,
        user_id=test_user.id,
        text="Отличное место!",
        rating=5,
        created_at=""
    )
    
    return review_repository.create_review(review)