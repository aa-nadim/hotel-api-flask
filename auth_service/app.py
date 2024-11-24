# auth_service/app.py
import os
import ast
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from werkzeug.exceptions import Unauthorized
from flasgger import Swagger
import re

app = Flask(__name__)

# Swagger configuration
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Auth Service API",
            "description": "API for managing authentication and role-based access",
            "version": "1.0.0",
        },
        "host": "127.0.0.1:5003",  
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

@app.route("/auth", methods=["GET"])
@jwt_required()
def get_destinations():
    """
    Get Destinations with Role-based Access
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Role-based message and list of destinations
      403:
        description: Role not recognized
      401:
        description: Missing or invalid JWT token
    """
    claims = get_jwt()
    role = claims.get("role")

    # Validate role
    if not role:
        return jsonify({"error": "Role not found in token."}), 400

    if role == "Admin":
        return jsonify(
            {
                "message": "Authorized Admin. User can manage destinations like create, update, and delete."
            }
        ), 200
    elif role == "User":
        return jsonify({"message": "Unauthorized Admin. Administrator privileges are required to access this feature."}), 200
    else:
        # If the role is not recognized, return a 403 Forbidden status
        return jsonify({"error": "Role not recognized"}), 403

@app.errorhandler(Unauthorized)
def handle_unauthorized(error):
    """
    Handle 401 Unauthorized error when the token is missing or invalid.
    This will return the expected error message: "Missing or invalid JWT token."
    """
    return jsonify({"error": "Missing or invalid JWT token."}), 401

@app.errorhandler(422)
def handle_invalid_token(error):
    """
    Handle 422 Unprocessable Entity when the token is invalid or malformed.
    This will return a custom error message: "Invalid token format or signature."
    """
    return jsonify({"error": "Invalid token format or signature."}), 422

@app.errorhandler(403)
def handle_forbidden(error):
    """
    Handle 403 Forbidden error when the role is not recognized.
    This will return the error message: "Role not recognized."
    """
    return jsonify({"error": "Role not recognized"}), 403

# Additional validation for JWT token structure
def validate_jwt_token(token):
    """
    Custom function to validate the JWT token structure.
    This will check if the token is in the correct format: "Bearer {token}"
    """
    if not token.startswith("Bearer "):
        return jsonify({"error": "Token should start with 'Bearer '"}), 400
    if len(token.split(" ")) != 2:
        return jsonify({"error": "Invalid token format."}), 400
    return None

# @app.before_request
# def validate_authorization_header():
#     """
#     Middleware to validate the Authorization header format before every request.
#     """
#     auth_header = request.headers.get('Authorization', None)
#     if auth_header:
#         print(f"Authorization Header Received: {auth_header}")  # Debug log
#         validation_error = validate_jwt_token(auth_header)
#         if validation_error:
#             return validation_error
#     else:
#         print("Authorization Header Missing")  # Debug log
#         return jsonify({"error": "Authorization header is missing"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)

