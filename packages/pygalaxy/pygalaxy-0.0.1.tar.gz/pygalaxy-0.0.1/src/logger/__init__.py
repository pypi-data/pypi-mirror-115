#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import datetime


def get_current_date():
    t = datetime.datetime.now()
    t1 = datetime.datetime.strftime(t, '%Y-%m-%d')
    return t1


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_directory_path = project_dir + '/logs'
if not os.path.exists(log_directory_path):
    os.makedirs(log_directory_path)
log_file = (str(log_directory_path) + '/' + get_current_date() + '.log')

# 创建文件和命令行的handler
s_handler = logging.StreamHandler()
f_handler = logging.FileHandler(log_file)
# 分别设置两个handler的日志等级，大于等于这个等级的才输出
s_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)
# 设置日志的输出格式并把格式添加到handler中
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_handler.setFormatter(formatter)
f_handler.setFormatter(formatter)
# 把handler添加到logger对象中
logger.addHandler(f_handler)
logger.addHandler(s_handler)


def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


if __name__ == '__main__':
    debug('logging')
