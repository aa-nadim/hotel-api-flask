# user_service/__tests__/test_user_service.py
import pytest
import os
import shutil
from user_service.app import app, USER_DATA_FILE, load_users, save_users
import re

# Backup file for original data
TEMP_USER_DATA_FILE = f"{USER_DATA_FILE}.backup"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Setup and teardown for tests.
    Temporarily empties user_data.py and restores it after the tests.
    """
    # Backup the original user data file
    if os.path.exists(USER_DATA_FILE):
        shutil.copy(USER_DATA_FILE, TEMP_USER_DATA_FILE)
    else:
        # Create an empty file if it doesn't exist
        open(USER_DATA_FILE, 'w').close()

    # Initialize with empty user data
    save_users()

    yield  # Run the tests

    # Restore the original user data file
    if os.path.exists(TEMP_USER_DATA_FILE):
        shutil.move(TEMP_USER_DATA_FILE, USER_DATA_FILE)
    else:
        os.remove(USER_DATA_FILE)


@pytest.fixture
def client():
    """
    Flask test client fixture.
    """
    app.config["TESTING"] = True
    return app.test_client()


def test_register_user(client):
    """
    Test user registration with valid input.
    """
    data = {
        "email": "newuser@example.com",
        "password": "Password123",
        "name": "New User",
        "role": "User",
    }
    response = client.post("/register", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_register_user_already_exists(client):
    """
    Test registration with an already existing user.
    """
    data = {
        "email": "existinguser@example.com",
        "password": "Password123",
        "name": "Existing User",
        "role": "User",
    }
    # Register the user first
    client.post("/register", json=data)
    # Try registering the same user again
    response = client.post("/register", json=data)
    assert response.status_code == 400
    assert response.json["error"] == "Email already registered"


def test_register_user_missing_fields(client):
    """
    Test registration with missing required fields.
    """
    data = {
        "email": "missingfields@example.com",
        "password": "password123",
        "role": "User",
    }
    response = client.post("/register", json=data)
    assert response.status_code == 400
    assert "Missing fields" in response.json["error"]


def test_register_user_invalid_email(client):
    """
    Test registration with an invalid email format.
    """
    data = {
        "email": "invalidemail.com",  # Invalid email
        "password": "password123",
        "name": "Invalid Email User",
        "role": "User",
    }
    response = client.post("/register", json=data)
    assert response.status_code == 400
    assert "Invalid email format" in response.json["error"]


def test_register_user_weak_password(client):
    """
    Test registration with a weak password.
    """
    data = {
        "email": "weakpassword@example.com",
        "password": "pass",  # Weak password
        "name": "Weak Password User",
        "role": "User",
    }
    response = client.post("/register", json=data)
    assert response.status_code == 400
    assert "Password must be at least 8 characters long" in response.json["error"]


def test_login_success(client):
    """
    Test successful user login.
    """
    data = {
        "email": "loginuser@example.com",
        "password": "Password123",
        "name": "Login User",
        "role": "User",
    }
    # Register the user first
    client.post("/register", json=data)

    # Test login
    response = client.post(
        "/login", json={"email": "loginuser@example.com", "password": "Password123"}
    )
    assert response.status_code == 200
    assert "token" in response.json


def test_login_failure(client):
    """
    Test login failure with invalid credentials.
    """
    response = client.post(
        "/login", json={"email": "invaliduser@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json["error"] == "Invalid credentials"


def test_profile_unauthorized(client):
    """
    Test accessing profile without authentication.
    """
    response = client.get("/profile")
    assert response.status_code == 401


def test_profile_authorized(client):
    """
    Test accessing profile with authentication.
    """
    data = {
        "email": "profileuser@example.com",
        "password": "Password123",
        "name": "Profile User",
        "role": "User",
    }
    # Register and login the user
    client.post("/register", json=data)
    login_response = client.post(
        "/login", json={"email": "profileuser@example.com", "password": "Password123"}
    )
    token = login_response.json.get("token")

    # Access the profile with the token
    response = client.get("/profile", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json["email"] == "profileuser@example.com"
    assert response.json["role"] == "User"
