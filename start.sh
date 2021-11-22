#!/bin/bash
APP_DIR="/opt/pg_exporter"
cd $APP_DIR
export L LC_ALL=en_US
export FLASK_APP=api
flask run --host 0.0.0.0 -p 9432