#!/usr/bin/env sh
if [ "$POSTGRES_DB" = "auth" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi


gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
