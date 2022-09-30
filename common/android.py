#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 3:48 下午
# @Author  : roger
# @File    : adb.py

__author__ = "neallyl"

import os, sys

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)

from common.lib import *

auto_setup(__file__)


class Android(object):
    @property
    def get_rotation_status(self):
        """
        功能描述：实时获取手机横竖屏状态
        适用范围：Android
        :return: 返回横竖屏状态
        """
        cur_width, cur_height = self.get_cur_resolution
        if cur_width < cur_height:
            return 1  # 竖屏
        else:
            return 2  # 横屏

    @property
    def get_cur_resolution(self):
        """
        功能描述：实时获取当前屏幕分辨率
        适用范围：Android
        :return: 返回当前屏幕分辨率
        """
        cmd = "dumpsys window displays|grep 'cur='"
        result = G.DEVICE.shell(cmd)
        print_log(f"分辨率信息：{result}", screenshot=False)
        target = result.strip().split(" ")[2].split("=")[1].split("x")
        cur_width = int(target[0])
        cur_height = int(target[1])
        return cur_width, cur_height

    def check_if_front(self, pkg):
        """
        功能描述：判断app是否在前台
        适用范围：Android
        :param pkg: 包名
        :return: 状态
        """
        cmd = "dumpsys window | grep mCurrentFocus"
        try:
            result = G.DEVICE.shell(cmd)
            print_log(f"当前前台进程：{result}")
            if pkg in result:
                return True
            else:
                return False
        except:
            return False

    def forbid_autoratate(self):
        """
         功能描述：禁止自动旋转屏幕。部分厂商屏蔽了该命令
         适用范围：Android
         """
        cmd = f"content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0"
        G.DEVICE.shell(cmd)
        sleep(1.0)

    def set_portrait(self):
        """
        功能描述：adb命令强行竖屏。并不是所有Android设备都生效
        适用范围：Android
        """
        cmd = f"content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:0"
        G.DEVICE.shell(cmd)
        sleep(1.0)

    def fold_notification(self, pkg):
        """
        功能描述：判断测试应用当前不在前台，怀疑打开了通知栏，尝试关闭
        适用平台：Android
        """
        if not self.check_if_front(pkg):
            swipe(down, up)
        else:
            pass

    @property
    def get_default_input(self):
        """
        功能描述：获取默认输入法。
        适用范围：Android
        :return: 默认输入法
        """
        cmd = "settings get secure default_input_method"
        return G.DEVICE.shell(cmd)

    @logwrap
    def adb_touch(self, x, y):
        """
        功能说明：adb命令点击屏幕

        适用范围：Android

        :param x: 横坐标
        :param y: 纵坐标
        :return: 点击目标坐标
        """
        show_screen()
        cmd = f"input tap {x} {y}"
        G.DEVICE.shell(cmd)
        sleep(1.0)

    def adb_touch_pos(self, pos):
        """
        功能描述：adb点击相对坐标
        适用范围：Android
        :param pos: 相对坐标
        :return: None
        """
        width, height = self.get_cur_resolution
        x = pos[0] * width
        y = pos[1] * height
        print_log(f"分辨率为:{width}x{height}，点击位置为：{x}x{y}", screenshot=False)
        self.adb_touch(x, y)
        sleep(1.0)

    def adb_touch_attrs(self, **kwargs):
        """
        功能描述：poco查找控件位置，adb touch点击。规避poco点击失败的问题
        适用范围：Android
        :param kwargs: 目标控件
        :return:None
        """
        pos = poco(**kwargs).get_position()
        print_log(f"{kwargs}相对坐标为：{pos}")
        self.adb_touch_pos(pos)

    @property
    def get_device_name(self):
        """
        功能描述：获取设备名称
        适用范围：Android
        :return: 返回设备名称
        """
        rs = ""
        if platform == 'Android':
            cmd = "getprop ro.product.model"
            rs = G.DEVICE.shell(cmd).strip()
        elif platform == 'IOS':
            rs = G.DEVICE.device_status()['os']['name']
        print_log(f"设备名为：{rs}", screenshot=False)
        return rs

    def back_click(self, x, y):
        """
        功能描述：后台点击。用于部分需要快速点击的场景
        适用范围：Android
        :param x: 点击的x坐标
        :param y: 点击的y坐标
        :return: None
        """
        # 定义子线程: 循环查找目标元素
        t = threading.Thread(target=self.adb_touch, name='BackClickThread', args=(x, y))
        # 增加守护线程，主线程结束，子线程也结束
        t.setDaemon(True)
        t.start()

    def get_meminfo(self):
        """
        功能描述：获取Android设备可用内存信息

        适用范围：Android

        :return: None
        """
        if platform == 'Android':
            cmd = "cat /proc/meminfo | grep 'Mem'"
            try:
                rs = G.DEVICE.shell(cmd)
                print_log(f"{rs}", screenshot=False)
            except:
                print_log(f"获取内存信息失败")

    def get_storageinfo(self):
        """
        功能描述：获取Android设备存储信息

        适用范围：Android

        :return: None
        """
        if platform == 'Android':
            cmd = "df"
            try:
                rs = G.DEVICE.shell(cmd)
                print_log(f"{rs}", screenshot=False)
            except:
                print_log(f"获取存储信息失败")

    def check_network(self):
        """
        功能描述：校验Android设备网络联通性
        适用范围：Android
        return：None
        """

        class NoNetWorkErr(Exception):
            def __init__(self, msg):
                self.msg = msg

            def __str__(self):
                print_log(self.msg)

        if platform == "Android":
            print_log(f"开始网络诊断")
            try:
                cmd = "ping -c 5 www.baidu.com"
                shell(cmd)
                print_log(f"网络校验通过")
            except Exception:
                raise NoNetWorkErr("当前设备无网络")

    def swipe_adb(self, v1, v2):
        """
        功能描述：适用adb 滑动界面
        适用范围：Android
        return：None
        """
        cmd = f"input swipe {v1[0]} {v1[1]} {v2[0]} {v2[1]}"
        print_log(f"开始滑动：{v1} -> {v2}")
        shell(cmd)
