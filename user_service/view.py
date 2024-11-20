from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import UserModel
from validation import validate_registration, validate_login

class RegisterView(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Name is required")
        parser.add_argument("email", required=True, help="Email is required")
        parser.add_argument("password", required=True, help="Password is required")
        parser.add_argument("role", choices=("Admin", "User"), required=True, help="Role must be 'Admin' or 'User'")
        args = parser.parse_args()

        # Validate input
        errors = validate_registration(args)
        if errors:
            return {"errors": errors}, 400

        # Check if email exists
        if UserModel.find_user_by_email(args["email"]):
            return {"message": "Email already registered"}, 400

        # Create user
        UserModel.create_user(args["name"], args["email"], args["password"], args["role"])
        return {"message": "User registered successfully"}, 201

class LoginView(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email is required")
        parser.add_argument("password", required=True, help="Password is required")
        args = parser.parse_args()

        # Validate input
        errors = validate_login(args)
        if errors:
            return {"errors": errors}, 400

        # Authenticate user
        user = UserModel.find_user_by_email(args["email"])
        if not user or not UserModel.verify_password(user["password"], args["password"]):
            return {"message": "Invalid email or password"}, 401

        # Generate token
        token = create_access_token(identity={"email": user["email"], "role": user["role"]})
        return {"access_token": token}, 200

class ProfileView(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = UserModel.find_user_by_email(identity["email"])
        if not user:
            return {"message": "User not found"}, 404

        return {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
