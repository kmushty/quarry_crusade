from pymongo import MongoClient
import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/quarry_crusade")
client = MongoClient(MONGO_URI)
db = client.quarry_crusade

def get_active_routes():
    return list(db.routes.find({"status": "active"}))

def create_route(route_data):
    return db.routes.insert_one(route_data)

def update_route_status(route_id, status):
    return db.routes.update_one(
        {"_id": route_id},
        {"$set": {"status": status}}
    )