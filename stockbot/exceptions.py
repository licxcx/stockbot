# -*- coding: utf-8 -*-

# Date


class NonTradingDate(Exception):
    """Indicates the market is closed on the date"""
    pass


class InvalidDatetime(Exception):
    """Indicates invalid datetime type"""
    pass

