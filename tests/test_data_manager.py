# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from stockbot.data.data_manager import DataManager


class DataManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.dm = DataManager("../stockbot/data/stock.db")

    def test_is_record_exists(self):
        now = datetime.now()
        self.assertEqual(False, self.dm._is_record_exists(now))

if __name__ == '__main__':
    unittest.main()
