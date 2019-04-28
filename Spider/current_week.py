#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import logging
from random import choice
import datetime
import pymysql
import json
from pyDes import triple_des, CBC, PAD_PKCS5

def __get_headers():
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko)'
                          ' Chrome/14.0.835.163 Safari/535.1'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko)'
                          ' Version/5.1 Safari/534.50'
        },
        {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2;'
                          ' .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;'
                          ' InfoPath.3; .NET4.0C; .NET4.0E)'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko)'
                          ' Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'
        },
        {
            'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us)'
                          ' AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
        },
        {
            'User-Agent': 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko)'
                          ' Version/6.0.0.337 Mobile Safari/534.1+'
        },
        {
            'User-Agent': 'User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91)'
                          ' AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50'
                          ' (KHTML, like Gecko) Version/5.1 Safari/534.50 '
        },
    ]

    return choice(headers)

def get_current_week(username, password):
    s = requests.session()
    key = b'neusofteducationplatform'
    iv = '01234567'
    k = triple_des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    student_no_encrypt = k.encrypt(username).hex()
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    password_encrypt = md5.hexdigest().upper()
    s.headers.update(
        {
            'source': 'neumobile',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'xyfw.cug.edu.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Mobile/15E302',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Language': 'zh-cn',
            'id_number': student_no_encrypt,
            'enp': password_encrypt
        }
    )
    # 伪装 UA
    s.headers.update(__get_headers())

    try:
        res = s.get('http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2F', timeout=1000)
    except Exception as e:
        logger.error(e)
        print('Failure. Please check logging.log')
        exit(1)

    if '错误' in res.text and 'sfrz' in res.url:
        logging.error("账号密码错误")
        print('Failure. Please check logging.log')
        exit(1)

    elif '身份验证失败' in res.text and 'ssoserver' in res.url:
        logger.error("学校SSO系统故障")
        print('Failure. Please check logging.log')
        exit(1)
    res=s.post('http://xyfw.cug.edu.cn/tp_up/up/calendar/getTeachWeekInfo', timeout=1000)
    data=json.loads(res.text)
    return data['ZC'] # str
