# -*- coding: utf-8 -*-
import sys
import time
from os.path import dirname, abspath
import requests, datetime
import pandas as pd
import numpy as np
import json
from com import *
'''Date: 2021.03.15'''


def total_handle_req(body, URL):
    response = requests.request(
        method='POST',
        url=URL,
        headers={'Content-Type': 'application/json'},
        params=None,
        data=json.dumps(body),
    )
    resp_data = response.json()
    resp_status = resp_data['success']

    if resp_status is False:
        return pd.DataFrame()
    try:
        _df_ = pd.DataFrame(resp_data['body']['data'])
    except:
        _df_ = (resp_data['body'])

    return _df_

def handle_hist_data_req_pages(body, URL):
    # 历史行情数据
    response = requests.request(
        method='POST',
        url=URL,
        headers={'Content-Type': 'application/json'},
        params=None,
        data=json.dumps(body),
    )
    try:
        resp_data = response.json()
        resp_status = resp_data['success']

        if resp_status is False:
            return pd.DataFrame()
        try:
            pages = resp_data['body']['pages']
            return pages
        except:
            ret = resp_data['body']
            return ret
    except Exception as exp:
        return '您好, 您填入的参数有误(response.status:{}), 请检查后重新请求!'.format(response.status_code)

def total_handle_hist_data_req(body, URL):
    response = requests.request(
        method='POST',
        url=URL,
        headers={'Content-Type': 'application/json'},
        params=None,
        data=json.dumps(body),
    )
    resp_data = response.json()
    resp_status = resp_data['success']

    if resp_status is False:
        return pd.DataFrame()
    try:
        __ = resp_data['body']['records']
        return __
    except:
        ret = resp_data['body']
        return ret

def change_timestamp(ts):
    # change ts
    ts = int(str(ts)[:10])
    timeArray = time.localtime(int(ts))
    _date_ = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return _date_

def t_typeof(variate):
    '''
    返回变量的类型
    '''

    type = None
    if isinstance(variate, int):
        type = "int"
    elif isinstance(variate, str):
        type = "str"
    elif isinstance(variate, float):
        type = "float"
    elif isinstance(variate, list):
        type = "list"
    elif isinstance(variate, tuple):
        type = "tuple"
    elif isinstance(variate, dict):
        type = "dict"
    elif isinstance(variate, set):
        type = "set"
    return type