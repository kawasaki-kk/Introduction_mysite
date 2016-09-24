import time
import os

import codecs
import json
from logging import getLogger
import requests
from urllib.parse import urlparse, parse_qs
from services import load_json

logger = getLogger(__name__)

URL_ITEMS     = "https://qiita.com/api/v2/items"
URL_TAG_ITEMS = "https://qiita.com/api/v2/tags/%s/items"
URL_TAGS      = "https://qiita.com/api/v2/tags"

HEADER_TOTAL = "Total-Count"
LINK_NEXT = "next"
LINK_LAST = "last"

default_per_page = 100
default_max_page = 100 
wait_seconds = 12
retry_wait_min = 1
retry_limit = 10

auth_token = load_json(os.path.dirname(os.path.abspath(__file__)), "auth_token.json")["qiita"]

def items(per_page = default_per_page, max_page = default_max_page):
    req = QiitaRequest(URL_ITEMS, per_page, max_page)
    return QiitaIterator(req)

def tag_items(tag_url, per_page = default_per_page, max_page = default_max_page):
    req = QiitaRequest(URL_TAG_ITEMS % tag_url, per_page, max_page)
    return QiitaIterator(req)

def tags(per_page = default_per_page, max_page = default_max_page):
    req = QiitaRequest(URL_TAGS, per_page, max_page)
    return QiitaIterator(req)

class QiitaIterator:
    def __init__(self, req):
        self.req = req
        self.items = req.request().__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        if self.items == None: raise StopIteration
        try:
            val = self.items.__next__()
            return val
        except StopIteration:
            if self.req.has_next():
                self.items = self.req.next().__iter__()
                return self.__next__()
            else:
                raise StopIteration

    def __len__(self):
        return self.req.total_count()

class QiitaRequest:

    last_request_time = None

    retry_num = 0

    def __init__(self, url, per_page = default_per_page, max_page = default_max_page, page = 1):
        self.url = url
        self.per_page = per_page
        self.max_page = max_page
        self.page = page
        self.res = None
        self.current_page = None

    def request(self):
        self.links = dict()
        params = {"per_page": self.per_page, "page": self.page}
        return self.__request__(self.url, params)

    def __request__(self, url, params = None):
        self.__wait__()
        logger.info("url:%s" % url)

        headers = {"Authorization": "Bearer " + auth_token} if auth_token != None else None
        self.res = requests.get(url, params = params, headers = headers)
        status = self.res.status_code

        while status != 200 and QiitaRequest.retry_num <= retry_limit:
            logger.warning("status:%d" % status)
            logger.warn("Wait for %d minuts" % retry_wait_min)
            time.sleep(retry_wait_min * 60)
            QiitaRequest.retry_num = QiitaRequest.retry_num + 1
            self.res = requests.get(url, params = params)
            status = self.res.status_code

        if status != 200:
            logger.warning("status:%d" % status)
            logger.warning(self.res.text)
            return None

        QiitaRequest.retry_num = 0
        return self.res.json()

    def next(self):
        if not self.has_next(): raise Exception()
        # For bug of lacking of per_page in Link response header on v2 
        params = {"per_page": self.per_page}
        return self.__request__(self.res.links[LINK_NEXT]["url"], params)

    def retry(self):
        pass
    def has_error(self):
        pass
    def has_next(self):
        if not LINK_NEXT in self.res.links: return False
        url = self.res.links[LINK_NEXT]["url"]
        page = self.__get_page__(url)
        return page <= self.max_page

    def last_page(self):
        url = self.res.links[LINK_LAST]["url"]
        return self.__get_page__(url)

    def total_count(self):
        return int(self.res.headers[HEADER_TOTAL])

    def __get_page__(self, url):
        query = urlparse(url).query
        page = parse_qs(query)["page"][0]
        return int(page)

    def __wait__(self):
        if QiitaRequest.last_request_time != None:
            last = QiitaRequest.last_request_time
            now = time.clock()
            wait = wait_seconds - (now - last)
            if 0 < wait:
                time.sleep(wait)
        QiitaRequest.last_request_time = time.clock()

def save_item(item):
    item_id = item["id"]
    filename = "data/items/%s.json" % item_id
    with codecs.open(filename, "w", "utf-8") as f:
        f.write(json.dumps(item, indent = 4, ensure_ascii=False))

if __name__ == '__main__':
    max_page_num = len(items())//100 + 1
    print("max_page_num is {}".format(max_page_num))

    for i in items():
        print(i["title"])
        save_item(i)
