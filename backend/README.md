# Backend server osm2you on Django 4, DRF.

## Local Instalation
- Install and activate virtual environment
- Instal postgres
- Install GDAL
- Create by postgres admin:

```
create role DB_USER with login;
create database DB_NAME owner DB_USER;
alter role DB_USER with encrypted password 'DB_PASSWORD';
```

- Create a .env file in the backend directory, following this example:
```
    ST_DEBUG="True"
    ST_SECRET_KEY="**************************************************"

    DB_NAME="osm2you"
    DB_USER="osm"
    DB_PASSWORD="osm_db_pass"
    DB_HOST="osm_db"
    DB_PORT=5432
    DB_TEST_NAME="test_osm2you"
```

- Install requirements:

```
cd backend
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install poetry

poetry install
```

- Then make  manage.py in project folder:
```
poetry run python manage.py migrate  
poetry run python manage.py collectstatic
poetry run python manage.py runserver
```
- Create superuser (optional)
```
poetry run python manage.py createsuperuser  
```