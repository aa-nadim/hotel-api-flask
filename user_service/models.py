import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

DATA_FILE = os.path.join("user_service/data", "data.json")

class UserModel:
    @staticmethod
    def load_data():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_data(data):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # Ensure the directory exists
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def create_user(name, email, password, role):
        users = UserModel.load_data()
        hashed_password = generate_password_hash(password)
        users.append({"name": name, "email": email, "password": hashed_password, "role": role})
        UserModel.save_data(users)

    @staticmethod
    def find_user_by_email(email):
        users = UserModel.load_data()
        for user in users:
            if user["email"] == email:
                return user
        return None

    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)
