#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from luckydonaldUtils.logger import logging
from typing import List, Union, Tuple

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


def pixel_array_intensities(
    pixels: Union[List[int], List[Tuple[int, int, int]]], *, width: int, height: int
) -> Intensities:
    """
    :param pixels: List of the format [255,255,255, 255,255,255, ...] of pixel values. It has `width x height x 3` elements.
    :param width: width of the image, needed to figure out the quadrant a pixel is in.
    :param height: height of the image, needed to figure out the quadrant a pixel is in.
    :return: The calculated intensities in the quadrants.
    """
    assert len(pixels) == width * height * 3
    # plaintext_buf = __ffi.new("unsigned char [{}]".format(plaintext_size))
    # __lib.crypto_kem_dec(plaintext_buf, ciphertext, secret_key)
    final_bytes = b''
    if all(isinstance(element, int) for element in pixels):
        final_bytes += bytes(pixels)
    else:
        # so we found at least one tuple, so we gonna process that manually.
        for element in pixels:
            if isinstance(element, tuple):
                # (r, g, b), (r, g, b), ...
                final_bytes += bytes(element)
            else:
                # r, g, b, r, g, b, ...
                assert isinstance(element, int)
                final_bytes += bytes([element])
            # end if
        # end for
    # end if

    return pixel_bytes_intensities(final_bytes, width=width, height=height)
# end if


def pixel_bytes_intensities(pixels: bytes, *, width: int, height: int) -> Intensities:
    """
    :param pixels: Binary representation b'\0x255\0x255\0x255\0x255\0x255\0x255...' of pixel values. It has a length of `width x height x 3`.
    :param width: width of the image, needed to figure out the quadrant a pixel is in.
    :param height: height of the image, needed to figure out the quadrant a pixel is in.
    :return: The calculated intensities in the quadrants.
    """
    from PIL import Image
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(prefix='converted', suffix='png') as f:
        Image.frombytes(mode='RGB', data=pixels, size=(width, height)).convert('RGB').save(f.name)
        return png_intensities(f.name)
    # end with
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
        try:
            from PIL import Image
            from tempfile import NamedTemporaryFile
            with NamedTemporaryFile(prefix='converted', suffix='png') as f:
                Image.open(filename).convert('RGB').save(f.name)
                return png_intensities(f.name)
            # end with
        except ImportError:
            raise NotImplementedError(
                f'Unsupported mime, only `image/png` and `image/jpeg` are supported, got {mime_type}.'
            )
        # end try
    # end if
# end def
