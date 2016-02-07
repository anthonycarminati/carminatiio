#!/bin/bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
