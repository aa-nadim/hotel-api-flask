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