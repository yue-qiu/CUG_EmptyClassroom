#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import hashlib
import logging
import json
from pyDes import triple_des, CBC, PAD_PKCS5
from fake_useragent import UserAgent

logging.basicConfig(level=logging.ERROR,
                    filename='logging.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
UA = UserAgent()


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
    s.headers.update({'User-Agent': str(UA.random)})

    try:
        res = s.get('http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2F', timeout=1000)
    except Exception as e:
        logger.error(e)
        print('Failure. Please check logging.log')
        exit(1)

    if '错误' in res.text and 'sfrz' in res.url:
        logger.error("账号密码错误")
        print('Failure. Please check logging.log')
        exit(1)

    elif '身份验证失败' in res.text and 'ssoserver' in res.url:
        logger.error("学校SSO系统故障")
        print('Failure. Please check logging.log')
        exit(1)
    res = s.post('http://xyfw.cug.edu.cn/tp_up/up/calendar/getTeachWeekInfo', timeout=1000)
    data = json.loads(res.text)
    return data['ZC']  # str
