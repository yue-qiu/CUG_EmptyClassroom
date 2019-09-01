import time
import requests
import hashlib
from random import choice
import datetime
from pyDes import triple_des, CBC, PAD_PKCS5
from Spider import current_week
from Log import logger
import Modle
import threading
import Config
import traceback
from fake_useragent import UserAgent


class EmptyClassroomSpider:
    def __init__(self):
        self.username = Config.account.get("username")
        self.password = Config.account.get("password")
        self.start_week = Config.week.get("start")
        self.end_week = Config.week.get("end")
        if self.start_week is None or self.end_week is None:
            self.start_week = int(current_week.get_current_week(self.username, self.password))
            self.end_week = self.start_week
        else:
            self.start_week = int(self.start_week)
            self.end_week = int(self.end_week)
        print(self.start_week)
        print(self.end_week)
        self.login_url = "http://202.114.207.126/sso/driotlogin"
        self.login_classroom_system_url = "http://202.114.207.126/jwglxt/cdjy/cdjy_cxKxcdlb.html?" \
                                          "gnmkdm=N2155&layout=default&su=20171000737 "
        self.get_empty_classroom_url = "http://202.114.207.126/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155"
        self.session = requests.session()
        self.Lock = threading.Lock()
        self.UA = UserAgent()
        self.session_list = {
                    '1,2': '3',
                    '3,4': '12',
                    '5,6': '48',
                    '7,8': '192',
                    '9,10': '768',
                    '11,12': '3072',
                    '上午': '15',
                    '下午': '240',
                    '晚上': '3840',
                    '白天': '255',
                    '整天': '4095',
        }

    def log_in(self):
        global res
        key = b'neusofteducationplatform'
        iv = '01234567'
        k = triple_des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        student_no_encrypt = k.encrypt(self.username).hex()
        md5 = hashlib.md5()
        md5.update(self.password.encode('utf-8'))
        password_encrypt = md5.hexdigest().upper()
        self.session.headers.update(
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
        self.session.headers.update({'User-Agent': str(self.UA.random)})

        try:
            res = self.session.get(self.login_url, timeout=1000)
        except Exception as e:
            logger.error(e, str(traceback.format_exc()))
            print('Failure. Please check logging.log')
            exit(1)

        if '错误' in res.text and 'sfrz' in res.url:
            logger.error("{} 的账号密码错误".format(self.username))
            print('Failure. Please check logging.log')
            exit(1)

        elif '身份验证失败' in res.text and 'ssoserver' in res.url:
            logger.error("学校SSO系统故障")
            print('Failure. Please check logging.log')
            exit(1)

        try:
            self.session.get(self.login_classroom_system_url, timeout=1000)
        except Exception as e:
            logger.error(e, str(traceback.format_exc()))
            print('Failure. Please check logging.log')
            exit(1)

        return True

    def get_empty_classroom(self, week, day, session):
        global r
        codes = {
            '综合楼': '13',
            '教三楼': '05',
            '教一楼': '06',
            '教二楼': '04',
            '东教楼': '15',
            '公共教学楼二': '22',
            '公共教学楼一': '21',

        }
        old_campus_buildings = ['综合楼', '教三楼', '教二楼', '教一楼', '东教楼']
        new_campus_buildings = ['公共教学楼一', '公共教学楼二']

        result = {}
        buildings = (old_campus_buildings if Config.basicInfo.get("xqh_id") == '1' else new_campus_buildings)
        # 对每栋楼进行抓取
        for building in buildings:
            result[building] = []
            data = EmptyClassroomSpider.get_data(week, day, session, codes.get(building))

            try:
                self.session.headers.update({'User-Agent': str(self.UA.random)})
                r = self.session.post(data=data, url=self.get_empty_classroom_url, timeout=1000)
            except Exception as e:
                logger.error(e, str(traceback.format_exc()))
                print('Failure. Please check logging.log')
                exit(1)

            if '用户登录' in r.text:
                logger.error("未进行单点登录")
                print('Failure. Please check logging.log')
                exit(1)

            res = r.json()
            for item in res.get('items'):
                if building != "综合楼":
                    result[building].append(
                        item.get('cdmc').replace(building, "").replace('公教1-', "").replace('公教2-', ""))
                else:
                    result[building].append(item.get('cdmc').replace("北综楼", ""))

        return result

    def run(self):
        thread_pool = []
        self.log_in()
        db = Modle.get_db()
        cur = db.cursor()

        # del_table_sql = """drop table if exists empty_classroom"""

        create_table_sql = """
        create table if not exists empty_classroom (
        id int unsigned primary key auto_increment,
        date date not null,
        campus tinyint not null ,
        day int,
        week int,
        session varchar(50),
        data longtext,
        updated_at datetime)
        """

        try:
            # cur.execute(del_table_sql)
            cur.execute(create_table_sql)
        except Exception as e:
            logger.error(e, str(traceback.format_exc()))
            print('Failure. Please check logging.log')
            exit(1)

        date = datetime.datetime.today() + datetime.timedelta(days=1)
        print("working... Just be patient~")
        for week in range(self.start_week, self.end_week + 1):
            if week == self.start_week:
                days = date.weekday()
                date = date + datetime.timedelta(days=-1)
            else:
                days = 0
            for day in range(days, 7):
                date = date + datetime.timedelta(days=1)
                for session in self.session_list:
                    # 降低速度防止被封
                    time.sleep(0.5)
                    th = threading.Thread(target=self._store_data, args=(week, day, date, session,))
                    thread_pool.append(th)
                    th.start()

        for t in thread_pool:
            t.join()
        print('Succeed!')

    @staticmethod
    def get_data(week, day, session, code):
        data = {
            'fwzt': 'cx',
            'xqh_id': Config.basicInfo.get("xqh_id"),
            'xnm': Config.basicInfo.get("xnm"),  # 学年
            'xqm': Config.basicInfo.get("xqm"),  # 学期，上学期3， 下学期12
            'zcd': pow(2, week - 1),  # 周数, 2^(n-1)
            'xqj': day,  # 星期。2表示星期二
            'jcd': session,  # 课程。第一节为1，第二节为2，第三节为4，第四节为8，第五节为16，以此类推。如3则代表1+2,即第一节与第二节
            'lh': code,
            'jyfs': 0,
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': 100,
            'queryModel.currentPage': 1,
            'queryModel.sortName': 'cdbh',
            'queryModel.sortOrder': 'asc',
            'time': 1,
            "cdlb_id": "006",
        }
        return data

    def _store_data(self, week, day, date, session):
        db = Modle.get_db()
        if db is None:
            print("Error, please check the log")
            return

        cur = db.cursor()
        if cur is None:
            print("Error, please check the log")
            return

        data = self.get_empty_classroom(week, day + 1, self.session_list.get(session))
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_sql = """
           insert into `empty_classroom`(`date`, `week`, `day`, `session`, `data`, `updated_at`, `campus`) values 
           (str_to_date('{}', '{}'), {}, {}, '{}', '{}', '{}', '{}')
           """.format(date.strftime('%Y-%m-%d'),
                      '%Y-%m-%d',
                      week,
                      day,
                      session,
                      str(data).replace("\'", "\"", -1),
                      now,
                      Config.basicInfo.get("xqh_id"))

        try:
            with self.Lock:
                cur.execute(insert_sql)
                db.commit()
        except Exception as e:
            logger.error(e)
            print('A failure happened. Please check logging.log')
            db.rollback()


