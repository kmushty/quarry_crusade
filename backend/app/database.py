# app/database.py
from . import mongo

def get_active_routes():
    return list(mongo.db.routes.find({"status": "active"}))

def create_route(route_data):
    return mongo.db.routes.insert_one(route_data)

def update_vehicle_status(vehicle_id, status_data):
    mongo.db.vehicles.update_one({"vehicle_id": vehicle_id}, {"$set": status_data})

