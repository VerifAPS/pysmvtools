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


def is_true(val: str):
    """
    >>> all(map(is_true, "True TRUE T".split(" ")))
    True

    :param val:
    :return:
    """
    return str(val).lower() in ("true", "yes", "t")


def is_false(val: str):
    """
    >>> any(map(is_false, "False FALSE F".split(" ")))
    True

    :param val:
    :return:
    """
    return str(val).lower() in ("false", "no", "f")


def is_dont_care(val):
    """
    >>> is_dont_care("*")
    True
    >>> is_dont_care("O")
    True
    >>> any(map(is_dont_care, "A b e True False blubb".split(" ")))
    False

    :param val:
    :return:
    """
    return str(val).lower() in ("*", "o")
