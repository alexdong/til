## brew

* restart service: `brew services restart redis`
* to see the plist: `vim ~/Library/LaunchAgents/homebrew.mxcl.redis.plist`

### Conventions on where the files are stored

* `conf` files:  `/usr/local/etc/redis.conf`
* `log` files:  `/usr/local/var/log/redis.log`
* `data` files are stored in `/usr/local/var`

### Directory permissions

* If the file's ownership is messed up, grant it again by using ```sudo chown -R "$USER":admin /usr/local/var/```

