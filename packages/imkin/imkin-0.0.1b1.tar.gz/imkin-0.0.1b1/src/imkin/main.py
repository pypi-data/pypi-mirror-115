#!/usr/bin/env python3
from collections import namedtuple
from .parsers import ImkinParser


def new(url, headers=None):
    Film = namedtuple("Film", "title original year duration")
    t, o, y, d = ImkinParser(url, headers=headers).parse()
    return Film(t, o, y, d)
