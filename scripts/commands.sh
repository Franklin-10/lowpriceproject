#!/bin/sh
set -e

/scripts/wait_psql.sh

COMMAND="$1"

chown -R duser:duser /data/web

if [ "$COMMAND" = "web" ]; then
    gosu duser python manage.py migrate
    gosu duser python manage.py collectstatic --no-input

    exec gosu duser /scripts/runserver.sh

elif [ "$COMMAND" = "worker" ]; then
    exec gosu duser /scripts/run_celery.sh
fi