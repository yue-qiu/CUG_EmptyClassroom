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

week = {'start': cfg.get('week', 'start'),
        'end': cfg.get('week', 'end'),
        }



