#!/bin/bash -xe

gunicorn -c /usr/src/app/gunicorn/conf.py ui.wsgi --log-file - -b [::1]:8000 -b 0.0.0.0:8000

