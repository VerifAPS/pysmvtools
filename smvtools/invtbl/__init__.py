import csv
from collections import namedtuple
from itertools import starmap

FIELD_MONITORED = 'Monitored'
FIELD_OPERATOR = 'Operator'
FIELD_VALUE = 'Value'

OPERATOR_MAP = {
    "only if": "IMPLY",
    "iff": "EQUIV"
}

OPERATOR_INFIX = dict(
    AND="&",
    OR="|",
    NOT="!",
    IMPLY="->",
    EQUIV="="
)


class Invariant(object):
    def __init__(self, right, value, operator, expr=None):
        self.actuator = right
        self.value = value
        self.operator = operator
        self.expr = SExpr("OR", *(expr or []))

    def as_sexpr(self):
        sexpr = _create_proposition(self.actuator, self.value)
        return SExpr(OPERATOR_MAP.get(self.operator, "IMPLY"), sexpr, self.expr)

    def __str__(self):
        return str(self.as_sexpr())

    def as_infix(self):
        return self.as_sexpr().as_infix()


class InvariantTable(object):
    def __init__(self):
        self.invariants = []

    def __str__(self):
        return '\n'.join(map(str, self.invariants))

    def as_infix(self):
        return '\n'.join(map(as_infix, self.invariants))

    @staticmethod
    def from_csv(fileobj):
        obj = InvariantTable()

        with open(fileobj) as fp:
            tbl = csv.DictReader(fp)
            invariant = None
            for row in tbl:
                if row[FIELD_MONITORED]:
                    invariant = Invariant(row[FIELD_MONITORED], row[FIELD_VALUE], row[FIELD_OPERATOR], [])
                    obj.invariants.append(invariant)

                values = dict(row)

                del values[FIELD_MONITORED]
                del values[FIELD_OPERATOR]
                del values[FIELD_VALUE]

                invariant.expr.args.append(_as_conjunction(values))

        return obj


from ..core import *


def _begins_with_operator(string):
    """
    >>> _begins_with_operator("<=5")
    True
    >>> _begins_with_operator("<6")
    True
    >>> _begins_with_operator(">5")
    True
    >>> _begins_with_operator("5")
    False

    :param string:
    :return:
    """
    return string[0] in ('>', '<', '=')


def _split_operator(string):
    for i in range(len(string)):
        if string[i].isdigit():
            break
    return string[:i], string[i:]


def _is_interval(s: str):
    s = s.strip()
    return (s.endswith(")") or s.endswith("]")) and \
           (s.startswith("[") or s.startswith("("))


def _split_interval(s: str):
    s = s.strip("()[]")
    return tuple(map(lambda x: float(x.strip()), s.split(",")))


def _create_proposition(variable, value):
    """
    >>> _create_proposition("A", "true")
    A
    >>> _create_proposition("A", "false")
    (NOT A)
    >>> _create_proposition("A", "*")
    None
    >>> _create_proposition("A", ">2")
    (> A 2)
    >>> _create_proposition("A", "<=2")
    (<= A 2)
    >>> _create_proposition("A", "[2,6]")
    (AND (>= A 2) (<= A 6))

    :param variable:
    :param value:
    :return:
    """

    if is_true(value):
        return variable
    elif is_false(value):
        return SExpr("NOT", variable)
    elif is_dont_care(value):
        return None
    elif _begins_with_operator(value):
        op, val = _split_operator(value)
        return SExpr(op, variable, float(val))
    elif _is_interval(value):
        lower, upper = _split_interval(value)
        return SExpr('AND', SExpr('>=', variable, lower), SExpr('<=', variable, upper))

    return None


def _as_conjunction(map):
    args = filter(lambda x: x is not None,
                  starmap(_create_proposition, map.items()))
    return SExpr('AND', *list(args))


class SExpr(object):
    def __init__(self, operator, *rest):
        self.operator = operator
        self.args = list(rest)

    def __str__(self):
        return "(%s %s)" % (self.operator, ' '.join(map(str, self.args)))

    def as_infix(self):
        op = OPERATOR_INFIX.get(self.operator, self.operator)
        if self.operator == "NOT":
            return "%s %s" % (op, self.args[0])
        else:
            op = " %s " % op
            return op.join(map(as_infix, self.args))


def as_infix(obj):
    if hasattr(obj, "as_infix"):
        return "(%s)" % obj.as_infix()
    return str(obj)
