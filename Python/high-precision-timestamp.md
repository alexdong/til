
## Python

The built-in `time.time` gives microseconds precision. There is also a
`time.time_ns()` but it does not give nanosecond resolution. It only returns
time in nanoseconds. [Discussion](https://stackoverflow.com/a/1938096/128601)

The `datetime.datetime.utcnow` also gives microseconds precision.

A fun fact is that there is also a Monotonic Clock, which is a thread-level
clock that will never go back. It's great when we need to calculate durations.
`time.monotonic_ns()`


## SqlAlchemy

> The problem I was having is that the stock SqlAlchemy DATETIME class does not
> work with the mysql requirement of passing a (6) value into the constructor
> in order to represent fractional time values. Instead, one needs to use the
> [sqlalchemy.dialects.mysql.DATETIME](https://docs.sqlalchemy.org/en/13/dialects/mysql.html#sqlalchemy.dialects.mysql.DATETIME)
> class. This class allows the use of the fsp parameter (fractional seconds
> parameter.) So, a column declaration should actually look like:
> dateCreated = Column(DATETIME(fsp=6)) 

## mysql

MySQL's DATETIME and TIMESTAMP can include a trailing fractional seconds part
in up to micrtoseconds (6 digits) precision. 

The colume type definition is `dt DATETIME(6)` or `TIMESTAMP(6)`. A value of 0
signifies that there is no fractional part. If omitted, the default precision
is 0.
