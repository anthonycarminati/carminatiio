#!/usr/bin/env bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all

sudo /etc/init.d/nginx restart
