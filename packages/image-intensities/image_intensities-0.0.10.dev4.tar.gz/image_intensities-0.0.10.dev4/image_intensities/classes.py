#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from luckydonaldUtils.logger import logging

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if

class RGB(object):
    r: int
    g: int
    b: int

    def __init__(
        self,
        r: int = 0,
        g: int = 0,
        b: int = 0,
    ):
        self.r = r
        self.g = g
        self.b = b
    # end def

    def __repr__(self):
        return f"{self.__class__.__name__}(r={self.r!r}, g={self.g!r}, b={self.b!r})"
    # end def
# end class


class Sums(object):
    nw: RGB
    ne: RGB
    sw: RGB
    se: RGB

    # noinspection PyShadowingNames
    def __init__(
        self,
        nw: Union[None, RGB] = None,
        ne: Union[None, RGB] = None,
        sw: Union[None, RGB] = None,
        se: Union[None, RGB] = None,
    ):
        if nw is None:
            nw = RGB()
        # end if
        self.nw = nw
        if ne is None:
            ne = RGB()
        # end if
        self.ne = ne
        if sw is None:
            sw = RGB()
        # end if
        self.sw = sw
        if se is None:
            se = RGB()
        # end if
        self.se = se
    # end def

    def __repr__(self):
        return f"{self.__class__.__name__}(nw={self.nw!r}, ne={self.ne!r}, sw={self.sw!r}, se={self.se!r})"
    # end def
# end class


class Luma(object):
    nw: float
    ne: float
    sw: float
    se: float

    def __init__(self, nw: float, ne: float, sw: float, se: float):
        self.nw = nw
        self.ne = ne
        self.sw = sw
        self.se = se
    # end def

    def equals(self, other):
        return (
            self.nw == other.nw and
            self.ne == other.ne and
            self.sw == other.sw and
            self.se == other.se
        )
    # end def

    __eq__ = equals

    def compare(self, other: 'Luma', distance: float = 0.25,):
        """
        Match by distance

        :param distance: suggested values: between 0.2 and 0.5
        :return:
        """
        return (
            self.nw - 0.25 < other.nw < self.nw + 0.25 and
            self.ne - 0.25 < other.ne < self.ne + 0.25 and
            self.sw - 0.25 < other.sw < self.sw + 0.25 and
            self.se - 0.25 < other.se < self.se + 0.25
        )
    # end def

    def __repr__(self):
        return f"{self.__class__.__name__}(nw={self.nw!r}, ne={self.ne!r}, sw={self.sw!r}, se={self.se!r})"
    # end def
# end class
