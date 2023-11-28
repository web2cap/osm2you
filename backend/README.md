# Backend server osm2you on Django 4, DRF.

## Local Instalation

```
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install poetry

poetry install

poetry run python manage.py migrate  
poetry run python manage.py runserver
```