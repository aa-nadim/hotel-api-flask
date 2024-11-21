import os
import ast
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
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
        "host": "127.0.0.1:5001",  
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

# Path to the Python file for storing user data
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), "user_data.py")
users = []
is_data_initialized = False  # Flag to ensure data is loaded only once


def load_users():
    """
    Load users from the user_data.py file into the global users list.
    """
    global users
    try:
        with open(USER_DATA_FILE, "r") as file:
            content = file.read()
            users = ast.literal_eval(content.split("=", 1)[1].strip())
    except (FileNotFoundError, SyntaxError, ValueError):
        users = []


def save_users():
    """
    Save the global users list to the user_data.py file.
    """
    global users
    with open(USER_DATA_FILE, "w") as file:
        file.write(f"users = {users}")


@app.before_request
def initialize_data():
    """
    Initialize data before processing any request, but only once.
    """
    global is_data_initialized
    if not is_data_initialized:
        load_users()
        is_data_initialized = True


@app.teardown_appcontext
def persist_data(exception=None):
    """
    Save user data to the user_data.py file when the application shuts down.
    """
    save_users()


@app.route("/register", methods=["POST"])
def register_user():
    """
    Register a New User
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email
              example: user@example.com
            password:
              type: string
              description: User's password
              example: password123
            name:
              type: string
              description: User's full name
              example: John Doe
            role:
              type: string
              description: User's role (User or Admin)
              example: User
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input or email already registered
    """
    global users
    data = request.get_json()

    # Validate that all required fields are provided
    required_fields = ["email", "password", "name", "role"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Validate role
    valid_roles = ["User", "Admin"]
    if data["role"] not in valid_roles:
        return jsonify({"error": f"Invalid role. Allowed roles: {', '.join(valid_roles)}"}), 400

    # Check if email is already registered
    if any(user["email"] == data["email"] for user in users):
        return jsonify({"error": "Email already registered"}), 400

    # Add the new user to the users list
    hashed_password = generate_password_hash(data["password"])
    users.append(
        {
            "email": data["email"],
            "name": data["name"],
            "password": hashed_password,
            "role": data["role"],
        }
    )

    save_users()  # Save the updated users list
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Authenticate a User
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email
              example: user@example.com
            password:
              type: string
              description: User's password
              example: password123
    responses:
      200:
        description: Login successful
      400:
        description: Missing email or password
      401:
        description: Invalid credentials
    """
    global users
    data = request.get_json()

    # Validate input
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    # Find user by email
    user = next((u for u in users if u["email"] == data["email"]), None)
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token with additional claims
    token = create_access_token(
        identity=user["email"], additional_claims={"role": user["role"]}
    )

    return jsonify({"token": token}), 200


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    Get Profile Information
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: User's profile details
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email
            role:
              type: string
              description: User's role
      401:
        description: Unauthorized
    """
    current_user = get_jwt_identity()  
    claims = get_jwt()  

    return jsonify({
        "email": current_user,   
        "role": claims.get("role")  
    }), 200


if __name__ == "__main__":
    app.run(port=5001)