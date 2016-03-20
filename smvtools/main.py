import click

from smvtools.invtbl import InvariantTable
from smvtools.td import TimingDiagram
import csv

from functools import *
from jinja2 import Environment


def readcsv(fp):
    """

    :param fp:
    :return:
    """
    states = []
    rd = csv.DictReader(fp)  # default: excel
    for row in rd:
        states.append(row)
    return states


@click.command()
@click.argument('csvfile', type=click.File('r'), )
@click.argument('output', type=str, )
def drawtd(output, csvfile):
    """

    :param output:
    :param csvfile:
    :return:
    """
    c = readcsv(csvfile)
    td = TimingDiagram.from_csv(c)
    td.draw(output)


@click.command()
@click.argument("-1", '--module1')
@click.argument("-2", '--module2')
@click.argument("file")
def ceviz(mod1, mod2, file):
    args = ap.parse_args()

    trace = Trace.from_file(args.file)
    trace.complete_states()
    jinja = Environment()

    cmp = partial(classes, sub_seperator="$", m1=args.module1, m2=args.module2)

    jinja.globals.update(sorted=sorted, classes=cmp)
    T = jinja.from_string(TEMPLATE)

    print(T.render(
        css_path=CSS_PATH,
        js_path=JS_PATH,
        modules=trace.modules,
        trace=trace,
        length=len(trace.modules['input'])))


@click.command()
@click.argument("input")
@click.option("create")
def invtbl2smv(input, create=False):
    """

    :param input:
    :param create:
    :return:
    """
    tbl = InvariantTable.from_csv(input)
    print(tbl)
    print(tbl.as_infix())
