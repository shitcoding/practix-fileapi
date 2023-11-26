from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app=app)


def test_person_by_uuid():
    person_id = "00591223-0fd4-4a5f-89f8-0317eff58c1b"
    response = client.get(f"/api/v1/persons/{person_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_person_not_found():
    response = client.get("/api/v1/persons/non-existing-person-uuid")
    assert response.status_code == 404
    assert "Person not found" in response.text


def test_persons_list():
    response = client.get("/api/v1/persons/search/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_persons_list_with_params():
    params = {"query": "John Doe", "sort": "asc", "page_number": 1, "page_size": 5}
    response = client.get("/api/v1/persons/search/", params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_person_films():
    person_id = "valid-person-uuid"
    response = client.get(f"/api/v1/persons/{person_id}/films")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_person_films_with_sort_and_pagination():
    person_id = "00591223-0fd4-4a5f-89f8-0317eff58c1b"
    params = {"sort": "desc", "page_number": 1, "page_size": 5}
    response = client.get(f"/api/v1/persons/{person_id}/films", params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
