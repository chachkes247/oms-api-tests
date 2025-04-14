from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.oms  
orders_collection = db.orders


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


@app.get("/health")
def health_check():
    return {"status": "ok"}
