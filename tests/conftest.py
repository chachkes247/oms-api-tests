import os
import time
import pytest
import requests
from pymongo import MongoClient

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_URL", "http://api:80")


@pytest.fixture(scope="session", autouse=True)
def wait_for_api(base_url):
    max_attempts = 10
    delay = 2
    for i in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                print("API is ready!")
                return
        except requests.exceptions.ConnectionError:
            pass
        print(f"Waiting for API... attempt {i + 1}")
        time.sleep(delay)
    raise Exception("API failed to become ready in time.")


@pytest.fixture
def auth_headers():
    # token = "mock-jwt-token"
    token = "test-token"
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
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    client = MongoClient(mongo_uri)
    yield client
    client.close()
    

@pytest.fixture
def clean_orders_collection(mongo_client):
    db = mongo_client["oms"]
    db["orders"].delete_many({})
    yield
    db["orders"].delete_many({})
