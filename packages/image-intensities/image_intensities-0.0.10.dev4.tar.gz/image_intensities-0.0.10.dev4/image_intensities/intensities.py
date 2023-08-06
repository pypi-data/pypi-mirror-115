#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from luckydonaldUtils.logger import logging
from luckydonaldUtils.encoding import to_binary as b

__author__ = 'luckydonald'

# logger = logging.getLogger(__name__)
# if __name__ == '__main__':
#     logging.add_colored_handler(level=logging.DEBUG)
# # end if

# noinspection PyUnresolvedReferences
from ._intensities import ffi as __ffi, lib as __lib
from .classes import Luma


def _convert_struct_to_luma(struct) -> Luma:
    return Luma(nw=struct.nw, ne=struct.ne, sw=struct.sw, se=struct.se)
# end def


def jpeg_intensities(filename) -> Luma:
    filename = b(filename)
    result_struct = __lib.jpeg_intensities(filename)
    return _convert_struct_to_luma(result_struct)
# end def


def png_intensities(filename) -> Luma:
    filename = b(filename)
    result_struct = __lib.png_intensities(filename)
    return _convert_struct_to_luma(result_struct)
# end def
