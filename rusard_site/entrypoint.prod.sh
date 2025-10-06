#!/bin/sh
set -e

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
        printf '.'
        sleep 1
    done
    echo "\nPostgreSQL is ready."
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
