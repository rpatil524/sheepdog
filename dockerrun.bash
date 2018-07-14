#!/bin/bash

cd /var/www/sheepdog

/usr/local/bin/gunicorn wsgi:app -w 4 -b 127.0.0.1:5000 --log-level=debug --chdir=/var/www/sheepdog --pythonpath "-pythonpath = /var/www/sheepdog/,/sheepdog/,/usr/local/lib/python2.7/dist-packages/" &
nginx -g 'daemon off;'
