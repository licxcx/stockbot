# coding:utf-8

import logging
import time
import collections
from datetime import date
import sqlite3

from stockbot.spider.common import Spider

logger = logging.getLogger(__name__)


class FundASpider(Spider):

    def __init__(self, db):
        super(FundASpider, self).__init__()
        self.url = 'http://www.jisilu.cn/data/sfnew/funda_list/?___t={time}'.format(time=str(int(time.time())))
        self.data = {'is_funda_search': '1',
                    'fundavolume': '100',
                    'market[]': ['sh', 'sz'],
                    'coupon_descr[]': ['+4.0%', '+3.0%', '+3.2%', '+3.5%']}
        self.method = 'post'
        self.db = db

    def get_jsl_data(self):
        funda = self.get_response(self.method, self.url, data=self.data).json()
        return funda

    def parse_jsl_data(self):
        raw = self.get_jsl_data()
        myfunda = collections.OrderedDict()
        today = date.today()
        for row in raw['rows']:
            # myfunda['date'] = row['cell']['funda_nav_dt']
            myfunda['date'] = str(today)
            myfunda['code'] = row['cell']['funda_id']
            myfunda['name'] = row['cell']['funda_name'].encode('utf-8')
            myfunda['current_price'] = row['cell']['funda_current_price']
            myfunda['coupon_descr'] = row['cell']['coupon_descr']
            myfunda['netvalue'] = row['cell']['funda_value']
            myfunda['coupon'] = row['cell']['funda_coupon']
            myfunda['coupon_next'] = row['cell']['funda_coupon_next']
            myfunda['discount_rate'] = row['cell']['funda_discount_rt']
            myfunda['increase_rate'] = row['cell']['funda_increase_rt']
            myfunda['revised_profit'] = row['cell']['funda_profit_rt_next']
            myfunda['left_year'] = row['cell']['funda_left_year'].encode('utf-8')
            myfunda['base_premium_rate'] = row['cell']['funda_base_est_dis_rt']
            myfunda['volume'] = row['cell']['funda_amount']
            yield myfunda

    def insert_funda_data(self):
        with sqlite3.connect(self.db) as conn:
            conn.text_factory = str
            cur = conn.cursor()
            for myfunda in self.parse_jsl_data():
                if myfunda['left_year'] == '永续':
                    values = tuple(myfunda.values())
                    logger.info(values)
                    cur.execute('insert into Afund values( ?,?,?,?,?,?,?,?,?,?,?,?,?,?)', values)

    def update_funda_data(self):
        pass


