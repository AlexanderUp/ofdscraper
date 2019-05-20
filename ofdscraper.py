# encoding:utf-8
# scraper for ofd providing detailed information about purchases

from bs4 import BeautifulSoup

import requests
import datetime
import time
import re
import pprint

from ofdscraper_config import URL
from ofdscraper_config import HEADERS
from ofdscraper_config import DICT_UTF


PATTERN = r'{multiline:true,value:\'(?P<item>.*)\'}'
PATTERN2 = r'\\u\w{4}'


class OfdScraper():

    def __init__(self, url=URL):
        self.session = requests.Session()
        self.req = self.session.get(url, headers=HEADERS)
        print('Status code: {}'.format(self.req.status_code))
        # print('Source code: {}'.format(self.req.text))
        self.bsObj = BeautifulSoup(self.req.text, features='lxml')
        print('***** Initialized! ******')
        self.items_purchased = []
        return None

    def _parse_page(self):
        candidates = self.bsObj.findAll('script', {'class':'z-runonce'})
        candidates = [candidate.get_text().strip('\n') for candidate in candidates]
        p = re.compile(PATTERN)
        for candidate in candidates:
            if candidate.startswith('zk.pi=1;zkmx('):
                items = p.findall(candidate)
        for item in items:
            self.items_purchased.append(self._normalize_string(self._translate(item)))
        return None

    def _translate(self, word):
        p = re.compile(PATTERN2) # to be shifted to outer scope of view
        return p.sub(self._substitute, word)

    def _substitute(self, m):
        return DICT_UTF.get(m.group(0).lower()[-5:])

    def _normalize_string(self, s):
        s = s.replace('\\n', ' => ')
        s = s.replace('\\', '')
        return s


if __name__ == '__main__':
    print('*' * 125)
    print('Script was ran on {} at {}'.format(datetime.date.today(), datetime.datetime.fromtimestamp(time.time())))
    scraper = OfdScraper()
    scraper._parse_page()
    pprint.pprint(scraper.items_purchased, width=250)
