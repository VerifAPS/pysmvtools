
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


import functools
import yaml
import os

__author__ = "Alexander Weigl"
__date__ = "2016-03-16"


def find_config(filename):
    FILES = (
        filename,
        os.path.join(os.environ.get("XDG_CONFIG_DIR", "/"), filename),
        os.path.join(os.environ.get("HOME", "/"), filename),
        os.path.join(os.path.dirname(__file__), "..", filename),
    )
    f = filter(os.path.exists, FILES)
    return next(f)


class DictToObject(object):
    def __init__(self, map):
        self.d = map
        self._type = lambda x: x

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            return self.__getattribute__(item)

    def __getitem__(self, item):
        return self._wrap(item)

    def set_type(self, t):
        self._type = t

    def _wrap(self, item):
        o = self.d[item]
        if isinstance(o, dict):
            self.d[item] = o = DictToObject(o)
        else:
            self.d[item] = o = self._type(o)
        return o


@functools.lru_cache()
def load_config(filename="smvtools.cfg.yaml"):
    with open(find_config(filename)) as fp:
        return DictToObject(yaml.load(fp))
