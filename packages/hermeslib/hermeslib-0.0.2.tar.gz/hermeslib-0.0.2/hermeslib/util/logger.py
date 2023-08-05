# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 12:47
# @Author  : keheng
# @version ：python 3.6.8
# @File    : logger.py

import os
import logging
from logging import handlers

from ..config import config
from ..util.common import get_current_time_str

ROOT_PATH = config.ROOT_PATH


class SetLogModel:
    """
    设置日志格式
    """
    WHEN = 'W0'
    BACK_COUNT = 3
    LOG_FORMAT = '[%(levelname)-5s:%(asctime)s:%(filename)-15s:%(lineno)-3d]：%(message)s'
    LOG_LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'warning': logging.WARNING, 'ERROR': logging.ERROR,
                  'critical': logging.CRITICAL}

    def __init__(self, log_mode="print", logger_id='main', log_filename="MainApp.log", level=None):
        """
        初始化设置日志格式
        :param log_mode: 日志记录模式 print为控制台输出， file为文件记录日志，默认控制台输出
        :param levels: 需要进行记录的日志等级，默认为 'INFO'
                       级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
        """

        if level is None:
            level = 'DEBUG'
        # 创建一个logger
        self.logger = logging.getLogger(logger_id)
        # 统一日志的输出格式
        self.formatter = logging.Formatter(SetLogModel.LOG_FORMAT)
        # 添加日志handler
        if 'file' == log_mode:
            filename = os.path.join(ROOT_PATH, 'logs', log_filename)
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            # 定时拆分日志
            handler = handlers.TimedRotatingFileHandler(filename=filename, when=SetLogModel.WHEN,
                                                        backupCount=SetLogModel.BACK_COUNT, encoding='utf-8')
            # handler = logging.FileHandler(filename, "a", encoding="UTF-8")
        else:
            # 如果设置了日志级别为NOTSET将记录所有级别日志
            # logging.basicConfig(level=logging.NOTSET)
            handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(SetLogModel.LOG_LEVELS.get(level))

    def get_logger(self, level='info'):
        """
        回调函数，返回实例
        :return: logger实例
        """
        if level not in ['debug', 'info', 'warning', 'error', 'critical']:
            raise ValueError(f'Unexpected level value : {level}')
        return self.__getattribute__(level)

    def debug(self, msg):
        return self.logger.debug(msg)

    def info(self, msg):
        return self.logger.info(msg)

    def warning(self, msg):
        return self.logger.warning(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def critical(self, msg):
        return self.logger.critical(msg)


logger = SetLogModel(config.LOG_MODE, 'hermes', 'run.log')


def record_log(log_str, is_print=False, in_file=False, level='info'):
    if is_print:
        print(log_str)
    if in_file:
        logger.get_logger(level)(log_str)
    return


def record_api_log(log_str, is_print=config.API_IS_PRINT, in_file=config.API_IN_FILE, level='info'):
    log_str = get_current_time_str('%Y-%m-%d %H:%M:%S.%f') + " : " + log_str
    return record_log(log_str, is_print, in_file, level)
