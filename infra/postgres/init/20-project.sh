#!/bin/bash

set -e


# Check required environment variables
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
    echo "Error: DB_NAME, DB_USER, and DB_PASSWORD must be set in the environment."
    exit 1
fi

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

# Create user, database, and set search_path
psql <<- EOSQL
CREATE ROLE $DB_USER WITH LOGIN;
ALTER ROLE $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET search_path = 'public';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
\c $DB_NAME
CREATE EXTENSION postgis;
EOSQL