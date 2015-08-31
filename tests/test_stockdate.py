# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from stockbot.util import stockdate


class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_trading_date(self):
        self.assertTrue(stockdate.is_trading_date(datetime(2015, 8, 31, 9, 35, 21)))
        self.assertFalse(stockdate.is_trading_date(datetime(2015, 5, 1)))

    def test_is_trading_datetime(self):
        self.assertTrue(stockdate.is_trading_datetime(datetime(2015, 8, 31, 9, 35, 21)))
        self.assertFalse(stockdate.is_trading_datetime(datetime(2015, 8, 31, 12, 0, 21)))
        self.assertFalse(stockdate.is_trading_datetime(datetime(2015, 9, 3, 9, 35, 21)))
        self.assertFalse(stockdate.is_trading_datetime(datetime(2015, 5, 1, 9, 35, 21)))
        self.assertFalse(stockdate.is_trading_datetime(datetime(2015, 8, 31, 15, 35, 21)))

    def test_raise_tpyeerror(self):
        self.assertRaises(TypeError, stockdate.is_trading_datetime, '2015-08-01')


if __name__ == '__main__':
    unittest.main()
