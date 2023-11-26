from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app=app)


def test_genre_by_uuid():
    genre_id = "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"
    response = client.get(f"/api/v1/genres/{genre_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_genres_list():
    response = client.get("/api/v1/genres/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_genres_list_with_params():
    params = {"query": "comedy", "sort": "asc", "page_number": 1, "page_size": 5}
    response = client.get("/api/v1/genres/", params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
