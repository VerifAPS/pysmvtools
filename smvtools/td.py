# smvtools -- Tools around NuSMV and NuXMV
# Copyright (C) 2014-2016 - Alexander Weigl
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

"""

"""

import abc
import svgwrite as svg
from svgwrite.shapes import *
from svgwrite.text import *
from svgwrite.path import Path
from svgwrite.container import *
import argparse
import csv
from itertools import *
from os import system



class Scale(object):
    @abc.abstractmethod
    def __call__(self, obj):
        pass


class BoolScale(Scale):
    def __call__(self, obj):
        if is_true(obj):
            return 1
        elif is_false(obj):
            return 0
        return None


class ListScale(Scale):
    def __init__(self, values):
        self.scale = dict()
        l = float(len(values))
        for i, v in enumerate(values):
            self.scale[v] = i / l

    def __call__(self, obj):
        return self.scale.get(obj, None)


from .config import load_config


class Curve(object):
    def __init__(self, name: str, states: list, scala: Scale, config: dict = None):
        self.name = name
        self.states = states
        self.scale = scala

        if not config:
            self.config = load_config()
        else:
            self.config = config

    def draw(self):
        lenghts = self.config['timingdiagram']['lengths']
        styles = self.config['timingdiagram']

        seq = self.states
        grp = Group()

        lastframe = len(seq) * lenghts.FRAME_LENGTH + 2 * lenghts.BEGIN_MARGIN_FRAME

        Y_AXES_TOP = (lenghts.Y_AXE_STARTX, lenghts.Y_AXE_TOP_MARGIN)
        Y_AXES_BOT = (lenghts.Y_AXE_STARTX, lenghts.Y_AXE_TOP_MARGIN + lenghts.Y_AXE_HEIGHT)
        Y_AXES_END = (lenghts.Y_AXE_STARTX + lastframe, lenghts.Y_AXE_TOP_MARGIN + lenghts.Y_AXE_HEIGHT)

        grp.add(Line(Y_AXES_TOP, Y_AXES_BOT, **styles.axes.d))
        grp.add(Line(Y_AXES_BOT, Y_AXES_END, **styles.axes.d))

        grp.add(Line((lenghts.Y_AXE_STARTX - 2, lenghts.TOP_VALUE_LINE),
                     (lenghts.Y_AXE_STARTX + lastframe, lenghts.TOP_VALUE_LINE),
                     **styles.top_line.d))
        grp.add(Line((lenghts.Y_AXE_STARTX - 2, lenghts.BOT_VALUE_LINE),
                     (lenghts.Y_AXE_STARTX + lastframe, lenghts.BOT_VALUE_LINE),
                     **styles.bottom_line.d))

        grp.add(Text("true", (lenghts.WIDTH_VARIABLE_NAME, lenghts.TOP_VALUE_LINE), **styles.valuename.d))
        grp.add(Text("false", (lenghts.WIDTH_VARIABLE_NAME, lenghts.BOT_VALUE_LINE), **styles.valuename.d))
        grp.add(Text(self.name, (lenghts.WIDTH_VARIABLE_NAME - 10, lenghts.BOT_VALUE_LINE - 5), **styles.varname.d))

        grp.add(Path(self._build_curve(), **styles.curve.d))

        return grp

    def _build_curve(self):
        lengths = self.config['timingdiagram']['lengths']


        values = [self.scale(s) for s in self.states]

        s = "M%d %d  " % (lengths.Y_AXE_STARTX + lengths.BEGIN_MARGIN_FRAME,
                          lengths.TOP_VALUE_LINE if is_true(values[0]) else lengths.BOT_VALUE_LINE)

        # s = "M%d %d H%d " % (Y_AXE_STARTX,
        #                     TOP_VALUE_LINE if is_true(values[0]) else BOT_VALUE_LINE,
        #                     Y_AXE_STARTX + BEGIN_MARGIN_FRAME)

        for i in range(0, len(values)):
            xnxt = (i + 1) * lengths.FRAME_LENGTH + lengths.Y_AXE_STARTX + lengths.BEGIN_MARGIN_FRAME

            v = values[i]
            if is_dont_care(v):
                s += "M%d %d " % (xnxt,
                                  lengths.TOP_VALUE_LINE if is_true(values[i + 1]) else lengths.BOT_VALUE_LINE)
                continue

            s += "V%d " % (lengths.TOP_VALUE_LINE if is_true(v) else lengths.BOT_VALUE_LINE)
            s += "H%d " % xnxt
        return s


class TimingDiagram(object):
    def __init__(self, curves, config=None):
        self.curves = curves
        if not config:
            self.config = load_config()
        else:
            self.config = config

    def draw(self, variables: list, output_filename="test.svg"):
        styles = self.config['timingdiagram']
        lengths = self.config['timingdiagram']['lengths']
        lengths.set_type(float)

        frames = len(self.curves[0].states)
        numcurves = len(self.curves)

        w = lengths.BEGIN_MARGIN_FRAME + frames * lengths.FRAME_LENGTH + lengths.WIDTH_VARIABLE_NAME
        h = numcurves * lengths.ROW_HEIGHT
        d = svg.Drawing(output_filename, profile='tiny',
                        size=("%dmm" % w,
                              "%dmm" % h),
                        viewBox=('0 0 %d %d' % (w, h)))  # use mm for sizespecification

        for i, curve in enumerate(self.curves):
            panel = curve.draw()
            panel.translate(0, i * lengths.ROW_HEIGHT)
            d.add(panel)

        takt = Group()
        takt.translate(lengths.Y_AXE_STARTX + lengths.BEGIN_MARGIN_FRAME, 0)
        ytop = lengths.Y_AXE_TOP_MARGIN
        ybot = len(variables) * lengths.ROW_HEIGHT

        for i in range(frames):
            x = i * lengths.FRAME_LENGTH
            takt.add(Line((x, ytop), (x, ybot), **styles.takt.d))

        d.add(takt)
        d.save()

    @staticmethod
    def from_csv(states, config=None):
        if not config:
            config = load_config()

        variables = slice_to_vars(states)

        names = sorted(variables.keys())

        def create(name):
            return Curve(name=name, states=variables[name], scala=BoolScale(), config=config)

        curves = list(map(create, names))

        td = TimingDiagram(curves)
        return td


def slice_to_vars(states):
    """
    >>> True
    False

    :param states:
    :return:
    """
    variables = {var: list() for var in states[0].keys()}

    for s in states:
        for var in variables.keys():
            variables[var].append(s[var])

    return variables
