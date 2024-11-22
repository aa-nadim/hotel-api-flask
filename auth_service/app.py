import os
import ast
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from flasgger import Swagger

app = Flask(__name__)

# Swagger configuration
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "User Service API",
            "description": "API for user registration, authentication, and profile management",
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
    """
    claims = get_jwt()
    role = claims.get("role")

    if role == "Admin":
        return jsonify(
            {
                "message": "Authorized Admin. User can manage destinations like create, update, and delete. "
            }
        ), 200
    elif role == "User":
        return jsonify({"message": "Error: Administrator privileges are required to access this feature."}), 200
    else:
        return jsonify({"error": "Role not recognized"}), 403
    

if __name__ == "__main__":
    app.run(port=5003)
