from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, EmailStr
from typing import List

client = MongoClient("mongodb://admin:secret@127.0.0.1:27017/")
db = client["fastapi-db"]
users_collection = db['users']
orders_collections = db["orders"]

app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    
class Order(BaseModel):
    user_email: EmailStr
    product: str
    price: float
    

@app.post("/users/", response_model=dict)
def create_user(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status=400, detail=f"User already exists")
    
    user_dict = user.model_dump()
    result = users_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id), "message": "User added"}
    
@app.get("/users/", response_model=List[dict])
def get_users():
    users = list(users_collection.find({}, {"_id": 1, "name": 1, "email": 1, "age": 1}))
    for user in users:
        user["_id"] = str(user["_id"])
    return users

@app.post("/orders/", response_model=dict)
def create_order(order: Order):
    user = users_collection.find_one({"email": order.user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    order_dict = {"user_id": user["_id"], "product": order.product, "price": order.price}
    result = orders_collections.insert_one(order_dict)
    return {"id": str(result.inserted_id), "message": "Order created"}

@app.get("/orders/{email}", response_model=List[dict])
def get_order(email: str):
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status=404, detail="User not found")
    
    orders = list(orders_collections.find({"user_id": user["_id"]}))
    for order in orders:
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])
    return orders