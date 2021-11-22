<h1>pg_expoter - Postgres Prometheus metrics exporter</h1>
This project help's us to share Postgres metrics for Prometheus.

## Install
```bash
pip3 install flask psycopg2 
```

## Config
Set the values according to your database.
```config
[PSQL]
PSQL_HOST=192.168.0.1
PSQL_PORT=5432
PSQL_USER=postgres
PSQL_PASS=password
```