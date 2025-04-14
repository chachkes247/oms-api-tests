from pymongo import MongoClient

def test_mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_db"]
    collection = db["test_collection"]

    # Insert a document
    result = collection.insert_one({"name": "ChatGPT"})
    assert result.inserted_id is not None

    # Fetch the document
    doc = collection.find_one({"name": "ChatGPT"})
    assert doc is not None
    assert doc["name"] == "ChatGPT"

    # Clean up
    collection.drop()
