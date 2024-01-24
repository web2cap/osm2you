#!/bin/bash

set -o errexit
set -o nounset

poetry add flower

worker_ready() {
    celery -A osm2you inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

celery -A osm2you  \
    --broker="${REDIS_USER}://${REDIS_HOST}:${REDIS_PORT}/${REDIS_INDEX}" \
    flower