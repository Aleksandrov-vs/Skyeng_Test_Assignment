#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

chown www-data:www-data /var/log
chown -R www-data:www-data /opt/app/media/

exec "$@"