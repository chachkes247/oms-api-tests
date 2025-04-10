import pytest
import requests
from pymongo import MongoClient


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"


@pytest.fixture(scope="session")
def auth_headers():
    # Replace with actual login if needed
    token = "mock-jwt-token"
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient("mongodb://localhost:27017")
    yield client
    client.close()


@pytest.fixture(scope="function")
def test_order():
    return {
        "user_id": "u_test_123",
        "items": [
            {"product_id": "p100", "name": "Test Product", "price": 100, "quantity": 2}
        ],
        "total_price": 200,
        "status": "Pending"
    }
