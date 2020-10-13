## Upgrade python in venv

```shell
# First, install the latest python3.8 to `/usr/local/bin/python`. 
# The latest stable release can be found at: https://www.python.org/downloads/
wget https://www.python.org/ftp/python/3.8.4/Python-3.8.4.tgz
tar -xf Python-3.8.4.tgz
cd Python-3.8.4/
./configure --enable-optimizations
make && make altinstall

# Now, go into the source code directory and update the local venv
/usr/local/bin/python3.8 -m venv .

# Update symlinks
rm bin/python
rm bin/python3
rm bin/python3.8
rm bin/pip
rm bin/pip3
rm bin/pip3.8
ln -s /usr/local/bin/python3.8 `pwd`/bin/python
ln -s /usr/local/bin/python3.8 `pwd`/bin/python3
ln -s /usr/local/bin/python3.8 `pwd`/bin/python3.8
ln -s /usr/local/bin/pip3.8 `pwd`/bin/pip
ln -s /usr/local/bin/pip3.8 `pwd`/bin/pip3
ln -s /usr/local/bin/pip3.8 `pwd`/bin/pip3.8


. bin/activate
pip install -r requirements/requirements-dev.txt
```

## Update Python venv after upgrading to Ubuntu 20.04 

```shell
# Establish the built-in python version
$ /usr/bin/python3.8 --version
Python 3.8.5

# Point local env's python to official python installation
# Then reinstall all packages. 
$ pip uninstall -y enum34
$ ln -s /usr/bin/python3.8 `pwd`/bin/python3.8
$ bin/python3.8 -m pip install --upgrade --force-reinstall -r requirements/requirements-dev.txt

```

Once the above is done, `service uwsgi restart` should bring the site up and
running. 

However, I did run into this on one of our server: 

```
Traceback (most recent call last):
  File "/opt/webapps/happymoose/lib/python3.8/site-packages/MySQLdb/__init__.py", line 18, in <module>
    from . import _mysql
ImportError: libmysqlclient.so.20: cannot open shared object file: No such file or directory
```


```shell
$ locate libmysqlclient.so.20
$ ln -s /usr/lib/x86_64-linux-gnu/libmysqlclient.so.20 /usr/lib/libmysqlclient.so.20

$ pushd /tmp && wget https://codeload.github.com/PyMySQL/mysqlclient-python/zip/master
$ unzip master.zip
$ cd mysqlclient-python-master
$ make
$ cp -r MySQLdb/* /opt/webapps/happymoose/lib/python3.8/site-packages/MySQLdb/
```

