# Geo-tourism project based on OSM and Leaflet
Allows you to view points of interest on the map.
Registered user can add their places. Write stories to places on the map and add photos, leave comments.
The parser robot looks for interesting places in open sources, and users can leave their story to this place.
The project is based on Open Stream Map and Leaflet. The data is stored in Postgres using GDAL.

## Technology:

- Python 3.9
- JS
- Django 4.0.2
- Postgresql 13
- Postgis
- GDAL
- libgeoip
- Bootstrap


# :TODO

 - debug

 - [x] Template
 - [x] Marker list
 - [x] Marker detail
 - [x] Registration
 - [x] Stories
 - [] Photos
 - [] Comments

 - [] Social auth
 - [] About
 - [] Search
 - [] Categories

 - [] Hosting

 - [] OSM mainer
 - [] Photo mainer



## Install

- Install and activate virtual environment
- Install requirements from requirements.txt
```
pip install -r requirements.txt
``` 
-Instal postgres
-Install GDAL
-Create by postgres admin:
```
create role mymap;
create database mymap owner mymap;
alter role mymap with encrypted password '';
alter role mymap with login ;
```

- Then make  manage.py in project folder:
```
python3 manage.py migrate
```

### Author:

Pavel Koshelev