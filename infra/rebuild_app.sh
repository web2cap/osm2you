docker-compose down
docker image rm infra_osm_celery_worker
docker image rm infra_osm_celery_beat
docker image rm infra_osm_back
docker image rm infra_osm_flower
docker-compose up            