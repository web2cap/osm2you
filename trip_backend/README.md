# **Trip Backend**

## **Overview**
`trip_backend` is a FastAPI-based microservice responsible for managing trips. It provides CRUD operations for trips, user authentication, and integrates with the main backend for user and marker data.

## **Features**
- **Trip Management**
  - Create, update, retrieve, and delete trips.
  - Validate trip dates and ownership.
- **Database & Migrations**
  - Uses PostgreSQL as the database.
  - Alembic for database migrations.
- **Authentication**
  - JWT-based authentication.
- **Testing**
  - `pytest-asyncio` for asynchronous tests.
  - Database fixtures for test isolation.
- **Versioned API**
  - All endpoints are accessible under `/v1/`.

---

## **Project Structure**
```
trip_backend/
├── app/
│   ├── api/ (API routes)
│   ├── core/ (Config, DB, dependencies)
│   ├── models/ (SQLAlchemy models)
│   ├── repository/ (Data access logic)
│   ├── schema/ (Pydantic schemas)
│   ├── services/ (Business logic)
│   ├── utils/ (Helper functions)
│   ├── main.py (FastAPI entry point)
├── migrations/ (Alembic migration files)
├── tests/ (Test suite)
│   ├── fixtures/ (Database test fixtures)
│   ├── integration/ (Integration tests)
├── poetry.lock
├── pyproject.toml
└── README.md
tests/
└── trip_backend
    ├── conftest.py
    ├── fixtures/ (Test fixtures)
    ├── integration (Integration tests)
```

---

## **Installation & Setup**

### **1. Install Dependencies**
Ensure you have [Poetry](https://python-poetry.org/) installed, then run:
```sh
cd trip_backend
poetry install
```

### **2. Configure Environment Variables**
Create a `.env` file in `trip_backend/` (or update existing one) with:
```ini
MODE="DEV"

ST_SECRET_KEY="your-secret-key"
ST_DEBUG="True"
ST_DEBUG_SQL="True"

POSTGRES_USER="postgres"
POSTGRES_DB="postgres"
POSTGRES_PASSWORD="changeme"

DB_NAME="osm2you"
DB_USER="osm2you"
DB_PASSWORD="osm_db_pass"
DB_HOST="localhost"
DB_PORT=5432
DB_TEST_NAME="test_osm2you"

REDIS_INDEX=0
REDIS_USER="redis"
REDIS_HOST="localhost"
REDIS_PORT=6379
```

### **3. Initialize the Database**
Before running the `trip_backend`, ensure the **main backend** is running and has initialized the **users and markers** tables.

Then, apply database migrations:
```sh
poetry run alembic upgrade head
```

---

## **Running the Application**
Start the FastAPI server with:
```sh
poetry run uvicorn app.main:app --reload
```
By default, it runs on `http://127.0.0.1:8000/v1`.

---

## **Running Tests**
To execute the test suite, run:
```sh
poetry run pytest ../tests/trip_backend/
```
Ensure that the **main backend database** is running before running tests.

---

## **API Endpoints**
The API documentation is available at:
- **Swagger UI**: [http://127.0.0.1:8000/v1/docs](http://127.0.0.1:8000/v1/docs)
- **Redoc**: [http://127.0.0.1:8000/v1/redoc](http://127.0.0.1:8000/v1/redoc)

### **Trips API** (`/v1/trip/`)
- **Create Trip** (POST `/trip/`)
  - Requires authentication
  - Body: `{ start_date, end_date, marker_id, description, user_id }`
  - Returns: Created trip details

- **Get Trip** (GET `/trip/{trip_id}`)
  - Returns details of a trip by `trip_id`

- **Update Trip Dates** (PUT `/trip/{trip_id}`)
  - Requires authentication
  - Body: `{ start_date, end_date }`
  - Returns: Updated trip details

- **Delete Trip** (DELETE `/trip/{trip_id}`)
  - Requires authentication
  - Deletes a trip by `trip_id`

### **Additional Features**
- **My Trips** (GET `/trip/my-trips/`)
  - Returns trips owned by the authenticated user

- **Join Trip** (POST `/trip/join/{trip_id}`)
  - Allows another user to join an existing trip

- **Trips in Map Area** (GET `/trip/in_bbox/`)
  - Returns trips within a given map bounding box

---

## **Future Enhancements**
- **Advanced filtering for trips**
- **Join trip by other users**
- **User's own trip listing**
- **Trips within a specified map bounding box**
- **Deploy on AWS Lambda**
