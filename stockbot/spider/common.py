#coding:utf-8

import logging
import requests
from requests import Request, Session

logger = logging.getLogger(__name__)


def retry(times):
    def deco(func):
        def wrapper(*args, **kwargs):
            for i in range(0, times):
                try:
                    resp = func(*args, **kwargs)
                except (requests.Timeout, requests.HTTPError, requests.ConnectionError), ex:
                    logger.warn('Caught requests exception')
                else:
                    return resp
            logger.error('Get response Failed %(t)s times', {'t': times})
        return wrapper
    return deco


class Spider(object):

    def __init__(self):
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                                     'AppleWebKit/537.36 (KHTML, like Gecko)'
                                     'Chrome/43.0.2357.130 Safari/537.36'}
        self.ses = Session()

    @retry(3)
    def get_response(self, method, url, data=None, params=None):
        reqt = Request(method, url, data=data, params=params, headers=self.headers)
        prepped = self.ses.prepare_request(reqt)
        resp = self.ses.send(prepped, stream=False)
        return resp