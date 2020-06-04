# coding:utf-8
__author__ = 'GaoRong'
import logging
import logging.handlers
from cf import config as cf


class log(object):
    def __init__(self):
        self.logname = "mylog"

    def setMSG(self, level, msg):
        logger = logging.getLogger()
        fh = logging.FileHandler(cf.log_path)
        ch = logging.StreamHandler()
        formater = logging.Formatter("%(asctime)s %(levelname)s %(message)s ")
        fh.setFormatter(formater)
        ch.setFormatter(formater)
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        if level == 'debug':
            logger.debug(msg)
        elif level == 'info':
            logger.info(msg)
        elif level == 'warning':
            logger.warning(msg)
        elif level == 'error':
            logger.error(msg)
        logger.removeHandler(fh)
        logger.removeHandler(ch)
        fh.close()

    def debug(self, msg):
        self.setMSG('debug', msg)

    def info(self, msg):
        self.setMSG('info', msg)

    def warning(self, msg):
        self.setMSG('warning', msg)

    def error(self, msg):
        self.setMSG('error', msg)
