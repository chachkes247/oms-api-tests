from pymongo import MongoClient


def test_example():
    print("\n\n\n1\n\n\n")
    assert 1 == 1  # Simple sanity test to ensure pytest is working


    

def test_mongo_insert():
    print("\n\n\n2\n\n\n")
    client = MongoClient("mongodb://localhost:27017/")
    db = client.test_db
    collection = db.test_collection
    result = collection.insert_one({"name": "test"})
    assert result.inserted_id is not None

def test_mongo_query():
    print("\n\n\n3\n\n\n")
    client = MongoClient("mongodb://localhost:27017/")
    db = client.test_db
    collection = db.test_collection
    result = collection.find_one({"name": "test"})
    assert result is not None