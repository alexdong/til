#!/usr/bin/env python3

"""
hydrojinja takes a JSON payload from `stdin`, uses it to render a jinja2 template
with output piped out via `stdout`.

For example: the following command takes the JSON records in data.txt,
use it to render `template.svg` and save the output into `/tmp/data.svg`.

  cat data.txt | hydrojinja $PROJECT_BASE/production/everyday_photo_books/cover.svg > /tmp/data.svg

Please note that

1. The template_path is a relative path based to `./templates`.
2. The data needs to be a valid string which may require `escape`. 

"""
import json
import sys

from flask import render_template
import click as cli


@cli.command()
@cli.argument("template_file_path")
def run(svg_file_path):
    payload = sys.stdin.read()
    target = render_template(svg_file_path, **json.loads(payload, strict=False))
    sys.stdout.write(target)

