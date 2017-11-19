# -*- coding: utf-8 -*-
# 2017, Kozlov Vasiliy <crarkie@gmail.com>

from enum import Enum

class DocState(Enum):
    Empty = 0
    Active = 1
    Outdated = 2