#!/usr/bin/env bash
<<<<<<< HEAD
set -o errexit

=======
>>>>>>> 5e61d040c93c8fd29e640e66b43e688eceb59f60
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
