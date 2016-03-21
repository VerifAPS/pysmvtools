#!/usr/bin/python3

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

__author__ = "Alexander Weigl <Alexander.Weigl@kit.edu>"
__version__ = "0.2"
__license__ = "GPLv3"

import sys
import os, os.path

from functools import partial

from jinja2 import Environment
from collections import defaultdict
from argparse import ArgumentParser
import click

def get_path(filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

def read(filename):
    with open(get_path(filename)) as fp:
        return fp.read()


TEMPLATE = read("smvceviz.tpl")
CSS_PATH = get_path("smvceviz.css")
JS_PATH = get_path("smvceviz.js")

def classes(modules, mod, step, var, m1="m1", m2="m2", sub_seperator="$"):
    def changed():
        """determines if the value has changed since last step.
        """
        if step == 0:
            return "changed"

        try:
            c = modules[mod][step - 1][var] != modules[mod][step][var]
            return "changed" if c else "not-changed"
        except:
            return "changed"

    def compare():
        """compares to modules with each other
        """
        if mod == m1:
            omod = m2

        elif mod == m2:
            omod = m1

        else:
            return "no-compare"

        try:
            c = modules[mod][step][var] != modules[omod][step][var]
            return "not-equals" if c else "equals"
        except:
            return "not-equals one-sided"

    def submodule_name():
        if sub_seperator in var:
            return ' '.join(var.split(sub_seperator))
        return "no-sub-module " + var

    return ' '.join((changed(), compare(), submodule_name()))


