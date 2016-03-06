import svgwrite as svg
from svgwrite.shapes import *
from svgwrite.text import *
from svgwrite.path import Path
from svgwrite.container import *
import argparse
import csv
from itertools import *
from os import system


class Styles:
    TAKT = {
        'stroke': 'blue',
        'stroke-opacity': 0.5,
        'stroke-width': '0.2mm',
        'stroke-dasharray': "1,1"
    }
    AXES = {
        'stroke': 'black',
        'stroke-width': '0.2mm',

    }

    VALUE_CURVE = {
        'stroke': 'black',
        'stroke-opacity': 0.6,
        'stroke-width': '0.5mm',
        'fill': 'none'
    }

    VARNAME = {
        'font-size': '2mm',
        'text-anchor': 'end',
        'alignment-baseline': 'middle',
        'font-family': 'monospace'
    }

    VALUENAME = {
        'font-size': '1mm',
        'alignment-baseline': 'middle',
    }

    TOP_LINE = {
        'stroke': 'green',
        'stroke-width': '0.1mm',
    }

    BOTTOM_LINE = {
        'stroke': 'red',
        'stroke-width': '0.1mm',
    }


def read(filename):
    states = []
    with open(filename) as fp:
        rd = csv.DictReader(fp)  # default: excel
        for row in rd:
            states.append(row)
    return states


def slice_to_vars(states):
    variables = {var: list() for var in states[0].keys()}

    for s in states:
        for var in variables.keys():
            variables[var].append(s[var])

    return variables


FRAME_LENGTH = 15
ROW_HEIGHT = 25
WIDTH_VARIABLE_NAME = 100
WIDTH_VALUE_NAMES = 10
BEGIN_MARGIN_FRAME = 10
Y_AXE_STARTX = WIDTH_VARIABLE_NAME + WIDTH_VALUE_NAMES
Y_AXE_HEIGHT = 20
Y_AXE_TOP_MARGIN = 3
TOP_VALUE_LINE = 10
BOT_VALUE_LINE = 18


def draw_timeline(d: svg.Drawing, name, seq):
    grp = Group()

    lastframe = len(seq) * FRAME_LENGTH + 2 * BEGIN_MARGIN_FRAME

    Y_AXES_TOP = (Y_AXE_STARTX, Y_AXE_TOP_MARGIN)
    Y_AXES_BOT = (Y_AXE_STARTX, Y_AXE_TOP_MARGIN + Y_AXE_HEIGHT)
    Y_AXES_END = (Y_AXE_STARTX + lastframe, Y_AXE_TOP_MARGIN + Y_AXE_HEIGHT)

    grp.add(Line(Y_AXES_TOP, Y_AXES_BOT, **Styles.AXES))
    grp.add(Line(Y_AXES_BOT, Y_AXES_END, **Styles.AXES))

    grp.add(Line((Y_AXE_STARTX - 2, TOP_VALUE_LINE), (Y_AXE_STARTX + lastframe, TOP_VALUE_LINE),
                 **Styles.TOP_LINE))
    grp.add(Line((Y_AXE_STARTX - 2, BOT_VALUE_LINE), (Y_AXE_STARTX + lastframe, BOT_VALUE_LINE),
                 **Styles.BOTTOM_LINE))

    grp.add(Text("true", (WIDTH_VARIABLE_NAME, TOP_VALUE_LINE), **Styles.VALUENAME))
    grp.add(Text("false", (WIDTH_VARIABLE_NAME, BOT_VALUE_LINE), **Styles.VALUENAME))
    grp.add(Text(name, (WIDTH_VARIABLE_NAME - 10, BOT_VALUE_LINE - 5), **Styles.VARNAME))

    print(name)
    grp.add(Path(build_curve(seq), **Styles.VALUE_CURVE))

    return grp


def is_true(val):
    return str(val).lower() in ("true", "yes")


def is_false(val):
    return str(val).lower() in ("false", "no")


def is_dont_care(val):
    return str(val).lower() in ("*", "o")


def build_curve(values):
    s = "M%d %d  " % (Y_AXE_STARTX + BEGIN_MARGIN_FRAME,
                      TOP_VALUE_LINE if is_true(values[0]) else BOT_VALUE_LINE)

    # s = "M%d %d H%d " % (Y_AXE_STARTX,
    #                     TOP_VALUE_LINE if is_true(values[0]) else BOT_VALUE_LINE,
    #                     Y_AXE_STARTX + BEGIN_MARGIN_FRAME)

    for i in range(0, len(values)):
        xnxt = (i + 1) * FRAME_LENGTH + Y_AXE_STARTX + BEGIN_MARGIN_FRAME

        v = values[i]
        if is_dont_care(v):
            s += "M%d %d " % (xnxt,
                              TOP_VALUE_LINE if is_true(values[i + 1]) else BOT_VALUE_LINE)
            continue

        s += "V%d " % (TOP_VALUE_LINE if is_true(v) else BOT_VALUE_LINE)
        s += "H%d " % xnxt

    print(s)
    return s


def draw(states: list, output_filename="test.svg"):
    frames = len(states)

    frames_position = [
        FRAME_LENGTH * i for i in range(frames)
        ]

    variables = slice_to_vars(states)
    names = sorted(variables.keys())

    w = (BEGIN_MARGIN_FRAME + frames * FRAME_LENGTH + WIDTH_VARIABLE_NAME)
    h = (len(names) * ROW_HEIGHT)
    d = svg.Drawing(output_filename, profile='tiny',
                    size=("%dmm" % w,
                          "%dmm" % h),
                    viewBox=('0 0 %d %d' % (w, h)))  # use mm for sizespecification

    #    d.add_stylesheet("draw.css", 'draw')

    for i, var in enumerate(names):
        seq = variables[var]
        panel = draw_timeline(d, var, seq)
        panel.translate(0, i * ROW_HEIGHT)
        d.add(panel)

    takt = Group()
    takt.translate(Y_AXE_STARTX + BEGIN_MARGIN_FRAME, 0)
    ytop = Y_AXE_TOP_MARGIN
    ybot = len(variables) * ROW_HEIGHT
    for i in range(len(states)):
        x = i * FRAME_LENGTH

        takt.add(Line((x, ytop), (x, ybot), **Styles.TAKT))
    d.add(takt)

    d.save()


#    system("eog test.svg")

if __name__ == "__main__":
    import sys

    states = read(sys.argv[1])
    draw(states)
