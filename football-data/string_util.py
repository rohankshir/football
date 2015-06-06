# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from re import sub
from decimal import Decimal

def parse_currency(money):
    value = Decimal(sub(r'[^\d.]', '', money))
    return value
