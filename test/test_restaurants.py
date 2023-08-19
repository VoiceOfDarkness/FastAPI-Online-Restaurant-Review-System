from fastapi.testclient import TestClient

from api import restaurant

client = TestClient(restaurant.res_router)


def rest_restaurant_index():
    response = client.get("/api/v1/restaurant/index")
    assert response.status_code == 200
    assert response.text == "The Restaurants"
