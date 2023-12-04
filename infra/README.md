# TODO
### Create DB

create role osm with login;
alter role osm with encrypted password 'osm_db_pass';
create database osm2you owner osm;
\c osm2you 
create extension postgis;

### Init backend
python manage.py migrate