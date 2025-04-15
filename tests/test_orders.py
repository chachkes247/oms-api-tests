import time
import requests

def wait_for_api(base_url, max_attempts=10, delay=2):
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

def test_health_check(base_url):
    wait_for_api(base_url)
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
    
# def test_mongo_insert(mongo_client):
#     db = mongo_client.test_db
#     collection = db.test_collection
#     result = collection.insert_one({"name": "test"})
#     assert result.inserted_id is not None


# def test_mongo_query(mongo_client):
#     db = mongo_client.test_db
#     collection = db.test_collection
#     result = collection.find_one({"name": "test"})
#     assert result is not None


# def test_create_order(base_url, auth_headers, test_order, mongo_client):
#     response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
#     assert response.status_code == 201
#     order_id = response.json()["_id"]

#     db_order = mongo_client["oms"]["orders"].find_one({"_id": order_id})
#     assert db_order is not None
#     assert db_order["status"] == "Pending"


# def test_get_order(base_url, auth_headers, test_order, mongo_client):
#     response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
#     order_id = response.json()["_id"]

#     get_response = requests.get(f"{base_url}/orders/{order_id}", headers=auth_headers)
#     assert get_response.status_code == 200
#     assert get_response.json()["_id"] == order_id


# @pytest.mark.parametrize("new_status", ["Processing", "Shipped", "Delivered"])
# def test_update_order_status(base_url, auth_headers, test_order, mongo_client, new_status):
#     response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
#     order_id = response.json()["_id"]

#     patch_response = requests.patch(f"{base_url}/orders/{order_id}", json={"status": new_status}, headers=auth_headers)
#     assert patch_response.status_code == 200
#     assert patch_response.json()["status"] == new_status

#     db_order = mongo_client["oms"]["orders"].find_one({"_id": order_id})
#     assert db_order["status"] == new_status


# def test_delete_order(base_url, auth_headers, test_order, mongo_client):
#     response = requests.post(f"{base_url}/orders", json=test_order, headers=auth_headers)
#     order_id = response.json()["_id"]

#     del_response = requests.delete(f"{base_url}/orders/{order_id}", headers=auth_headers)
#     assert del_response.status_code == 204

#     db_order = mongo_client["oms"]["orders"].find_one({"_id": order_id})
#     assert db_order is None


# def test_update_nonexistent_order(base_url, auth_headers):
#     fake_id = "nonexistent123"
#     patch_response = requests.patch(f"{base_url}/orders/{fake_id}", json={"status": "Shipped"}, headers=auth_headers)
#     assert patch_response.status_code == 404
