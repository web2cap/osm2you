# OSM Mainer
Python application that parses OpenStreetMap data for searching hiking places, uses PostgreSQL as the database, and can be containerized with Docker. We'll also integrate Celery for task management.

## Project File Structure
osmmainer/
|-- app/
|   |-- models.py
|   |-- parser.py
|   |-- search.py
|-- tests/
|   |-- test_parser.py
|-- config/
|   |-- config.py
|-- celery_worker.py
|-- Dockerfile
|-- pyproject.toml
|-- run.py
