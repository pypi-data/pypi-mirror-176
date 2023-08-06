#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
#
# Copyright 2020-2022 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
"""ANSI colors' and styles' definitions"""

from pathlib import Path
from typing import Dict, List

import toml


class AnsiCodes:
    """
    Structure containing text decoration codes

    ANSI codes' namespace

    Earlier, these values were imported from
    `colorama. <https://pypi.org/project/colorama/>`__

    This structure obviates such a need.
    """

    def __init__(self, ansi_dict: Dict[str, Dict[str, str]]):
        self.RESET_ALL = ''
        """Reset all styles to plain text"""

        self.GLOSS = {}
        """Gloss"""

        self.FG_COLORS = {}
        """Text (foreground) color"""

        self.BG_COLORS = {}
        """Background color"""

        self._section_names: List[str] = []
        for section_name, section in ansi_dict.items():
            _section = {}
            for code, ansi_seq in section.items():
                if code.isdigit():
                    _section[int(code)] = ansi_seq
                else:
                    _section[code] = ansi_seq
            if section_name == 'DEFAULT':
                for code, ansi_seq in _section.items():
                    setattr(self, code, ansi_seq)
                    self._section_names.append(code)
            else:
                setattr(self, section_name, _section)
                self._section_names.append(section_name)

    def __getitem__(self, __key):
        for section_name in self._section_names:
            if __key in getattr(self, section_name):
                return getattr(self, section_name)[__key]
        raise KeyError(
            f'{__key} is not a valid psprint terminal style descriptor')

    def __repr__(self):
        return '\n\n'.join((f'{section}: {repr(getattr(self, section))}'
                            for section in self._section_names))


with open(Path(__file__).resolve().parent / 'ansi.toml', 'r') as stream:
    ANSI = AnsiCodes(toml.load(stream))
    """
    ANSI Colors:

      * 0: black, k
      * 1: red, r
      * 2: green, g
      * 3: yellow, y
      * 4: blue, b
      * 5: magenta, m
      * 6: cyan, c
      * 7: white, w
      * 8 + `code`: light `color name`, l`c`
      * 16: terminal, t  (Terminal-determined)

    ANSI Gloss:

      * 0: reset all
      * 1: normal
      * 2: dim
      * 3: bright

    """
