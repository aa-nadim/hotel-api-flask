# Travel API with Microservices 

This project provides a set of microservices related to hotel management, built using Flask, with services for user management, destination management, and authentication. The services are containerized using Docker for easy deployment and scalability.

## Installation

### Clone the Repository
  ```bash
  git clone https://github.com/aa-nadim/hotel-api-flask.git
  cd hotel-api-flask
  ```
### For **Linux**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
### If you use **Docker**
```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  deactivate
  ```

### For **Windows**
  ```bash
  python -m venv .venv
  source .venv/Scripts/activate
  pip install -r requirements.txt
  deactivate
  ```

## Docker Setup Instructions

### **Pre-requisites**
1. **Docker**: Ensure that Docker and Docker Compose are installed on your machine.
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

### **Build the Docker Images**

To build the Docker images for all services and start the containers, run:

```bash
  sudo docker-compose up -d --build
  docker-compose down
```

## Running the Services (Not Aplicable for Docker)

### **User Service**
Run the user service on port 5001:
  ```bash
  python user_service/app.py
  ```
### **Destination Service**
Run the destination service on port 5002:
  ```bash
  python destination_service/app.py
  ```
### **Auth Service**
Run the authentication service on port 5003:
  ```bash
  python auth_service/app.py
  ```

## Services Overview (Access the Swagger UI)
1. **User Service**:
   - Run on: [http://127.0.0.1:5001/apidocs/](http://127.0.0.1:5001/apidocs/)

2. **Destination Service**:
   - Run on: [http://127.0.0.1:5002/apidocs/](http://127.0.0.1:5002/apidocs/)

3. **Auth Service**:
   - Run on: [http://127.0.0.1:5003/apidocs/](http://127.0.0.1:5003/apidocs/)

Use Swagger UI to test the endpoints, review request/response formats, and explore available features.


## Running Tests
Run the unit tests for each service individually:

### User Service
  ```bash
  pytest user_service/__tests__/test_user_service.py
  pytest user_service --cov=.
  ```

### Destination Service
  ```bash
  pytest destination_service/__tests__/test_destination_service.py
  pytest destination_service --cov=.
  ```

### Auth Service
  ```bash
  pytest auth_service/__tests__/test_auth_service.py
  pytest auth_service --cov=.
  ```

### Run All Tests with Coverage
To run all tests and check the combined coverage:
  ```bash
  pytest --cov=user_service --cov=destination_service --cov=auth_service --cov-report=term --cov-report=html
  ```
  Open the generated `htmlcov/index.html` for detailed coverage reports.


## API Endpoints

### **User Service Endpoints**

#### **1. Register a New User**
- **URL**: `/register`
- **Method**: `POST`
- **Description**: Register a new user with the required details.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "Password123",
    "name": "John Doe",
    "role": "User"
  }
- **Responses:**
  - `201`: User registered successfully
  - `400`: Missing fields or invalid input


#### **2. User Login**
- **URL**: `/login`
- **Method**: `POST`
- **Description**: Authenticate a user and provide an access token.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "Password123"
  }
- **Responses:**
  - `200`: Login successful with JWT token
  - `400`: Missing email or password
  - `401`: Invalid credentials


#### **3. View User Profile**
- **URL**: `/profile`
- **Method**: `GET`
- **Description**: View the profile of the logged-in user.
- **Authentication**: JWT token is required (Authorization header with "Bearer {token}").
- **Responses:**
  - `200`: User profile data (email, role)
  - `401`: Unauthorized (no token provided)


### **Destination Service Endpoints**

#### **1. Add a New Destination**
- **URL**: `/addDestinations`
- **Method**: `POST`
- **Description**: Add a new destination (Admin only).
- **Authentication**: JWT token required (Admin role).
- **Request Body**:
  ```json
  {
    "name": "Bali",
    "description": "A tropical paradise",
    "location": "Indonesia",
    "price_per_night": 200.5
  }
- **Responses:**
  - `201`: Destination added successfully
  - `401`: Unauthorized (Admin access required)
  - `400`: Missing fields or invalid data


#### **2. Get All Destinations**
- **URL**: `/destinations`
- **Method**: `GET`
- **Description**: Retrieve a list of all destinations.
- **Responses:**
  - `200`: List of all destinations


#### **3. Delete a Destination**
- **URL**: `/destinations/<id>`
- **Method**: `DELETE`
- **Description**: Delete a destination by its ID (Admin only).
- **Authentication**: JWT token required (Admin role).
- **Parameters:**
  - `id`: Destination ID (string)
- **Responses:**
  - `200`: Destination deleted successfully
  - `401`: Unauthorized (Admin access required)
  - `404`: Destination not found


### **Auth Service Endpoints**

#### **1. Get Destinations with Role-based Access**
- **URL**: `/auth`
- **Method**: `GET`
- **Description**: Get access to destinations with role-based access.
- **Authentication**: JWT token required (Admin or User role).
- **Responses:**
  - `200`: Role-based message (for Admin and User roles)
  - `401`: Missing or invalid JWT token
  - `403`: Role not recognized or unauthorized



### **Error Responses**
  - `400`: Bad Request – Missing required fields or invalid input
  - `401`: Unauthorized – Token missing or invalid
  - `403`: Forbidden – Insufficient role privileges (Admin required)
  - `404`: Not Found – The requested resource was not found
  - `422`: Unprocessable Entity – Invalid token format or signature