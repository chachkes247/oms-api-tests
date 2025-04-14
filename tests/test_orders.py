from pymongo import MongoClient
import pytest
import requests

def test_mongo_insert(mongo_client):
    client = mongo_client
    db = client.test_db
    collection = db.test_collection
    result = collection.insert_one({"name": "test"})
    assert result.inserted_id is not None


def test_mongo_query(mongo_client):
    client = mongo_client
    db = client.test_db
    collection = db.test_collection
    result = collection.find_one({"name": "test"})
    assert result is not None
    
    
def test_create_order(base_url, auth_headers, test_order, mongo_client):
    response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    order_id = data["_id"]

    # Validate in MongoDB
    db_order = mongo_client["oms"]["orders"].find_one({"_id": order_id})
    assert db_order is not None
    assert db_order["status"] == "Pending"


def test_get_order(base_url, auth_headers, test_order, mongo_client):
    # First, create the order
    response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
    order_id = response.json()["_id"]

    # Now, fetch it
    get_response = requests.get(f"{base_url}/orders/{order_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["_id"] == order_id


@pytest.mark.parametrize("new_status", ["Processing", "Shipped", "Delivered"])
def test_update_order_status(base_url, auth_headers, test_order, mongo_client, new_status):
    response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
    order_id = response.json()["_id"]

    patch_response = requests.patch(f"{base_url}/orders/{order_id}", json={"status": new_status}, headers=auth_headers)
    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == new_status

    db_order = mongo_client["oms"]["orders"].find_one({"_id": order_id})
    assert db_order["status"] == new_status


def test_delete_order(base_url, auth_headers, test_order, mongo_client):
    response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
    order_id = response.json()["_id"]

    del_response = requests.delete(f"{base_url}/orders/{order_id}", headers=auth_headers)
    assert del_response.status_code == 204

    db_order = mongo_client["oms"]["orders"].find_one({"_id": order_id})
    assert db_order is None


def test_update_nonexistent_order(base_url, auth_headers):
    fake_id = "nonexistent123"
    patch_response = requests.patch(f"{base_url}/orders/{fake_id}", json={"status": "Shipped"}, headers=auth_headers)
    assert patch_response.status_code == 404