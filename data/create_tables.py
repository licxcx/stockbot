# -*- coding:utf-8-*-
__author__ = 'lucasliu'
import sqlite3


def create_table():

    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute('''delete from stockhistory''')
    c.execute('''drop table stockhistory''')
    c.execute('''CREATE TABLE stockhistory(
                date text,
                code text,
                name text,
                closeprice real,
                hprice real,
                lprice real,
                openprice real,
                preprice real,
                flucv real,
                flucp real,
                volume real,
                primary key(date,code))''')
    conn.commit()
    conn.close()

# TODO timestap
def create_structured_fund():
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute('''delete from Afund''')
    c.execute('''drop table Afund''')
    c.execute('''CREATE TABLE Afund(
                date                date,
                code                text,
                name                text,
                current_price       real,
                coupon_descr        text,
                netvale             real,
                coupon              real,
                coupon_next         real,
                discount_rate       real,
                increase_rate       real,
                revised_profit      real,
                left_year           text,
                base_premium_rate   real,
                volume              real,
                primary key(date,code))''')
    conn.commit()
    conn.close()
# create_table()
create_structured_fund()