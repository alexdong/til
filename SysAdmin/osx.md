## brew

* restart service: `brew services restart redis`
* to see the plist: `vim ~/Library/LaunchAgents/homebrew.mxcl.redis.plist`

### Conventions on where the files are stored

* `conf` files:  `/usr/local/etc/redis.conf`
* `log` files:  `/usr/local/var/log/redis.log`
* `data` files are stored in `/usr/local/var`

### Directory permissions

* If the file's ownership is messed up, grant it again by using ```sudo chown -R "$USER":admin /usr/local/var/```

### Version

* `brew upgrade` will install `node@14` but our code base still uses `node@12`. Add `brew link --overwrite --force node@12`. Then add `/usr/local/opt/node@12/bin` to `PATH`.
