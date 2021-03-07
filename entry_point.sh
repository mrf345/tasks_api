#!/bin/sh
echo "Await database launch..."
while ! nc -z database $DATABASE_PORT; do sleep 0.1; done

echo "Database is ready"
./manage.py migrate
celery --app tasks_api worker -l info &

echo "Should be running: http://0.0.0.0:$PORT"
./manage.py runserver 0.0.0.0:$PORT
