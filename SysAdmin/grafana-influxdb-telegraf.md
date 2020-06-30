## Telegraf - Collector

Telegraf is a data collection agent which pulls data according `/etc/telegraf/telegraf.conf` `[[input]]` and store the data into whatever `[[output]]` is specified.

### Configure and test

After changing the `telegraf.conf` file, use `telegraf -config /etc/telegraf/telegraf.conf -test | less` to test the result. 
Or use `telegraf -config /etc/telegraf/telegraf.conf -test --input-filter mysql | less` to view only the measurements with `mysql`.

By default, telegraf does not create log file, which makes it impossible to find out why an input plugin is not working. 
We need to manually turn on the `debug=true` and `logtarget = "file"`.

### Data endpoint

Beyond the built-in [input plugins](https://docs.influxdata.com/telegraf/v1.14/plugins/plugin-list/#input-plugins), we can code up internal metrics http endpoints. Then we can configure telegraf to use the `http`[https://github.com/influxdata/telegraf/tree/master/plugins/inputs/http] to **pull** data from our server. ([CityBike Example](https://docs.influxdata.com/telegraf/v1.14/guides/using_http/))

The default pull interval is `10s` but we can set it to per hour with input level `interval` value as specified [here](https://docs.influxdata.com/telegraf/v1.2/administration/configuration/#input-configuration).

The data comes in as [InfluxDB line-data protocol](https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/). 

## InfluxDB - Data store

InfluxDB is a Time-series database with a SQL-like syntax.  influxDB itself doesn't have an UI. The query is done through `influx` command. Similar to
`mysql`. The influxdb server is called `influxd`, similar to `mysqld`.
From business analysis perspective, our code writes data into `influxdb`. Then our data analyst uses Grafana to query and make sense of the data.


## Grafana - Display
Grafana is a visualisation and alerting frontend that supports multiple backends, including Cloudwatch and InfluxDB. 
