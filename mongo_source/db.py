from pymongo import MongoClient

client = MongoClient("mongodb://admin:secret@localhost:27017/")

db = client["shop"]

user_collections = db["users"]
order_collections = db["orders"]