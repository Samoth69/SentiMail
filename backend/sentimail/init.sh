#!/bin/sh
python manage.py migrate --noinput
python manage.py create_services_users