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
from .classes import Intensities
from mimetypes import guess_type


class ErrorCode(Exception):
    error: int

    def __init__(self, *args, error=None, **kwargs):
        assert error is not None
        self.error = error
        super().__init__(*args, **kwargs)
    # end def
# end class


def _convert_struct_to_luma(struct) -> Intensities:
    """
    :raises ErrorCode: The library had an error.
    """
    if struct.error:
        raise ErrorCode(error=struct.error)
    # end if
    return Intensities(nw=struct.nw, ne=struct.ne, sw=struct.sw, se=struct.se)
# end def


def jpg_intensities(filename) -> Intensities:
    """
    :raises ErrorCode: The library had an error.
    """
    filename = b(filename)
    result_struct = __lib.jpeg_intensities(filename)
    return _convert_struct_to_luma(result_struct)
# end def


def png_intensities(filename) -> Intensities:
    """
    :raises ErrorCode: The library had an error.
    """
    filename = b(filename)
    result_struct = __lib.png_intensities(filename)
    return _convert_struct_to_luma(result_struct)
# end def


def image_intensities(filename: str) -> Intensities:
    """
    :raises ErrorCode: The library had an error.
    :raises NotImplementedError: The file is not png/jpg.
    """
    (mime_type, encoding) = guess_type(filename)
    if mime_type == 'image/png':
        return png_intensities(filename)
    elif mime_type == 'image/jpeg':
        return jpg_intensities(filename)
    else:
        raise NotImplementedError('Unknown mime.')
    # end if
# end def
