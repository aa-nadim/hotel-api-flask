from flask import jsonify, request
from users_models import users
from user_validation import validate_user_registration, validate_login
from utils.jwt_utils import generate_token

class UserController:
    def __init__(self, app):
        @app.route("/register", methods=["POST"])
        def register_user():
            data = request.json
            error = validate_user_registration(data)
            if error:
                return jsonify({"error": error}), 400
            data["id"] = len(users) + 1
            users.append(data)
            return jsonify({"message": "User registered successfully"}), 201

        @app.route("/login", methods=["POST"])
        def login_user():
            data = request.json
            user, error = validate_login(data, users)
            if error:
                return jsonify({"error": error}), 401
            token = generate_token(user)
            return jsonify({"token": token}), 200
