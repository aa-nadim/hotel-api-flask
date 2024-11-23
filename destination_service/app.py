# destination_service/app.py
import os
import ast
import uuid
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from flasgger import Swagger
import re

app = Flask(__name__)

# Swagger configuration
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Destination Service API",
            "description": "API for managing travel destinations",
            "version": "1.0.0",
        },
        "host": "127.0.0.1:5002",
        "basePath": "/",
        "schemes": ["http"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"',
            }
        },
        "security": [{"Bearer": []}],
    },
)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "your-secret-key"
jwt = JWTManager(app)

# Path to the Python file for storing destination data
DESTINATION_DATA_FILE = os.path.join(os.path.dirname(__file__), "destination_data.py")

# In-memory data to hold destinations
destinations = []

# Helper functions to load and save destination data
def load_destinations():
    """
    Load destinations from the destination_data.py file.
    """
    global destinations
    try:
        with open(DESTINATION_DATA_FILE, "r") as file:
            content = file.read()
            destinations = ast.literal_eval(content.split("=", 1)[1].strip())
    except (FileNotFoundError, SyntaxError, ValueError):
        destinations = []


def save_destinations():
    """
    Save the destinations list to the destination_data.py file.
    """
    global destinations
    with open(DESTINATION_DATA_FILE, "w") as file:
        file.write(f"destinations = {destinations}")


@app.before_request
def initialize_data():
    """
    Initialize data before processing any request.
    """
    global destinations
    if not destinations:
        load_destinations()


@app.teardown_appcontext
def persist_data(exception=None):
    """
    Save destination data to the destination_data.py file when the app shuts down.
    """
    save_destinations()


def validate_destination_data(data):
    """
    Validate the required fields and values for the destination data.
    """
    required_fields = ["name", "description", "location", "price_per_night"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return {"error": f"Missing fields: {', '.join(missing_fields)}"}, 400

    # Validate name length
    if len(data["name"]) < 3:
        return {"error": "Destination name must be at least 3 characters long."}, 400

    # Validate price per night (must be a positive float)
    try:
        price = float(data["price_per_night"])
        if price <= 0:
            return {"error": "Price per night must be a positive number."}, 400
    except ValueError:
        return {"error": "Invalid price format."}, 400

    return None, None


@app.route("/addDestinations", methods=["POST"])
@jwt_required()
def add_destination():
    """
    Add a New Destination (Admin only)
    --- 
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Destination name
              example: Bali
            description:
              type: string
              description: Short description of the destination
              example: A tropical paradise
            location:
              type: string
              description: Destination location
              example: Indonesia
            price_per_night:
              type: float
              description: Price per night in USD
              example: 200.5
    responses:
      201:
        description: Destination added successfully
      401:
        description: Unauthorized
      400:
        description: Missing fields or invalid data
    """
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Admin access required"}), 401

    data = request.get_json()

    # Validate the destination data
    error_response, status_code = validate_destination_data(data)
    if error_response:
        return jsonify(error_response), status_code

    destination = {
        "id": str(uuid.uuid4()),  # Generate a unique ID
        "name": data["name"],
        "description": data["description"],
        "location": data["location"],
        "price_per_night": data["price_per_night"],
    }
    destinations.append(destination)
    save_destinations()

    return jsonify({"message": "Destination added successfully", "destination": destination}), 201


@app.route("/destinations", methods=["GET"])
def get_destinations():
    """
    Get All Destinations
    ---
    responses:
      200:
        description: List of all destinations
    """
    return jsonify({"destinations": destinations}), 200


@app.route("/destinations/<string:id>", methods=["DELETE"])
@jwt_required()
def delete_destination(id):
    """
    Delete a Destination by ID (Admin only)
    ---
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: Destination ID
        example: 3f6b13f5-84d8-4e5d-b178-e2e4c9c69b33
    responses:
      200:
        description: Destination deleted successfully
      404:
        description: Destination not found
      401:
        description: Unauthorized
    """
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Admin access required"}), 401

    global destinations
    destination = next((d for d in destinations if d["id"] == id), None)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    destinations = [d for d in destinations if d["id"] != id]
    save_destinations()

    return jsonify({"message": "Destination deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
