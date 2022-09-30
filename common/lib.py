#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 5:01 下午
# @Author  : roger
# @File    : lib.py

__author__ = "neallyl"

import shutil
import threading

import wda
from airtest.core.api import *
from airtest.core.cv import try_log_screen
from airtest.core.helper import logwrap
from airtest.aircv import cv2_2_pil, aircv
from urllib import parse

from common.readconfig import ReadConfig

readconfig = ReadConfig()

import os, sys, datetime
import json

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)


platform = G.DEVICE.__class__.__name__
if platform == 'Android':
    from poco.drivers.android.uiautomation import AndroidUiautomationPoco

    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)
elif platform == 'IOS':
    c = wda.Client(G.DEVICE.addr)
    from poco.drivers.ios import iosPoco

    poco = iosPoco()

width, height = G.DEVICE.get_current_resolution()
up = (width * 0.5, height * 0.2)
down = (width * 0.5, height * 0.8)
left = (width * 0.2, height * 0.5)
right = (width * 0.8, height * 0.5)
center = (width * 0.5, height * 0.5)

from common.utils.pathutil import get_project_root

pic_filepath = os.path.join(get_project_root(), "pic")

ERROR_TYPE = ["AssertionError", "airtest.core.error", "UIObjectProxy",
              "poco.exceptions", "NameError", "AttributeError", "TargetNotFoundError"]
UPLOAD_RELEASE_API = "https://xy.alibaba-inc.com/web_api/base/save_ui_automation_result/?back_door=NDI2j9DKNF71Vv"
UPLOAD_MONKEY_API = "https://xy.alibaba-inc.com/web_api/base/save_monkey_automation_result/?back_door=NDI2j9DKNF71Vv"
auto_setup(__file__)


@logwrap
def show_screen(msg=None):
    """
    功能描述：在报告中显示截图

    适用范围：Android，iOS

    :return: None
    """
    if msg is not None:
        print(msg)
    try:
        try_log_screen()
    except:
        print_log(f"获取截图失败", screenshot=False)


@logwrap
def print_log(msg, screenshot=True):
    """
    功能描述：封装本地print和报告的日志
    适用范围：Android，IOS
    :param msg: 打印内容
    :return: None
    """
    print(msg)
    if screenshot:
        show_screen()


def get_irma_ext():
    switch = readconfig.get_ext()
    return switch


def get_irma_task_id():
    task_id = readconfig.get_task_id()
    return task_id


def get_irma_config():
    config = readconfig.get_config()
    return config


def get_irma_pkg_name():
    pkg_name = readconfig.get_package_name()
    return pkg_name


def get_irma_udid():
    udid = readconfig.get_udid()
    return udid


def get_testcase(path):
    """
    功能描述：获取用例名称
    适用范围：Android,IOS
    :param path: 用例绝对路径
    :return: 用例文件名
    """
    cur_path = os.path.split(path)[0]
    last_path, filename = os.path.split(cur_path)
    dir = os.path.basename(last_path)
    return dir, filename


def get_orientation_size():
    """
    功能描述：获取当前屏幕是否横屏，返回宽度和高度
    适用范围：Android，IOS
    :return: 当前屏幕是否横屏，返回宽度和高度
    """
    display_info = G.DEVICE.display_info
    width = 0
    height = 0
    # 是否横屏
    is_horizonal = 0
    if platform == 'Android':
        if display_info.get('orientation') in [1, 3]:
            width = display_info.get('height')
            height = display_info.get('width')
            is_horizonal = 1
        else:
            width = display_info.get('width')
            height = display_info.get('height')
    else:
        if display_info.get('orientation') == 'LANDSCAPE':
            width = display_info.get('height')
            height = display_info.get('width')
            is_horizonal = 1
        else:
            width = display_info.get('width')
            height = display_info.get('height')
    return is_horizonal, width, height


def get_ios_monkey_url(pkg):
    """
    功能描述：获取IOS运行monkey的指令。仅在Irma生效
    适用范围：IOS
    :param pkg: bundle_id
    :return: 启动和结束monkey的指令
    """
    start_url = f"wda/monkey/start?bundleID={pkg}"
    stop_url = f"wda/monkey/stop?bundleID={pkg}"
    # G.DEVICE.stop_app(self.pkg)
    return start_url, stop_url


def exists_imgs(pic):
    """
    功能描述：判断图片是否存在，用于兼容多分辨率设备的图像识别失败的问题。

    适用范围：Android，IOS

    :param pic: 图片列表
    :return:
    """
    if isinstance(pic, list):
        for item in pic:
            if exists(item):
                return True
            else:
                continue
        return False
    else:
        return False


def upload_result(api, param):
    import requests
    response = requests.request("POST", api, data=param)

    print(response.text)
