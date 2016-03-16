"""

"""
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
