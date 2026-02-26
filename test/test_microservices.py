import pytest
import requests

AUTH_URL = "http://127.0.0.1:8000"
ORDER_URL = "http://127.0.0.1:8001"

pytestmark = pytest.mark.focus

def test_full_flow():

    # Opret bruger
    requests.post(f"{AUTH_URL}/register_user", json={
        "username": "test@test.com",
        "password": "1234",
        "first_name": "Test",
        "last_name": "User",
        "roles": ["user"]
    })

    # Få token
    token_response = requests.post(f"{AUTH_URL}/get_bearer_token", json={
        "username": "test@test.com",
        "password": "1234"
    })

    token = token_response.json()["token"]

    # Opret ordre
    order_response = requests.post(
        f"{ORDER_URL}/orders",
        params={"product": "Laptop"},
        headers={"token": token}
    )

    assert order_response.status_code == 200

    # Hent ordre
    get_response = requests.get(
        f"{ORDER_URL}/orders",
        headers={"token": token}
    )

    assert get_response.status_code == 200
    assert "Laptop" in get_response.json()["orders"]