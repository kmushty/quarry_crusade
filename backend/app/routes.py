from flask import Blueprint, request, jsonify
from .database import get_active_routes, create_route, update_vehicle_status
from . import socketio

main = Blueprint("main", __name__)

@main.route("/api/routes", methods=["GET"])
def fetch_active_routes():
    active_routes = get_active_routes()
    
    if not active_routes:
        return jsonify({"message": "No active routes available"}), 200  # Return an empty array if no routes exist
    return jsonify(active_routes), 200

@main.route("/api/route", methods=["POST"])
def create_new_route():
    try:
        data = request.json
        if "route_name" not in data:
            return jsonify({"error": "Missing 'route_name' in request"}), 400
        
        create_route(data)  # Insert route data into DB
        socketio.emit("route_update", data)  # Emit WebSocket event for frontend update
        return jsonify({"message": "Route created"}), 201
    except Exception as e:
        app.logger.error(f"Error creating route: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@main.route("/api/vehicle/<vehicle_id>/status", methods=["POST"])
def update_vehicle(vehicle_id):
    status_data = request.json
    update_vehicle_status(vehicle_id, status_data)  # Update vehicle status in DB
    socketio.emit("vehicle_update", {"vehicle_id": vehicle_id, **status_data})  # Emit WebSocket event for frontend update
    return jsonify({"message": "Vehicle status updated"}), 200
