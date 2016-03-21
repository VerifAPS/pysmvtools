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



import argparse

from smvtools.ce import CounterExample
#from smvtools.td import draw


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
