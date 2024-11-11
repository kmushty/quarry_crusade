# app/routes.py
from flask import Blueprint, request, jsonify
from .database import get_active_routes, create_route, update_vehicle_status
from . import socketio

main = Blueprint("main", __name__)

@main.route("/routes", methods=["GET"])
def fetch_active_routes():
    active_routes = get_active_routes()
    return jsonify(active_routes), 200

@main.route("/route", methods=["POST"])
def create_new_route():
    data = request.json
    create_route(data)
    socketio.emit("route_update", data)
    return jsonify({"message": "Route created"}), 201

@main.route("/vehicle/<vehicle_id>/status", methods=["POST"])
def update_vehicle(vehicle_id):
    status_data = request.json
    # update the DB
    update_vehicle_status(vehicle_id, status_data)
    # update the web app
    socketio.emit("vehicle_update", {"vehicle_id": vehicle_id, **status_data})
    return jsonify({"message": "Vehicle status updated"}), 200

