# Geo-tourism Project with OSM and Leaflet

Explore points of interest on the map and share your own stories about unique locations with this geo-tourism project.
Users can register, add their favorite places, and contribute personal narratives to create a community-driven map of interesting spots.
The project leverages OpenStreetMap (OSM) for mapping and Leaflet for a dynamic user interface.
Data is stored in Postgres with the help of GDAL.

## Technology Stack:

### Backend:
- Python 3.10
- Django 4
- GeoDjango: Django module for developing geographic web applications.
- Djoser: Django package for handling authentication endpoints.
- Postgresql
- Postgis: Geographic Information System (GIS) extension for PostgreSQL.
- GDAL: Geospatial Data Abstraction Library for reading and writing raster and vector geospatial data formats.
- Pytest: App tests in /tests dir

### Frontend:
- React
- Redux
- Axios

### Deployment:
- Docker
- Docker Compose
- NGINX




## Installation:

1. Clone the repository:
   ```bash
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

## API Endpoints:

- **Main Page:** `/`

### Markers:
- List all markers: `api/v1/markers/`
- User-specific markers: `api/v1/markers/user/(username)/`
- Marker by ID: `api/v1/markers/(pk)/`

### Stories:
- Story details by ID: `api/v1/stories/(pk)/` 

### Authentication:
- Authentication: `api/v1/auth/` Djoser endpoints

### Documentation:
- Swagger UI: `api/v1/docs/`
- ReDoc: `api/v1/redoc/`

### Admin Panel:
- Admin Panel: `admin/`


Feel free to contribute, report issues, or share your own geo-tourism stories with the community!


