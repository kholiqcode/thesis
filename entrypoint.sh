#!/bin/sh
if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."
    
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    
    echo "Mysql started"
fi

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec "$@"
