"""
Command line utils to extract part of xml using xpath.
The utility comes with full namespace support.

Under the hook, this utility is a glorified wrapper for
`lxml`. Consider this a lightweight replacement for `xmlstarlet`
but with better stackoverflow searchability.

`xmlselect` is supposed to be used as part of a unix pipe.
Let's look at a couple of examples:

    $ echo "<svg><text>hello</text></svg>" | xmlselect "//text"
    hello


When it comes to more real-world XML documents, we'll need
to explicitly specify the namespace in the query.
Please refer to https://stackoverflow.com/a/56936158 if you
want to see human suffering in action.

Here is an example of production code

    $ cat barcode.svg | xmlselect -n "svg=http://www.w3.org/2000/svg" //svg:text
    <text style="...">14727</text>


Going further, the namespaces are definted in the URL
query string format. So, say, in order to query MathML
and SVG,  you can pass the following to the `-n` parameter:

    `-n svg=http://www.w3.org/2000/svgMathML=http://www.w3.org/1998/Math/MathML`

This utility is pretty self-contained, but it does require `lxml`.

    pip install lxml

"""
import sys
import urllib

from lxml import etree
import click as cli


@cli.command()
@cli.option(
    "-n",
    "--namespaces",
    "namespaces",
    help="Namespaces declared in URL query format. eg  `svg=http://www.w3.org/2000/svgMathML=http://www.w3.org/1998/Math/MathML`",
)
@cli.argument("selector")
def run(namespaces: str, selector: str):
    payload = sys.stdin.read().encode()
    soup = etree.fromstring(payload)
    elem = soup.xpath(selector, namespaces=urllib.parse.parse_qsl(namespaces))
    if isinstance(elem, list):
        for e in elem:
            sys.stdout.write(etree.tostring(e, encoding="unicode"))
    else:
        sys.stdout.write(etree.tostring(elem, encoding="unicode"))


if __name__ == "__main__":
    run()

