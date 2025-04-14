from pymongo import MongoClient


def test_example():
    assert 1 == 1  # Simple sanity test to ensure pytest is working


    

def test_mongo_insert():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.test_db
    collection = db.test_collection
    result = collection.insert_one({"name": "test"})
    assert result.inserted_id is not None

def test_mongo_query():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.test_db
    collection = db.test_collection
    result = collection.find_one({"name": "test"})
    assert result is not None