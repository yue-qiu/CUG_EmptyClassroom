import os
import configparser

__all__ = ['db_config', 'account', 'week']


cfg = configparser.ConfigParser()
cfg.read(os.path.join('Config', 'Config.ini'))

account = {'username': cfg.get('account', 'username'),
           'password': cfg.get('account', 'password'),
           }

db_config = {'host': cfg.get('db', 'host'),
             'username': cfg.get('db', 'username'),
             'password': cfg.get('db', 'password'),
             'database': cfg.get('db', 'database'),
             }

if cfg.has_option('week', 'start') and cfg.has_option('week', 'end'): # 存在字段则填充否则交由爬虫自己按当前周填充
    start = cfg.get('week', 'start')
    end = cfg.get('week', 'end')
else:
    start = None
    end = None

week = {'start': start,
        'end': end,
        }
