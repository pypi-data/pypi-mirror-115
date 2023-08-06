#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

from sys import version_info
from aiohttp import ClientTimeout
from datetime import timedelta, date
from urllib.parse import urljoin
import logging
import math , json , time
import requests
import urllib3
urllib3.disable_warnings()

MIN_PYTHON_VERSION = (3, 5, 3)

_ = version_info >= MIN_PYTHON_VERSION or exit(
    "Python %d.%d.%d required" % MIN_PYTHON_VERSION
)

__version__ = "1.0.1"

_LOGGER = logging.getLogger(__name__)

# Base url to Eliq Online API
BASE_URL = "https://my.eliq.io/api/"

# Date format for url
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

TIMEOUT = timedelta(seconds=30)


class API:
    """ API class for EVN Online API  """

    INTERVAL_6MIN = "6min"
    INTERVAL_DAY = "day"

    def __init__(self, name=None, pw=None):
        self._session = requests.Session()
        self.name = name
        self.pw = pw

    def _request_data(self, makh='PE04000011867'):
        #session = requests.Session()
        headers = {
          'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Referer': 'https://cskh.evnhcmc.vn/Taikhoan/lienKetDiemDungDien',
          'X-Requested-With': 'XMLHttpRequest',
          'sec-ch-ua-mobile': '?0',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        data = {
          'u': self.name,
          'p': self.pw,
          'remember': '1',
          'token': ''
        }
        response = self._session.post('https://cskh.evnhcmc.vn/Dangnhap/checkLG', headers=headers, data=data, verify=False).text

        time.sleep(1)

        data = {
          'token': '',
          'input_makh': makh,
          'input_tungay': '04/08/2021',
          'input_denngay': '05/08/2021'
        }
        response = self._session.post('https://cskh.evnhcmc.vn/Tracuu/ajax_dienNangTieuThuTheoNgay',  data=data, verify=False).text
        #print(response)
        time.sleep(1)
        rsp = json.loads(response)
        state = rsp['state']
        datavn = rsp['data']
        sanluong_tungngay = datavn['sanluong_tungngay']
        datajson = {
          'state':state,
          'soNgay':datavn['soNgay'],
          'tieude':datavn['tieude'],
          'ngay': sanluong_tungngay[0]['ngay'],
          'sanluong_tong':sanluong_tungngay[0]['sanluong_tong'],
          'tong_p_giao':sanluong_tungngay[0]['tong_p_giao']
        }
        #print(datajson)

        return datajson

    def get_evn_hcm(self, makhx='PE04000011867'):
        return self._request_data(makhx='PE04000011867')
