web: gunicorn -w 3 --log-file - server_side.wsgi
worker: python manage.py rqworker high default low