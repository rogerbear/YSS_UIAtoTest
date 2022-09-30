#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 6:13 下午
# @Author  : roger
# @File    : device.py

__author__ = "neallyl"

import os, sys

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)

from common.lib import *
from common.android import Android
from common.ios import IOS

ios = IOS()
android = Android()

auto_setup(__file__)


class Device(object):
    def __init__(self):
        pass

    @property
    def get_os_version(self):
        """
        功能描述：获取系统版本
        适用范围：Android,IOS
        :return: sdk version
        """
        if platform == 'Android':
            cmd = "getprop ro.build.version.sdk"
            try:
                rs = int(G.DEVICE.shell(cmd))
                print_log(f"sdk:{rs}", screenshot=False)
            except:
                print_log(f"系统固件版本获取失败")
        elif platform == 'IOS':
            rs = G.DEVICE.device_status()['os']['version']
        return rs

    def get_orientation_size(self):
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

    def back(self):
        """
        功能描述：Android点击返回硬件；IOS右滑返回
        适用范围：Android，IOS
        :return: None
        """
        if platform == 'Android':
            keyevent("BACK")
        elif platform == 'IOS':
            ios.s.swipe_right()

    def tap_click(self, **kwargs):
        """
        功能描述：封装tap源生点击
        适用平台：Android,IOS
        :param kwargs:
        :return:
        """
        if platform == 'Android':
            android.adb_touch_attrs(**kwargs)
        elif platform == 'IOS':
            ios.wda_click(**kwargs)

    def tap_click_pos(self, **kwargs):
        """
        功能描述：封装tap源生点击
        适用平台：Android,IOS
        :param kwargs:
        :return:
        """
        if platform == 'Android':
            pos = poco(**kwargs).get_position()
            print_log(f"{kwargs}坐标为：{pos}")
            android.adb_touch_pos(pos)
        else:
            ios.wda_click_pos(**kwargs)

    def get_devices_serialno(self,idx):
        if G.DEVICE_LIST:
            return G.DEVICE_LIST[idx].serialno
        return 0

    def get_app_version_name(self,pkg):
        if platform == 'Android':
            version_name = shell(f'dumpsys package {pkg} | grep versionName')
            return version_name.split('=')[1]
        return None