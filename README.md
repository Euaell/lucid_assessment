# FastAPI Blog Application

A web application following the MVC design pattern, built with FastAPI, SQLAlchemy, and MySQL.

## Features

- User authentication with JWT tokens
- CRUD operations for blog posts
- Request validation with Pydantic schemas
- Response caching for improved performance
- Database access via SQLAlchemy ORM
- Containerized with Docker and Docker Compose

## Project Structure

The project follows the MVC (Model-View-Controller) design pattern:

- **Models**: SQLAlchemy models for database entities (`app/models/`)
- **Views**: Pydantic schemas for request/response validation (`app/schemas/`)
- **Controllers**: API route handlers (`app/api/routes/`)

Additional components:

- **Repositories**: Data access layer for database operations (`app/repositories/`)
- **Services**: Business logic layer (`app/services/`)
- **Core**: Configuration, database setup, security utilities (`app/core/`)
- **Dependencies**: FastAPI dependencies for request validation, auth, etc. (`app/api/dependencies/`)

## Requirements

- Docker and Docker Compose
- Python 3.12+ (for development without Docker)
- MySQL (for development without Docker)

## Getting Started

### Running with Docker (Recommended)

1. Clone the repository
2. Build and start the containers:

```bash
make build
make up
```

3. Apply database migrations:

```bash
make migrate
```

4. Access the API at http://localhost:8000
5. View the API documentation at http://localhost:8000/docs

### Running without Docker

1. Clone the repository
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up a MySQL database and update the connection string in `app/core/config.py`
5. Run the application:

```bash
python start.py
# or
uvicorn app.main:app --reload
```

6. Apply database migrations:

```bash
alembic upgrade head
```

## Testing the API

A simple test script is provided to verify that the API is working correctly. After starting the application, run:

```bash
# Install requests first if not already installed
pip install requests

# Run the test script
python test_api.py
```

The script will test the following endpoints:
- Root endpoint (GET /)
- Signup endpoint (POST /api/signup)
- Add post endpoint (POST /api/posts)
- Get posts endpoint (GET /api/posts)
- Delete post endpoint (DELETE /api/posts)

## API Endpoints

### Authentication

- `POST /api/signup`: Register a new user
  - Request: `{ "email": "user@example.com", "password": "strongpassword" }`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`

- `POST /api/login`: Log in an existing user
  - Request: `{ "email": "user@example.com", "password": "strongpassword" }`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`

### Posts

- `POST /api/posts`: Create a new post
  - Auth: Bearer token required
  - Request: `{ "text": "Post content" }`
  - Response: `{ "post_id": 1 }`

- `GET /api/posts`: Get all posts for the authenticated user
  - Auth: Bearer token required
  - Response: `[{ "id": 1, "text": "Post content", "user_id": 1, "created_at": "..." }, ...]`

- `DELETE /api/posts`: Delete a post
  - Auth: Bearer token required
  - Request: `{ "post_id": 1 }`
  - Response: `{ "message": "Post deleted successfully" }`

## Development Commands

The Makefile provides several commands to help with development:

- `make build`: Build the Docker containers
- `make up`: Start the Docker containers in detached mode
- `make down`: Stop the Docker containers
- `make logs`: View the logs from the Docker containers
- `make shell`: Open a shell in the app container
- `make db-shell`: Open a MySQL shell for the database
- `make migrate`: Apply database migrations

## License

This project is licensed under the MIT License. 