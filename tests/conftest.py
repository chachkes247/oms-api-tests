import pytest
from pymongo import MongoClient

@pytest.fixture(scope="session")
def base_url():
    return "http://api:8000"  

@pytest.fixture
def auth_headers():
    token = "mock-jwt-token"
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_order():
    return {
        "user_id": "u_test_123",
        "items": [{
            "product_id": "p100",
            "name": "Test Product",
            "price": 100,
            "quantity": 2
        }],
        "total_price": 200,
        "status": "Pending"
    }

@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient("mongodb://mongo:27017")  # assumes mongo container is named "mongo"
    yield client
    client.close()
