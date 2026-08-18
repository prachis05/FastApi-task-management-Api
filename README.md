# FastAPI Task Management API

A modular Task Management REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite**. The API provides complete CRUD functionality for tasks, task completion, request validation with Pydantic, structured error handling, and automatic Swagger/OpenAPI documentation.

## Features

- Create new tasks
- View all tasks
- View a task by ID
- Update existing tasks
- Mark tasks as completed
- Delete tasks
- SQLite database persistence
- SQLAlchemy ORM
- Pydantic request/response validation
- HTTP status codes and meaningful error messages
- Environment variable configuration
- Swagger/OpenAPI documentation
- Modular application structure using routers, models, schemas, and services

## Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Uvicorn**
- **python-dotenv**

## Project Structure

```text
fastapi-task-management-api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py
│   │
│   └── services/
│       ├── __init__.py
│       └── task_services.py
│
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks` | Get all tasks |
| `GET` | `/tasks/{task_id}` | Get a task by ID |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |
| `PATCH` | `/tasks/{task_id}/complete` | Mark a task as completed |

## Task Fields

Each task contains:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Build a Task Management API",
  "status": false,
  "created_at": "2026-08-18T10:30:00"
}
```

- `id` — unique task identifier
- `title` — task title
- `description` — task description
- `status` — completion status (`true`/`false`)
- `created_at` — date and time when the task was created

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi-task-management-api.git
cd fastapi-task-management-api
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install fastapi uvicorn sqlalchemy python-dotenv
```

## Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./example.db
```

A `.env.example` file is included as a template:

```env
DATABASE_URL=
```

Do not commit your actual `.env` file to GitHub.

## Running the Application

From the project root, run:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

You can use Swagger UI to test all endpoints without needing a separate API client.

## Example Requests

### Create a Task

**POST** `/tasks`

Request body:

```json
{
  "title": "Learn FastAPI",
  "description": "Study FastAPI CRUD operations"
}
```

Successful response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Study FastAPI CRUD operations",
  "status": false,
  "created_at": "2026-08-18T10:30:00"
}
```

Status code:

```text
201 Created
```

### Get All Tasks

**GET** `/tasks`

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "description": "Study FastAPI CRUD operations",
    "status": false,
    "created_at": "2026-08-18T10:30:00"
  }
]
```

### Get a Task by ID

**GET** `/tasks/1`

If the task exists, its details are returned.

If it does not exist:

```json
{
  "detail": "Task not found"
}
```

Status code:

```text
404 Not Found
```

### Update a Task

**PUT** `/tasks/1`

Request body:

```json
{
  "title": "Learn FastAPI and SQLAlchemy",
  "description": "Complete CRUD and database integration",
  "status": false
}
```

### Complete a Task

**PATCH** `/tasks/1/complete`

This changes the task's status to:

```json
{
  "status": true
}
```

### Delete a Task

**DELETE** `/tasks/1`

A successfully deleted task returns:

```text
204 No Content
```

## Database

The project uses **SQLite** for persistent storage.

The database URL is configured through the `DATABASE_URL` environment variable:

```env
DATABASE_URL=sqlite:///./app.db
```

SQLAlchemy manages the database connection and ORM models, while SQLite stores the task data in the `app.db` file.

## Error Handling

The API returns appropriate HTTP status codes for common situations:

| Status Code | Meaning |
|---|---|
| `200` | Request successful |
| `201` | Resource created successfully |
| `204` | Resource deleted successfully |
| `404` | Task not found |
| `422` | Request validation failed |
| `500` | Internal server error |

Example error response:

```json
{
  "detail": "Task not found"
}
```

## Architecture

The application follows a modular structure:

```text
Client
   ↓
FastAPI Router
   ↓
Pydantic Schema
   ↓
Service Layer
   ↓
SQLAlchemy Model
   ↓
SQLite Database
```

### Responsibilities

**Routers**  
Handle HTTP requests and responses.

**Schemas**  
Validate request data and define response formats.

**Services**  
Contain task-related business and database logic.

**Models**  
Define SQLAlchemy database tables.

**Database**  
Manage the SQLite connection and SQLAlchemy sessions.

## Testing

All endpoints can be tested through Swagger UI:

```text
http://127.0.0.1:8000/docs
```

You can also test the API using tools such as Postman.

## Future Improvements

Possible future enhancements include:

- User authentication and authorization
- JWT-based authentication
- Pagination and filtering
- Task priorities and deadlines
- Search functionality
- PostgreSQL support
- Automated tests with Pytest
- Docker deployment
- Alembic database migrations

## Author

**Ahmed Amir**

Built as a FastAPI backend project for learning and practicing REST API development, database integration, and modular application architecture.
