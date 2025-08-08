
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_recipe():
    # Пример входных данных, соответствующих schemas.RecipeIn
    payload = {
        "title_of_dish": "Test Dish",
        "description": "Test Description",
        "ingredients": "Ingredient1, Ingredient2",
        "preparing_time_in_min": 30,
        "view_count": 0
    }
    response = client.post("/recipes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title_of_dish"] == payload["title_of_dish"]
    assert data["description"] == payload["description"]
    assert "id" in data
    assert "view_count" in data  # если это поле есть в response_model

def test_get_recipes():
    response = client.get('/recipes/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Если есть данные — проверяем поля первого рецепта
    if data:
        first = data[0]
        assert "title_of_dish" in first
        assert "view_count" in first
        assert "preparing_time_in_min" in first

def test_get_recipe_by_id():
    idx = 1
    response = client.get(f"/recipes/{idx}")
    assert response.status_code == 200
    data = response.json()
    assert "title_of_dish" in data
    assert "description" in data
    assert "ingredients" in data
    assert "preparing_time_in_min" in data