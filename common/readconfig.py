#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/10/12 5:05 下午
# @Author  : roger
# @File    : readconfig.py

import os
import pathlib

curPath = os.path.dirname(os.path.dirname(__file__))
path = curPath + "/common/requirements.txt"

try:
    import configparser
except ImportError:
    os.system(f"pip3 install -r {path}")
    import configparser

cf = configparser.ConfigParser()
filepath = os.path.dirname(os.path.dirname(__file__))  # 获取当前git仓库的根目录
file = filepath + "/config.ini"
path = pathlib.Path(file)
r = path.is_file()
if r:
    configfile = os.path.join(filepath, 'config.ini')  # config.ini 默认写在根目录
else:
    configfile = 'config.ini'
cf.read(configfile)


class ReadConfig(object):
    def get_ext(self):
        return cf.get("config", "ext")

    def get_task_id(self):
        return cf.get("config", "taskid")

    def get_package_name(self):
        return cf.get("config", "package_name")

    def get_udid(self):
        return cf.get("config", "udid")

    def get_config(self):
        return cf.items("config")


if __name__ == "__main__":
    c = ReadConfig()
    print(c.get_ext())
