#!/usr/bin/python3

#
#
#
#

"""

"""

import argparse
import csv
from itertools import *


def read(filename):
    states = []
    with open(filename) as fp:
        rd = csv.DictReader(fp)  # default: excel
        for row in rd:
            states.append(row)
    return states


def is_true(val):
    return str(val).lower() in ("true", "yes")


def is_false(val):
    return str(val).lower() in ("false", "no")


def is_dont_care(val):
    return str(val).lower() in ("*", "o")


def condition(state: dict):
    def to_literal(n):
        if is_true(state[n]):
            return n
        elif is_false(state[n]):
            return "! %s" % n
        elif is_dont_care(state[n]):
            return "TRUE"
        else:
            return "%s = %s" % (n, state[n])

    names = sorted(state.keys())
    literals = map(to_literal, names)
    return ' & '.join(literals)


def generate(states: list,
             module_name: str = "StutterAutomata",
             triggerfml='TRUE'):
    state_names = starmap(lambda i, s: "line_%d" % (1 + i), enumerate(states))
    variables = sorted(states[0].keys())

    print("""
    MODULE %s(%s)

    VAR state : { inactive, %s, accept, error}

    DEFINE Trigger := %s
           FOUND   := (state = success);


    ASSIGN
\tinit(state) := inactive;
\tnext(state) := case
\t\t(state=inactive | state=success) & Trigger : line_1;
\t\tstate = error : error;""" % (module_name, ','.join(variables), ','.join(state_names), triggerfml))

    for i, state in enumerate(states[:-1]):
        if i < len(states) - 2:
            next_state = "line_%d" % (i + 2)
        else:
            next_state = "success"

        print("\t\t state = line_%d &" % (i + 1), condition(state), ':', 'line_%d' % (i + 1),'; -- stuttering')
        print("\t\t state = line_%d &" % (i + 1), condition(states[i + 1]), ":", next_state,';  -- next line ')



    print("""\t\tTRUE : error; -- if no transition matches above we have a counterexample against this word under stuttering
        esac;""")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", help="name of the generated module",
                    action="store", default="StutteringAutomata", dest="name")
    ap.add_argument("file")

    ns = ap.parse_args()

    states = read(ns.file)
    generate(states)


if __name__ == "__main__":
    main()
