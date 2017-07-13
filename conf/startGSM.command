#!/bin/bash
# Command to launch the Texting Centre Server

cd ~/SITES/texting/ && gunicorn wsgi:application -p /tmp/texting.pid -b texting.centre:8888
# to restart: kill -HUP `cat /tmp/texting.pid`
# dev server: cd ~/SITES/texting/ && ./manage.py runserver 8888

# On OS X, one can start Texting Centre at login by adding this file to login items.
# System Preferences > Users & Groups > [Current User] > Login Items > [+] > Find this file > Add
