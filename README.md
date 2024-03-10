# OSM2YOU id geo-tourism project with OSM and Leaflet

## Website [osm.w2c.net.eu.org](https://osm.w2c.net.eu.org/)

Explore points of interest on the map and share your own stories about unique locations with this geo-tourism project.
Users can register, add their favorite places, and contribute personal narratives to create a community-driven map of interesting spots.
The project leverages OpenStreetMap (OSM) for mapping and Leaflet for a dynamic user interface.
Data is stored in Postgres with the help of GDAL.

[![GitHub Actions](https://github.com/web2cap/osm2you/actions/workflows/main_backend.yml/badge.svg)](https://github.com/web2cap/osm2you/actions/workflows/main_backend.yml)

## Technology Stack:

### Backend:
- Python 3.10
- Django 4
- GeoDjango: Django module for developing geographic web applications.
- Djoser: Django package for handling authentication endpoints.
- Postgresql
- Postgis: Geographic Information System (GIS) extension for PostgreSQL.
- GDAL: Geospatial Data Abstraction Library for reading and writing raster and vector geospatial data formats.
- Celery: Distributed task queue used for background processing.
- Pytest: App tests in /tests dir

### Frontend:
- React
- Redux
- Axios

### Deployment:
- Docker
- Docker Compose
- NGINX

## Installation:

1. Clone the repository:
   ```
   git clone git@github.com:web2cap/osm2you.git
   ```
2. Create a .env file in the osm2you/infra directory, following this example:
    ```
    ST_SECRET_KEY="**************************************************"

    POSTGRES_USER="postgres"
    POSTGRES_DB="postgres"
    POSTGRES_PASSWORD="changeme"

    DB_NAME="osm2you"
    DB_USER="osm"
    DB_PASSWORD="osm_db_pass"
    DB_HOST="osm_db"
    DB_PORT=5432
    DB_TEST_NAME="test_osm2you"

    REDIS_INDEX=0
    REDIS_USER="redis"
    REDIS_HOST="osm_redis"
    REDIS_PORT=6379
    ```
3. Run Docker Compose to set up the environment:
    ```bash
    cd osm2you/infra
    docker-compose up
    ```

## Celery Tasks and Marker Clustering:
The project utilizes Celery for asynchronous task execution and includes functionality for clustering markers. Here's an overview of the tasks and clustering process:

### Celery Tasks:
 - run_clustermarkers: Task to update marker clusters based on marker locations.
 - run_scrap_markers_main: Task to scrape main marker data from OSM.
 - run_scrap_markers_related: Task to scrape related marker data based on a marker ID.
 - run_scrap_markers_batch_related: Task to scrape related marker data in batches.
 - Marker Clustering:

### The project implements server-side clustering for markers using geographic coordinates. The clustering process involves:
 - Calculating marker clusters based on specified square sizes.
 - Storing temporary marker clusters.
 - Moving clusters from temporary storage to production.
 - Automatic Data Retrieval and Clustering:

### After deployment, the project automatically performs the following tasks:
 - Scraping Main Markers: The system loads all camp sites from OSM using the run_scrap_markers_main task.
 - Clustering: Clustering of markers is initiated to group nearby markers together.
 - Scraping Related Markers: The run_scrap_markers_batch_related task is started to add related markers for all added main markers.
These tasks are scheduled to run periodically to search for new markers from OSM and keep the map updated with the latest information.

## API Endpoints:

- **Main Page:** `/api/v1/`

### Authentication:
- Obtain JWT token: `api/v1/auth/jwt/create/`
- Refresh JWT token: `api/v1/auth/jwt/refresh/`
- Verify JWT token: `api/v1/auth/jwt/verify/`
- Create user: `api/v1/auth/users/`
- Reset password: `api/v1/auth/users/reset_password/`
- Confirm reset password: `api/v1/auth/users/reset_password_confirm/`
- Set password: `api/v1/auth/users/set_password/`
- Retrieve or update current user: `api/v1/auth/users/me/`

### Markers:
- List all markers: `api/v1/markers/`
- User-specific markers: `api/v1/markers/user/{username}/`
- Get, retrieve, update, or delete marker: `api/v1/markers/{id}/`

### Stories:
- Story details by ID: `api/v1/stories/(pk)/` 

### Tags:
- List all tags: `api/v1/tags/`

### Kinds:
- List all kinds: `api/v1/kinds/`

### Documentation:
- Swagger UI: `api/v1/docs/`
- ReDoc: `api/v1/redoc/`



Feel free to contribute, report issues, or share your own geo-tourism stories with the community!

Terms of Service: [BSD License](https://github.com/web2cap/osm2you/blob/main/LICENSE)


