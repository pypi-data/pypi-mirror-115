#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

with open(str(Path(__file__).parent.absolute() / 'VERSION.txt'), 'r') as f:
    version = f.read().strip()
# end with

__version__ = version
VERSION = version

if __name__ == '__main__':
    print(__version__)
# end if
