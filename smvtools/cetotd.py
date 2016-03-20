#!/usr/bin/python3

"""

"""


import argparse

from smvtools.ce import CounterExample
from smvtools.td import draw


def cliparser():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--output", action="store", dest="output", metavar="FILE")
    return ap

def main():
    ap = cliparser()
    ns = ap.parse_args()

    ce = CounterExample.from_file(ns.file)
    ce.complete_states()
    td = ce.variable_traces()

    vars = {"%s.%s" % (mod,var) : val for mod, m in td.items() for var,val in m.items()}
    draw(vars, output_filename=ns.output)
