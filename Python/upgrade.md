## Upgrade python in venv

### Install latest Python

```shell
# First, install the latest python3.8 to `/usr/local/bin/python`. 
# The latest stable release can be found at: https://www.python.org/downloads/
wget https://www.python.org/ftp/python/3.8.4/Python-3.8.4.tgz
tar -xf Python-3.8.4.tgz
cd Python-3.8.4/
./configure --enable-optimizations
make && make altinstall
```

### Update local venv and install packages

```shell
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
