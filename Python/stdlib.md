* Monotonic Clock is a clock that will never go back. It's great to calculate durations. `time.monotonic_ns()`
* MySQL's DATETIME and TIMESTAMP can include a trailing fractional seconds part in up to micrtoseconds (6 digits) precision. The colume type definition is `dt DATETIME(6)` or `TIMESTAMP(6)`. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0.

