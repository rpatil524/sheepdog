#!/bin/bash

cd /var/www/sheepdog
export PYTHONUNBUFFERED=TRUE
/usr/local/bin/gunicorn wsgi:app -w 4 -b 127.0.0.1:5000 --log-level=info --chdir=/var/www/sheepdog --pythonpath "/var/www/sheepdog/,/sheepdog/,/usr/local/lib/python2.7/dist-packages/" &
nginx -g 'daemon off;'
