import pymysql
from Config import db_config
from Log import logger
import threading

conn = None
lock = threading.Lock()


def get_db():
    global conn

    if conn is None:
        with lock:
            if conn is None:
                try:
                    conn = pymysql.connect(db_config.get("host"),
                                           db_config.get("username"),
                                           db_config.get("password"),
                                           db_config.get("database"))
                except Exception as e:
                    logger.error("fail to connect to the database: {}".format(e))
                    return None
    return conn


__all__ = ["get_db"]
