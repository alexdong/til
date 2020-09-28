#!/usr/bin/env python3

"""
Bump the version number by 1.

This script should be used as a pre-commit script to automatically
increase the build number everytime we do a new commit.

The actual version is stored in `.version` file where this script is
located.

Usage:

    $ cat .version
    5.19.87
    $ version_bump.py
    $ cat .version
    5.19.88

"""

import subprocess

VERSION_FILE = ".version"
version = open(VERSION_FILE).read().strip()
major, minor, build = version.split('.')

# Beginning of the minor release
feature_head = f"{major}.{minor}.1"

# Get number of commits since then.
# Need `capture_output`, so the `wc` result is available through `stdout`.
r = subprocess.run(f"git log {feature_head}..HEAD | grep ^commit | wc -l", capture_output=True, shell=True)
next_commit = 1 + int(str(r.stdout, 'utf-8').strip())

with open(VERSION_FILE, 'w') as fp:
    fp.write(f"{major}.{minor}.{next_commit}")

