import pytest
from flask import json
from flask_jwt_extended import create_access_token
from auth_service.app import app  # Ensure this points to your auth_service app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_admin_access(client):
    """Test access for Admin role"""
    # Create an access token for an Admin
    with app.app_context():
        access_token = create_access_token(
            identity='admin_user', 
            additional_claims={'role': 'Admin'}
        )
    
    # Make request with Admin token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/auth', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Authorized Admin" in data['message']

def test_user_access(client):
    """Test access for User role"""
    # Create an access token for a regular User
    with app.app_context():
        access_token = create_access_token(
            identity='regular_user', 
            additional_claims={'role': 'User'}
        )
    
    # Make request with User token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/auth', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Error: Administrator" in data['message']

# def test_missing_token(client):
#     """Test access without providing a token"""
#     response = client.get('/auth')
    
#     assert response.status_code == 401
#     data = json.loads(response.data)
#     assert data['error'] == 'Missing or invalid JWT token.'

def test_missing_token(client):
    """Test access without providing a token"""
    response = client.get('/auth')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    # Flask-JWT-Extended returns 'msg' instead of 'error'
    assert 'msg' in data
    assert "Missing Authorization Header" in data['msg']

# def test_invalid_token(client):
#     """Test access with an invalid token"""
#     headers = {'Authorization': 'Bearer invalid_token'}
#     response = client.get('/auth', headers=headers)
    
#     assert response.status_code == 422
#     data = json.loads(response.data)
#     assert 'error' in data
#     assert "Invalid token format or signature." in data['error']


def test_invalid_token(client):
    """Test access with an invalid token"""
    headers = {'Authorization': 'Bearer invalid_token'}
    response = client.get('/auth', headers=headers)
    
    assert response.status_code == 422
    data = json.loads(response.data)
    # Flask-JWT-Extended returns 'msg' instead of 'error'
    assert 'msg' in data
    assert "Not enough segments" in data['msg']

def test_unknown_role(client):
    """Test access with an unknown role"""
    # Create an access token with an unknown role
    with app.app_context():
        access_token = create_access_token(
            identity='unknown_user', 
            additional_claims={'role': 'Unknown'}
        )
    
    # Make request with unknown role token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/auth', headers=headers)
    
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['error'] == 'Role not recognized'

# Additional configuration for running tests
if __name__ == '__main__':
    pytest.main([__file__])