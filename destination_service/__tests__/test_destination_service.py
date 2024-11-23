import pytest
import os
import shutil
import json
from flask_jwt_extended import create_access_token
from destination_service.app import app

DESTINATION_DATA_FILE = os.path.join(os.path.dirname(__file__), "../destination_data.py")
TEMP_DESTINATION_DATA_FILE = os.path.join(os.path.dirname(__file__), "../destination_data_backup.py")

@pytest.fixture
def client():
    """Set up the test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Backup and restore the destination data file.
    - Backup the original `destination_data.py`.
    - Create a temporary empty data file for testing.
    """
    # Backup the original data file
    if os.path.exists(DESTINATION_DATA_FILE):
        shutil.copy(DESTINATION_DATA_FILE, TEMP_DESTINATION_DATA_FILE)
    else:
        open(DESTINATION_DATA_FILE, "w").close()  # Ensure the file exists

    # Clear the destinations
    with open(DESTINATION_DATA_FILE, "w") as file:
        file.write("destinations = []")
    yield

    # Restore the original data file
    if os.path.exists(TEMP_DESTINATION_DATA_FILE):
        shutil.move(TEMP_DESTINATION_DATA_FILE, DESTINATION_DATA_FILE)

def test_add_destination_admin(client):
    """Test adding a new destination with Admin role."""
    with app.app_context():
        token = create_access_token(identity="admin_user", additional_claims={"role": "Admin"})

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Paris",
        "description": "The City of Light",
        "location": "France",
        "price_per_night": 150.0,
    }
    response = client.post("/addDestinations", json=data, headers=headers)

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["message"] == "Destination added successfully"
    assert response_data["destination"]["name"] == "Paris"

def test_add_destination_non_admin(client):
    """Test adding a destination with non-Admin role."""
    with app.app_context():
        token = create_access_token(identity="regular_user", additional_claims={"role": "User"})

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Tokyo",
        "description": "The Land of the Rising Sun",
        "location": "Japan",
        "price_per_night": 200.0,
    }
    response = client.post("/addDestinations", json=data, headers=headers)

    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data["error"] == "Admin access required"

def test_get_destinations(client):
    """Test retrieving all destinations."""
    response = client.get("/destinations")
    assert response.status_code == 200
    response_data = response.get_json()
    assert "destinations" in response_data
    assert isinstance(response_data["destinations"], list)

def test_delete_destination_admin(client):
    """Test deleting a destination with Admin role."""
    # First, add a destination
    with app.app_context():
        token = create_access_token(identity="admin_user", additional_claims={"role": "Admin"})

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "London",
        "description": "The Capital of England",
        "location": "UK",
        "price_per_night": 180.0,
    }
    add_response = client.post("/addDestinations", json=data, headers=headers)
    destination_id = add_response.get_json()["destination"]["id"]

    # Then, delete the destination
    delete_response = client.delete(f"/destinations/{destination_id}", headers=headers)
    assert delete_response.status_code == 200
    response_data = delete_response.get_json()
    assert response_data["message"] == "Destination deleted successfully"

def test_delete_destination_non_admin(client):
    """Test deleting a destination with non-Admin role."""
    # First, add a destination
    with app.app_context():
        admin_token = create_access_token(identity="admin_user", additional_claims={"role": "Admin"})
        user_token = create_access_token(identity="regular_user", additional_claims={"role": "User"})

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}
    data = {
        "name": "Berlin",
        "description": "The German Capital",
        "location": "Germany",
        "price_per_night": 100.0,
    }
    add_response = client.post("/addDestinations", json=data, headers=admin_headers)
    destination_id = add_response.get_json()["destination"]["id"]

    # Attempt to delete with a non-admin token
    delete_response = client.delete(f"/destinations/{destination_id}", headers=user_headers)
    assert delete_response.status_code == 401
    response_data = delete_response.get_json()
    assert response_data["error"] == "Admin access required"
