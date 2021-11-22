<h1>pg_expoter - Postgres Prometheus metrics exporter</h1>
This project will help you share Postgres metrics for Prometheus.

## Install
```bash
$ pip3 install flask psycopg2 
$ git clone https://github.com/andrebrisolla/pg_exporter.git /opt/pg_exporter
$ cd /opt/pg_exporter
```


Change the APP_DIR variable according to your configuration:
```bash
#!/bin/bash
APP_DIR="/opt/pg_exporter"
cd $APP_DIR
export L LC_ALL=en_US
export FLASK_APP=api
flask run --host 0.0.0.0 -p 9432
```
## Start exporter
```bash
$ sh start.sh
```

## Create a Systemd Service

Copy the pg_exporter.service file to /etc/systemd/system/pg_exporter.service.
```bash
$ cp pg_exporter.service /etc/systemd/system/pg_exporter.service
```
 Reload systemd daemon
```bash
$ systemctl daemon-reload
```
Start service
```bash
$ systemctl start pg_exporter
```
## Test
```bash
curl http://[IP]:9432/metrics
```