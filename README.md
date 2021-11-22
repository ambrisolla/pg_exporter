<h1>pg_expoter - Postgres Prometheus metrics exporter</h1>
This project help's us to share Postgres metrics for Prometheus.

## Install
```bash
pip3 install flask psycopg2 
```

## Config
Set the values according to your database:
```bash
[PSQL]
PSQL_HOST=192.168.0.1
PSQL_PORT=5432
PSQL_USER=postgres
PSQL_PASS=password
```
</br>

Change the APP_DIR variable according to your configuration:
```bash
#!/bin/bash
APP_DIR="/opt/pg_exporter"
cd $APP_DIR
export L LC_ALL=en_US
export FLASK_APP=api
flask run --host 0.0.0.0 -p 9432
```
## Run
```bash
sh start.sh
```

## Test
```bash
curl http://[IP]:9432/metrics
```