# -*- coding: utf-8 -*-

import logging

from stockbot.spider.jisilu import FundASpider
from stockbot.util import stockdate


class DataManager(object):

    def __init__(self):
        self.fas = FundASpider()

    def update_all_data(self):
        self._insert_funda()

    def _insert_funda(self):
        self.fas.insert_funda_data()

if __name__ == '__main__':
    logging.root.addHandler(logging.StreamHandler())
    logging.root.setLevel(logging.DEBUG)
    dm = DataManager()
    dm.update_all_data()
