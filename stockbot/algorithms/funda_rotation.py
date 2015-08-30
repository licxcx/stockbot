# coding:utf-8

from __future__ import division
import sqlite3
import copy
import logging
from datetime import date

import xlwt

logger = logging.getLogger(__name__)

class Rotator(object):

    def __init__(self):
        self.rotate_range = '0.3%'
        self.db = '../data/stock.db'
        self.decision_data = {'+3.0%': {}, '+3.2%': {},
                              '+3.5%': {}, '+4.0%': {}}

    def calc_decision_data(self, coupon_descr):
        avg_num = 4 if coupon_descr == '+3.2%' else 10
        remove, sum = 0, 0
        profit = []
        for index, row in enumerate(self._select_data(coupon_descr)):
            if index < avg_num+remove:
                if row[2] in [u'深成指A', u'H股A']:
                    remove += 1
                else:
                    sum += float(row[10][:-1])*0.01
            profit.append(float(row[10][:-1])*0.01)
        reference = sum/avg_num
        self.decision_data[coupon_descr]['ref'] = format(reference, '.3%')
        self.decision_data[coupon_descr]['pos'] = self._find_ref_postion(reference, profit)

    def _find_ref_postion(self, reference, profit):
        all = copy.deepcopy(profit)
        all.append(reference)
        all.sort(reverse=True)
        return '{}/{}'.format(str(all.index(reference)), len(all))

    def _select_data(self, coupon_descr, orderby='volume'):
        holder = (coupon_descr, str(date.today()))
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('''select * from Afund where coupon_descr = ? and date = ?
                        order by {} desc '''.format(orderby), holder)
            return cur.fetchall()

    def _write_decision_data(self, coupon_descr, start_col, sheet):
        col = start_col
        sheet.write(0, col, coupon_descr)
        for k, v in self.decision_data[coupon_descr].items():
            sheet.write(0, col+1, v)
            col += 1

    def _write_selected_data(self, coupon_descr, start_col, sheet):
        for i, row in enumerate(self._select_data(coupon_descr, orderby='revised_profit')):
            col = start_col
            for j, cell in enumerate(row):
                if j in [1, 2, 10, 12]:              #code,name,revised_profit,base_premium_rate
                    sheet.write(i+1, col, cell)
                    col += 1

    def build_result(self, coupon_descr_list):
        stk_wb = xlwt.Workbook()
        myfont = xlwt.Font()
        mystyle = xlwt.XFStyle()
        mystyle.font = myfont
        sheet_name = str(date.today())
        sheet = stk_wb.add_sheet(sheet_name, cell_overwrite_ok=True)

        for index, item in enumerate(coupon_descr_list):
            self._write_decision_data(item, index*5, sheet)
            self._write_selected_data(item, index*5, sheet)

        stk_wb.save('../output/funda_rotation_{}'.format(sheet_name) + '.xls')


if __name__ == '__main__':
    logger = logging.root.addHandler(logging.StreamHandler)
    r = Rotator()
    coupons = ['+3.0%', '+3.2%', '+3.5%', '+4.0%']
    for coupon in coupons:
        r.calc_decision_data(coupon)
    r.build_result(coupons)

