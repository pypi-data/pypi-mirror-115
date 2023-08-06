#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from luckydonaldUtils.logger import logging

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if


DEFAULT_DISTANCE = 0.25


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


class QuadrantSums(object):
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


class Intensities(object):
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

    def compare(self, other: 'Intensities', *, distance: float = DEFAULT_DISTANCE) -> bool:
        """
        Match by distance

        :param other: the Luma value to compare with.
        :param distance: suggested values: between 0.2 and 0.5
        :return:
        """
        return (
            self.nw - distance < other.nw < self.nw + distance and
            self.ne - distance < other.ne < self.ne + distance and
            self.sw - distance < other.sw < self.sw + distance and
            self.se - distance < other.se < self.se + distance
        )
    # end def

    def __repr__(self):
        return f"{self.__class__.__name__}(nw={self.nw!r}, ne={self.ne!r}, sw={self.sw!r}, se={self.se!r})"
    # end def
# end class
