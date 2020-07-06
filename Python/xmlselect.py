"""
Command line utils to extract part of xml using xpath.
The utility comes with full namespace support.

Under the hook, this utility is a glorified wrapper for
`lxml`. Consider this a lightweight replacement for `xmlstarlet`
but with better stackoverflow searchability.

`xmlselect` is supposed to be used as part of a unix pipe.
Let's look at a couple of examples:

    $ echo "<svg><text>hello</text></svg>" | xmlselect "//text"
    <text>hello</text>


When it comes to more real-world XML documents, we'll need
to explicitly specify the namespace in the query.
Please refer to https://stackoverflow.com/a/56936158 if you
want to see human suffering in action.

Here is an example of production code

    $ cat barcode.svg | xmlselect -n "svg=http://www.w3.org/2000/svg" //svg:g
    <g><text>...</text></g>


When you want to print only the 'inner XML`, use the `-c` or `--children-only`.
For example, in the example above, here is the command to print only the children
of `<g>`:

    $ cat barcode.svg | xmlselect -i -n "svg=http://www.w3.org/2000/svg" //svg:g
    <text>...</text>


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


def print_element(e):
    sys.stdout.write(etree.tostring(e, encoding="unicode"))


def print_inner_nodes(e):
    for child in e:
        print_element(child)


def print_node(e, show_only_children):
    print_inner_nodes(e) if show_only_children else print_element(e)


@cli.command()
@cli.option(
    "-n",
    "--namespaces",
    "namespaces",
    help="Namespaces declared in URL query format. eg  `svg=http://www.w3.org/2000/svgMathML=http://www.w3.org/1998/Math/MathML`",
)
@cli.option(
    "-c",
    "--children-only",
    "show_children_only",
    is_flag=True,
    default=False,
    help="Show only the inner XML",
)
@cli.argument("selector")
def run(namespaces: str, show_children_only: bool, selector: str):
    payload = sys.stdin.read().encode()
    elem = etree.fromstring(payload).xpath(
        selector, namespaces=urllib.parse.parse_qsl(namespaces)
    )
    if isinstance(elem, list):
        for e in elem:
            print_node(e, show_only_children=show_children_only)
    else:
        print_node(elem, show_only_children=show_children_only)


if __name__ == "__main__":
    run()

