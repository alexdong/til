Grafana is a visualisation and alerting frontend that supports multiple backends, including Cloudwatch and InfluxDB. 

InfluxDB is a Time-series database with a SQL-like syntax.  influxDB itself doesn't have an UI. The query is done through `influx` command. Similar to
`mysql`. The influxdb server is called `influxd`, similar to `mysqld`.

From business analysis perspective, our code writes data into `influxdb`. Then our data analyst uses Grafana to query and make sense of the data.
