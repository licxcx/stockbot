# -*- coding: utf-8 -*-


from datetime import datetime
from stockbot.exceptions import InvalidDatetime


# 2015年周一到周五中的非交易日（休市）
CLOSE_DATE = ['2015-01-01', '2015-01-02', '2015-02-18', '2015-02-19',
              '2015-02-20', '2015-02-23', '2015-02-24', '2015-04-06',
              '2015-05-01', '2015-06-22', '2015-09-03', '2015-09-04',
              '2015-10-01', '2015-10-02', '2015-10-05', '2015-10-06',
              '2015-10-07']


def is_trading_date(date_time):
    """判断是否交易日"""
    if isinstance(date_time, datetime):
        weekday = date_time.isoweekday()
        if weekday == 6 or weekday == 7 or str(date_time.date()) in CLOSE_DATE:
            return False
        else:
            return True
    else:
        raise InvalidDatetime('Date is not instance of datetime, check the type!')


def is_trading_datetime(date_time):
    """判断是否为交易日交易时间"""
    if is_trading_date(date_time) and _is_trading_time(date_time):
        return True
    else:
        return False


def _is_trading_time(date_time):
    """判断是否为交易时间，不判断是否为交易日"""
    if isinstance(date_time, datetime):
        if date_time.hour == 9 and date_time.minute > 30:
            return True
        elif date_time.hour == 10 or date_time.hour == 13 or date_time.hour == 14:
            return True
        elif date_time.hour == 11 and date_time.minute < 30:
            return True
        else:
            return False
    else:
        raise InvalidDatetime('Time is not instance of datetime, check the type!')
