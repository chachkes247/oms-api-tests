import pymongo
import pytest

def test_pymongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
    try:
        client.server_info()  # Will throw if can't connect
    except Exception as e:
        pytest.fail(f"Could not connect to MongoDB: {e}")
