#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/20 5:32 下午
# @Author  : Roger
# @File    : common.py

__author__ = "neallyl"

import os
import sys

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)

from common.lib import *
from common.poco import Poco
from common.android import Android
from common.ios import IOS
from common.airtest import Airtest
from common.device import Device
from airtest.core.android.adb import ADB

poco_ui = Poco()
android = Android()
ios = IOS()
airtest = Airtest()
device = Device()

auto_setup(__file__)


class Common(object):
    def __init__(self):
        self.poco = poco
        self.platform = platform
        self.width = width
        self.height = height
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.center = center
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.task_day = datetime.date.today().strftime("%Y-%m-%d")
        self.pic_filepath = pic_filepath
        if platform == "IOS":
            self.s = c.session()
            self.w, self.h = self.s.window_size()
        if self.platform == 'Android':
            self.adb = ADB(serialno=G.DEVICE.uuid)

    @property
    def get_rotation_status(self):
        """
        功能描述：实时获取手机横竖屏状态
        适用范围：Android
        :return: 返回横竖屏状态
        """
        return android.get_rotation_status

    @property
    def get_cur_resolution(self):
        """
        功能描述：实时获取当前屏幕分辨率
        适用范围：Android
        :return: 返回当前屏幕分辨率
        """
        return android.get_cur_resolution

    def poco_click(self, focus=[0.5, 0.5], **kwargs):
        """
        功能描述：封装poco(xxx).click方法。增加找不到控件时截图.focus只在竖屏下生效
        适用范围：Android,IOS
        :param kwargs: 控件：name=xxx,text=xxx,desc=xxx...  正则模糊定位：textMatches="^.*xxx.*$"，nameMatches="^.*xxx.*$"
        :return:None
        """
        poco_ui.poco_click(focus, **kwargs)

    def poco_click_pos(self, **kwargs):
        """
        功能描述：获取控件坐标，点击具体位置。横屏下，适用adb tap点击方式
        适用范围：Android，IOS
        :param kwargs: 目标控件
        :return: None
        """
        poco_ui.poco_click_pos(**kwargs)

    def poco_click_pos_exists(self, **kwargs):
        """
        功能描述：控件存在，则点击控件坐标
        适用范围：Android , IOS
        :param kwargs: 属性控件
        :return:
        """
        poco_ui.poco_click_pos_exists(**kwargs)

    def poco_click_exists(self, **kwargs):
        """
        功能描述：控件存在，则点击控件
        适用范围：Android，IOS
        :param kwargs: 目标控件
        :return: None
        """
        poco_ui.poco_click_exists(**kwargs)

    def poco_get_text(self, **kwargs):
        """
        功能描述：获取控件的text属性

        适用范围：Android，IOS

        :param kwargs: 目标控件
        :return:
        """
        return poco_ui.poco_get_text(**kwargs)

    def poco_assert(self, msg, **kwargs):
        """
        功能描述：断言目标是否存在，同时会出发截图
        适用范围：Android，IOS
        :param msg: 断言消息
        :param kwargs: 目标控件
        :return: None
        """
        poco_ui.poco_assert(msg, **kwargs)

    def poco_mult_assert(self, msg, attr1, attr2):
        """
        功能描述：断言目标是否存在，任意一个存在，即为成功
        适用范围：Android，IOS
        :param msg:断言消息
        :param attr1:目标属性name=attr1
        :param attr2:目标属性name=attr2
        :return:None
        """
        poco_ui.poco_mult_assert(msg, attr1, attr2)

    def poco_exists(self, **kwargs):
        """
        功能描述：判断控件是否存在
        适用范围：Android，IOS
        :param kwargs: 目标控件
        :return: 返回控件存在的判断结果
        """
        return poco(**kwargs).exists()

    def poco_pos(self, pos):
        """
        功能描述：相对坐标点击。比如pos = [0.5,0.5]
        适用范围：Android，IOS
        :param pos: 目标坐标
        :return:
        """
        poco_ui.poco_pos(pos)

    def get_ios_monkey_url(self, pkg):
        """
        功能描述：获取IOS运行monkey的指令。仅在Irma生效
        适用范围：IOS
        :param pkg: bundle_id
        :return: 启动和结束monkey的指令
        """
        return get_ios_monkey_url(pkg)

    def check_if_front(self, pkg):
        """
        功能描述：判断app是否在前台
        适用范围：Android
        :param pkg: 包名
        :return: 状态
        """
        return android.check_if_front(pkg)

    def run_monkey(self, times, pkg=None):
        """
        功能描述：运行monkey
        适用范围：Android，IOS
        :param times: Android表示monkey点击次数；IOS表示运行时长
        :param pkg: 包名
        :return:None
        """
        airtest.run_monkey(times, pkg)

    def quit_app(self, pkg):
        """
        功能描述：退出app
        适用范围：Android,IOS
        :param pkg: 包名
        :return: None
        """
        airtest.quit_app(pkg)

    def forbid_autoratate(self):
        """
         功能描述：禁止自动旋转屏幕。部分厂商屏蔽了该命令
         适用范围：Android
         """
        android.forbid_autoratate()

    def set_portrait(self):
        """
        功能描述：adb命令强行竖屏。并不是所有Android设备都生效
        适用范围：Android
        """
        android.set_portrait()

    def poco_find_all(self, **kwargs):
        """
        功能描述：查询目标控件的个数。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件的个数
        """
        return poco_ui.poco_find_all(**kwargs)

    def poco_find_pos(self, target=None, **kwargs):
        """
        功能描述：查询目标控件的pos属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件pos
        """
        return poco_ui.poco_find_pos(target, **kwargs)

    def poco_find_name(self, **kwargs):
        """
        功能描述：查询目标控件的name属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件name
        """
        return poco_ui.poco_find_name(**kwargs)

    def poco_find_attrs_name(self, target=None, **kwargs):
        """
        功能描述：查询目标控件的name和pos属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件name和pos
        """
        return poco_ui.poco_find_attrs_name(target, **kwargs)

    def poco_find_attrs_text(self, **kwargs):
        """
        功能描述：查询目标控件的text和pos属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件name和pos
        """
        return poco_ui.poco_find_attrs_text(**kwargs)

    def fold_notification(self, pkg):
        """
        功能描述：判断测试应用当前不在前台，怀疑打开了通知栏，尝试关闭
        适用平台：Android
        """
        android.fold_notification(pkg)

    def poco_fuzzy_match_click(self, keyword, attrs):
        """
        功能描述：通过name属性，模糊匹配控件。匹配成功，触发点击；匹配失败，截图
        适用平台：Android,IOS
        :param keyword: name属性，模糊匹配关键词
        :param attrs: 控件属性集合
        :return: 控件位置点击
        """
        poco_ui.poco_fuzzy_match_click(keyword, attrs)

    def poco_poll_click_brother(self, **kwargs):
        """
        功能描述：轮询点击目标控件的兄弟节点
        适用范围：Android,IOS
        :param kwargs: 目标控件
        :return: None
        """
        poco_ui.poco_poll_click_brother(**kwargs)

    def poco_poll_click_attrs(self, **kwargs):
        """
        功能描述：轮询点击所有目标控件节点
        适用范围：Android,IOS
        :param kwargs:
        :return:
        """
        poco_ui.poco_poll_click_attrs(**kwargs)

    @property
    def get_os_version(self):
        """
        功能描述：获取Android sdk版本
        适用范围：Android,IOS
        :return: sdk version
        """
        return device.get_os_version

    def poco_swipe(self, posa, posb):
        """
        功能描述:封装poco的swipe函数，不选中UI
        适用范围：Android,IOS
        :param posa: 起始位置，相对坐标
        :param posb: 结束位置，相对坐标
        :return: None
        """
        poco_ui.poco_swipe(posa, posb)

    @property
    def get_default_input(self):
        """
        功能描述：获取默认输入法。
        适用范围：Android
        :return: 默认输入法
        """
        return android.get_default_input

    def touch_real_pos(self, **kwargs):
        """
        功能描述：部分机型，poco的click事件，坐标点击存在偏移。点击操作改成点击真实坐标
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 点击目标控件
        """
        return poco_ui.touch_real_pos(**kwargs)

    def wda_click(self, **kwargs):
        """
        功能描述：wda库的点击操作。若IOS的poco click未生效，可以采用此方法代替。此方法无日志，无步骤
        适用范围：IOS
        :param kwargs: 目标控件
        :return: None
        """
        ios.wda_click(**kwargs)

    def wda_click_exist(self, **kwargs):
        """
        功能描述：wda click前判断是否存在
        适用范围：IOS
        :param kwargs: 目标控件
        :return: None
        """
        ios.wda_click_exist(**kwargs)

    def wda_click_pos(self, pos):
        """
        功能描述：wda库的坐标点击操作。此方法无日志，无步骤

        注意：wda获取的屏幕大小与poco获取的分辨率不一致

        适用范围：IOS

        :param kwargs: 目标控件
        :return: None
        """
        ios.wda_click_pos(pos)

    def adb_touch(self, x, y):
        """
        功能说明：adb命令点击屏幕

        适用范围：Android

        :param x: 横坐标
        :param y: 纵坐标
        :return: 点击目标坐标
        """
        android.adb_touch(x, y)

    def adb_touch_pos(self, pos):
        """
        功能描述：adb点击相对坐标
        适用范围：Android
        :param pos: 相对坐标
        :return: None
        """
        android.adb_touch_pos(pos)

    def adb_touch_attrs(self, **kwargs):
        """
        功能描述：poco查找控件位置，adb touch点击。规避poco点击失败的问题
        适用范围：Android
        :param kwargs: 目标控件
        :return:None
        """
        android.adb_touch_attrs(**kwargs)

    @property
    def get_device_name(self):
        """
        功能描述：获取设备名称
        适用范围：Android
        :return: 返回设备名称
        """
        return android.get_device_name

    def back_click(self, x, y):
        """
        功能描述：后台点击。用于部分需要快速点击的场景
        适用范围：Android
        :param x: 点击的x坐标
        :param y: 点击的y坐标
        :return: None
        """
        # 定义子线程: 循环查找目标元素
        android.back_click(x, y)

    def find_target_pos(self, **kwargs):
        """
        功能描述：寻找符合目标要求，且x=0.5的坐标点
        适用范围：Android，IOS
        :param kwargs:目标控件
        :return:None
        """
        return poco_ui.find_target_pos(**kwargs)

    def print_log(self, msg, screenshot=True):
        """
        功能描述：封装本地print和报告的日志
        适用范围：Android，IOS
        :param msg: 打印内容
        :return: None
        """
        print_log(msg, screenshot)

    def get_testcase(self, path):
        """
        功能描述：获取用例名称
        适用范围：Android,IOS
        :param path: 用例绝对路径
        :return: 用例文件名
        """
        return get_testcase(path)

    def init_result(self, content):
        """
        功能描述：上传结果至idb

        适用范围：Android，IOS

        :param content:统计数据.content内容如下：
        (device_name,task_day,testcase,instance,rom,datetime,platform,result,status,product)

        :return:None
        """
        airtest.init_result(content)

    def insert_monkey_result(self, content):
        """
        功能描述：上传结果至idb

        适用范围：Android，IOS

        :param content:统计数据.content内容如下：
        (device_name,task_day,sences,times,rom,datetime,platform,result,product)

        :return:None
        """
        airtest.insert_monkey_result(content)

    def tap_click(self, **kwargs):
        """
        功能描述：封装tap源生点击
        适用平台：Android,IOS
        :param kwargs:
        :return:
        """
        device.tap_click(**kwargs)

    def show_screen(self, msg=None):
        """
        功能描述：在报告中显示截图

        适用范围：Android，iOS

        :return: None
        """
        show_screen(msg)

    def get_irma_ext(self):
        return get_irma_ext()

    def get_irma_task_id(self):
        return get_irma_task_id()

    def get_irma_config(self):
        return get_irma_config()

    def get_irma_pkg_name(self):
        return get_irma_pkg_name()

    def get_irma_udid(self):
        return get_irma_udid()

    def ocr_text_exist(self, text, num=0, full_match=1):
        return airtest.ocr_text_exist(text, num, full_match)

    def ocr_text_click(self, text, num=0):
        airtest.ocr_text_click(text, num)

    def ocr_text_wait(self, text, timeout, num=0, full_match=1):
        flag = True
        i = 0
        while flag:
            if not self.ocr_text_exist(text, num, full_match) == (0, 0):
                flag = False
            time.sleep(1)
            i = i + 1
            if i == timeout:
                flag = False

    def remove_pic(self):
        airtest.remove_pic()

    def get_meminfo(self):
        """
        功能描述：获取Android设备可用内存信息

        适用范围：Android

        :return: None
        """
        android.get_meminfo()

    def get_storageinfo(self):
        """
        功能描述：获取Android设备存储信息

        适用范围：Android

        :return: None
        """
        android.get_storageinfo()

    def touch_imgs(self, pic):
        """
        功能描述：多张图片，匹配点击。用于兼容多分辨率设备的图像识别失败的问题。

        适用范围：Android，IOS

        :param pic: 图片列表
        :return:
        """
        airtest.touch_imgs(pic)

    def exists_imgs(self, pic):
        """
        功能描述：判断图片是否存在，用于兼容多分辨率设备的图像识别失败的问题。

        适用范围：Android，IOS

        :param pic: 图片列表
        :return:
        """
        return exists_imgs(pic)

    def close_assistivetouch(self):
        """
        功能描述：关闭IOS的辅助触控功能

        适用范围：IOS

        :return: None
        """
        poco_ui.close_assistivetouch()

    def get_orientation_size(self):
        """
        获取当前屏幕是否横屏，返回宽度和高度
        :return:
        """
        return device.get_orientation_size()

    def save_screen_shot(self):
        """
        保存快照，路径是项目路径/pic/时间戳.png
        适用：Android、IOS
        :return:
        """
        return airtest.save_screen_shot()

    def partial_screen_shot(self, file_name=None, absolute=0, x_min=0, y_min=0, x_max=0, y_max=0):
        """
        适用：
        截图，返和图片路径，absolute指定是否是绝对坐标，默认是相对坐标，不传或全部为0则是全局截图
        :param x_min:
        :param y_min:
        :param x_max:
        :param y_max:
        :return:
        """
        return airtest.partial_screen_shot(file_name, absolute, x_min, y_min, x_max, y_max)

    def get_screen_text(self, img_file=None):
        """
        根据提供的截图路径获取截图文字，不传则截取当前整个页面快照作为识别对象
        :param img_file:
        :return:
        """
        return airtest.get_screen_text(img_file)

    def find_text_in_ocr_res(self, keyword, ocr_res):
        """
        结合get_screen_text使用，找出OCR识别结果中，是否包含要查询的关键字
        OCR识别结果格式：[{'rect': [508, 8, 693, 48], 'word': '15985135'}]
        :param text:
        :param ocr_res:
        :return:
        """
        return airtest.find_text_in_ocr_res(keyword, ocr_res)

    def back(self):
        """
        功能描述：Android点击返回硬件；IOS右滑返回
        适用范围：Android，IOS
        :return: None
        """
        device.back()

    def check_network(self):
        """
        功能描述：校验Android设备网络联通性
        适用范围：Android
        return：None
        """
        android.check_network()

    def touch_retry(self, v, times=1, **kwargs):
        """
        功能描述：touch点击重试。使用adb点击重试
        适用范围：Android,IOS
        """
        airtest.touch_retry(v, times, **kwargs)

    def swipe_adb(self, v1, v2):
        """
        功能描述：适用adb 滑动界面
        适用范围：Android
        return：None
        """
        android.swipe_adb(v1, v2)

    def text(self, keywords, is_screenshot=True, enter=False):
        """
        封装源生text，增加截图
        """
        airtest.text(keywords, is_screenshot, enter)

    def expand_notification(self):
        """
        功能描述：打开通知栏
        适用平台：Android
        """
        cmd = "cmd statusbar expand-notifications"
        shell(cmd)

    def close_notification(self):
        """
        功能描述：关闭通知栏
        适用平台：Android
        """
        cmd = "cmd statusbar collapse"
        shell(cmd)

    def click_notification(self, text):
        """
        功能描述：打开通知栏后点击指定消息
        适用平台：Android
        """
        self.expand_notification()
        for num in range(0, 10):
            if poco(text=text).exists():
                self.poco_click(text=text)
                break
            self.poco_swipe((0.5, 0.5), (0.5, 0.1))

    def check_notification(self, text):
        """
        功能描述：打开通知栏后滑动到指定消息
        适用平台：Android
        """
        self.expand_notification()
        flag = False
        for num in range(0, 5):
            if not self.ocr_text_exist(text) == (0, 0):
                flag = True
                break
            self.poco_swipe((0.5, 0.5), (0.5, 0.1))
        return flag

    def get_model(self):
        """
        功能描述：获取安卓机型
        适用平台：Android
        """
        cmd = "getprop ro.product.model"
        model = ""
        if platform == 'Android':
            model = shell(cmd).replace('\n', '')
            print(model)
        return model

    def unlock(self):
        """
        功能描述：唤醒并解锁屏幕
        适用平台：Android
        """
        if self.adb.is_locked():
            wake()
            self.adb.unlock()

    def get_app_version_name(self, pkg):
        return device.get_app_version_name(pkg)
