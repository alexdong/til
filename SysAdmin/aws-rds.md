# Performance

1. [RDS w/ MySQL common wait
   events](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Reference.html#AuroraMySQL.Reference.Waitevents)

2. [RDS Storage
   type](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html#Concepts.Storage.GeneralSSD):
   "For a production application that requires fast and consistent I/O
   performance, we recommend Provisioned IOPS (input/output operations per
       second) storage.  Provisioned IOPS storage is a storage type that
   delivers predictable performance, and consistently low latency. Provisioned
   IOPS storage is optimized for online transaction processing (OLTP) workloads
   that have consistent performance requirements. Provisioned IOPS helps
   performance tuning of these workloads."

3. [RAM Recommendations](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html):
   "To tell if your working set is almost all in memory, check the ReadIOPS
   metric (using Amazon CloudWatch) while the DB instance is under load. The
   value of ReadIOPS should be small and stable. If scaling up the DB instance
   class—to a class with more RAM—results in a dramatic drop in ReadIOPS, your
   working set was not almost completely in memory. Continue to scale up until
   ReadIOPS no longer drops dramatically after a scaling operation, or ReadIOPS
   is reduced to a very small amount.  "

4. To see the host server's "Exhanced Monitoring" details, go to "CloudWatch > Log groups > RDSOSMetrics". 
   `memory.free`, `memory.total` shows free and total RAM. [Definitions of all metrics](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html#USER_Monitoring.OS.CloudWatchLogs). `processList.memoryUsedPc` and `processList.cpuUsedPc`.
