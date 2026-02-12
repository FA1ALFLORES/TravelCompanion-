from fastapi.testclient import TestClient

def test_create_hotel_review(client: TestClient, test_hotel, auth_headers):
    """Тест создания отзыва на отель"""
    response = client.post("/reviews/hotel/", 
        json={
            "hotel_id": test_hotel.id,
            "user_id": 1,  # Будет заменено на из токена
            "text": "Отличный отель!",
            "rating": 5
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["hotel_id"] == test_hotel.id
    assert data["text"] == "Отличный отель!"


def test_create_place_review(client: TestClient, test_place, auth_headers):
    """Тест создания отзыва на место"""
    response = client.post("/reviews/place/", 
        json={
            "place_id": test_place.id,
            "user_id": 1,
            "text": "Отличное место!",
            "rating": 5
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["place_id"] == test_place.id


def test_get_hotel_reviews(client: TestClient, test_hotel, test_hotel_review):
    """Тест получения отзывов отеля"""
    response = client.get(f"/reviews/hotel/{test_hotel.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["hotel_id"] == test_hotel.id