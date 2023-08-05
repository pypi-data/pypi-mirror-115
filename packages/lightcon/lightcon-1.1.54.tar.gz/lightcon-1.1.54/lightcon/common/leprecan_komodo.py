# -*- coding: utf-8 -*-
"""
Created on Thu May 18 17:45:11 2017

@author: butkus
"""
from ..common.leprecan_base import LepreCanBase

from ..common.komodo import Komodo

class LepreCanKomodo(LepreCanBase):
    def __init__(self):
        self.can_service = Komodo
    