from flask import Flask
from flask_restx import Api, Resource
from flask import request
from werkzeug.security import generate_password_hash
import json
import os

app = Flask(__name__)
api = Api(app, title='Travel API', version='1.0', description='API for Travel Service')

# Define a path for storing user data
USER_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users.json')

# Utility function to read user data from the file
def read_user_data():
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r') as f:
            return json.load(f)
    return {}

# Utility function to write user data to the file
def write_user_data(data):
    with open(USER_DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# Register Route
@api.route('/register')
class Register(Resource):
    def post(self):
        user_data = request.get_json()
        
        # Validate input
        if not user_data or 'name' not in user_data or 'email' not in user_data or 'password' not in user_data or 'role' not in user_data:
            return {"message": "Invalid input. Please provide all required fields."}, 400

        # Hash the password
        hashed_password = generate_password_hash(user_data['password'])

        # Read existing users and add the new user
        users = read_user_data()
        user_id = len(users) + 1
        user_data['password'] = hashed_password  # Store the hashed password
        user_data['id'] = user_id
        users[user_id] = user_data
        
        # Save the updated users data
        write_user_data(users)
        
        return {"message": "User registered successfully"}, 201

# Login Route
@api.route('/login')
class Login(Resource):
    def post(self):
        login_data = request.get_json()

        # Validate input
        if not login_data or 'email' not in login_data or 'password' not in login_data:
            return {"message": "Invalid input. Please provide email and password."}, 400
        
        # Simulate checking user credentials (you may need to implement authentication logic here)
        users = read_user_data()
        user = next((u for u in users.values() if u['email'] == login_data['email']), None)
        
        if user is None:
            return {"message": "User not found."}, 404

        # Normally, you'd check the password here, using something like bcrypt or werkzeug's check_password_hash.
        # For simplicity, we will skip the password validation here.
        
        # Return a mock token (you'd normally generate a real JWT token)
        return {"access_token": "your_token_here"}, 200

if __name__ == '__main__':
    app.run(debug=True)
