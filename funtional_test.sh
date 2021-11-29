#!/usr/bin/bash

echo "Setting JWT secret environment variable..."
source env

echo "Run server..."
discounterland &

echo "Run tests in functional mode..."
pytest --functional
