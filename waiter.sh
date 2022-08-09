#!/bin/sh


echo "Waiting for Redis db..."

while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done

echo "Redis db started"


echo "Waiting for Postgres db..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "Postgres db started"


exec "$@"
