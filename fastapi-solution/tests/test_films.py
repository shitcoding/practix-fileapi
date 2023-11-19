from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app=app)


def test_list_films():
    response = client.get("/api/v1/films/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_similar_films():
    film_id = "35d4ecd5-0904-48bc-8989-dc355b86bfcd"
    response = client.get(f"api/v1/films/{film_id}/similar")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_films():
    query_params = {"query": "star", "page_number": 1, "page_size": 10}
    response = client.get("api/v1/films/search", params=query_params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_film_details():
    film_id = "35d4ecd5-0904-48bc-8989-dc355b86bfcd"
    response = client.get(f"api/v1/films/{film_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    response = client.get("/films/unknown")
    assert response.status_code == 404
