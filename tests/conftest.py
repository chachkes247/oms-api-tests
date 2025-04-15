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
