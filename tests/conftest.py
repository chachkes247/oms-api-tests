import pytest
from unittest.mock import MagicMock


@pytest.fixture
def base_url():
    return "http://localhost:8000"


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
            }
        ],
        "total_price": 200,
        "status": "Pending"
    }


@pytest.fixture
def mongo_client():
    return MagicMock()



