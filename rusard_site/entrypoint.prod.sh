#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"
#!/bin/sh
set -e

echo "📡 Attente de la base de données..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "⏳ PostgreSQL n'est pas prêt - attente..."
  sleep 1
done

echo "✅ Base de données prête !"

echo "🔧 Lancement des migrations..."
python manage.py migrate --noinput

echo "🎯 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🚀 Lancement de Gunicorn"
exec gunicorn rusard_site.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120