from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException, Request, Depends, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
import os


app = FastAPI()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.oms  # if oms DB doesn't exist yet, MongoDB will create it when you insert your first doc(BSON)
orders_collection = db.orders #then, in the DB I created, we can have collections such as "orders"


class Item(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int


class Order(BaseModel):
    user_id: str
    items: List[Item]
    total_price: float
    status: str = Field(default="Pending")


@app.post("/orders", status_code=201)
async def create_order(order: Order):
    order_dict = order.dict()
    result = await orders_collection.insert_one(order_dict)
    order_dict["_id"] = str(result.inserted_id)
    return JSONResponse(status_code=201, content=order_dict)


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    order = await orders_collection.find_one({"_id": obj_id})
    if not order:
        raise HTTPException(status_code=404, detail="Not Found")

    order["_id"] = str(order["_id"])
    return order


@app.patch("/orders/{order_id}")
async def update_order(order_id: str, update: dict):
    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await orders_collection.update_one({"_id": obj_id}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    updated_order = await orders_collection.find_one({"_id": obj_id})
    updated_order["_id"] = str(updated_order["_id"])
    return updated_order


@app.delete("/orders/{order_id}", status_code=204)
async def delete_order(order_id: str):
    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await orders_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return


@app.get("/health")
def health_check():
    return {"status": "ok"}
