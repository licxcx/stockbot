# -*- coding: utf-8 -*-

import logging
import sqlite3
from datetime import datetime

from stockbot.spider.jisilu import FundASpider
from stockbot.util import stockdate


class DataManager(object):

    def __init__(self, db="stock.db"):
        self.fas = FundASpider()
        self.db = db

    def _insert_funda(self):
        self.fas.insert_funda_data()

    def _is_record_exists(self, date_time):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute('''select distinct date from Afund where date = ?''', (str(date_time.date()),))
            return True if cur.fetchall() else False

    def update_all_data(self):
        now = datetime.now()
        if stockdate.is_trading_datetime(now) and not self._is_record_exists(now):
            self._insert_funda()
            


if __name__ == '__main__':
    logging.root.addHandler(logging.StreamHandler())
    logging.root.setLevel(logging.DEBUG)
    dm = DataManager()
    dm.update_all_data()
