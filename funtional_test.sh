#!/usr/bin/bash

echo "Starting MongoDB container..."
docker-compose -f docker-compose-dev.yaml up -d

echo "Setting environment variables..."
source ./env

echo "Run server..."
flask run &

echo "Run tests in functional mode..."
pytest --functional

echo "Stop server..."
kill %1

echo "Stopping MongoDB container..."
docker-compose -f docker-compose-dev.yaml down
