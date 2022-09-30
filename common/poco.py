#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 3:36 下午
# @Author  : roger
# @File    : poco.py

__author__ = "neallyl"

import os, sys

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)

from common.lib import *
from common.device import Device

device = Device()
auto_setup(__file__)


class Poco(object):
    def poco_click(self, focus=[0.5, 0.5], **kwargs):
        """
        功能描述：封装poco(xxx).click方法。增加找不到控件时截图.focus只在竖屏下生效
        适用范围：Android,IOS
        :param kwargs: 控件：name=xxx,text=xxx,desc=xxx...  正则模糊定位：textMatches="^.*xxx.*$"，nameMatches="^.*xxx.*$"
        :return:None
        """
        try:
            if platform == 'Android':
                attr1 = self.poco_find_attrs_name(touchable=True)
                poco(**kwargs).focus(focus).click()
                sleep(1)
                attr2 = self.poco_find_attrs_name(touchable=True)
                if len(attr1) == 0 or len(attr2) == 0:
                    print_log(f"获取属性树失败，不做重试")
                elif attr1 == attr2 and len(attr2) != 0 and self.poco_exists(**kwargs):
                    print_log(f"poco({kwargs}).click点击未生效，启动tap点击重试")
                    device.tap_click(**kwargs)
                else:
                    print_log(f"poco({kwargs}).click点击生效，进入下一页")
            elif platform == 'IOS':
                poco(**kwargs).focus(focus).click()
                sleep(1)
        except:
            if platform == 'Android':
                attr = self.poco_find_attrs_name(touchable=True)
                print_log(f"当前界面的可点击控件如下：{attr}")
            elif platform == 'IOS':
                attr = self.poco_find_attrs_name(type="Button")
                print_log(f"当前界面的Button如下：{attr}")
            print_log(f"{kwargs}控件不存在")
            raise

    def poco_click_pos(self, **kwargs):
        """
        功能描述：获取控件坐标，点击具体位置。横屏下，适用adb tap点击方式
        适用范围：Android，IOS
        :param kwargs: 目标控件
        :return: None
        """
        try:
            device.tap_click_pos(**kwargs)
        except:
            print_log(f"{kwargs}控件不存在")
            raise

    def poco_click_pos_exists(self, **kwargs):
        """
        功能描述：控件存在，则点击控件坐标
        适用范围：Android , IOS
        :param kwargs: 属性控件
        :return:
        """
        if self.poco_exists(**kwargs):
            self.poco_click_pos(**kwargs)
        else:
            print_log(f"{kwargs} -不存在")

    def poco_click_exists(self, **kwargs):
        """
        功能描述：控件存在，则点击控件
        适用范围：Android，IOS
        :param kwargs: 目标控件
        :return: None
        """
        if self.poco_exists(**kwargs):
            self.poco_click(**kwargs)
        else:
            print_log(f"{kwargs} -不存在")

    def poco_get_text(self, **kwargs):
        """
        功能描述：获取控件的text属性

        适用范围：Android，IOS

        :param kwargs: 目标控件
        :return:
        """
        show_screen(f"寻找控件：{kwargs}")
        return poco(**kwargs).get_text()

    def poco_assert(self, msg, **kwargs):
        """
        功能描述：断言目标是否存在，同时会出发截图
        适用范围：Android，IOS
        :param msg: 断言消息
        :param kwargs: 目标控件
        :return: None
        """
        show_screen(msg)
        if self.poco_exists(**kwargs):
            print_log(f"{kwargs}存在")
        else:
            assert_equal(self.poco_exists(**kwargs), True, msg)

    def poco_mult_assert(self, msg, attr1, attr2):
        """
        功能描述：断言目标是否存在，任意一个存在，即为成功
        适用范围：Android，IOS
        :param msg:断言消息
        :param attr1:目标属性name=attr1
        :param attr2:目标属性name=attr2
        :return:None
        """
        show_screen(msg)
        if self.poco_exists(name=attr1) or self.poco_exists(name=attr2):
            assert_equal(1, 1, msg)
        else:
            assert_equal(1, 0, msg)

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
        if platform == 'Android':
            attr1 = self.poco_find_attrs_name(touchable=True)
        elif platform == 'IOS':
            attr1 = self.poco_find_attrs_name(type="Button")
        poco.click(pos)
        sleep(1)
        if platform == 'Android':
            attr2 = self.poco_find_attrs_name(touchable=True)
        elif platform == 'IOS':
            attr2 = self.poco_find_attrs_name(type="Button")
        if len(attr1) == 0 or len(attr2) == 0:
            print_log(f"获取属性树失败，不做重试")
        elif attr1 == attr2 and len(attr2) != 0:
            print_log(f"poco.click({pos})点击未生效，重试一次")
            poco.click(pos)
            sleep(1)
        else:
            print_log(f"poco.click({pos})点击生效，进入下一页")

    def poco_find_all(self, **kwargs):
        """
        功能描述：查询目标控件的个数。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件的个数
        """
        with poco.freeze() as frozen_poco:
            return frozen_poco(**kwargs).__len__()

    def poco_find_pos(self, target=None, **kwargs):
        """
        功能描述：查询目标控件的pos属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件pos
        """
        position = []
        with poco.freeze() as frozen_poco:
            if target == "children":
                attrlen = frozen_poco(**kwargs).children().__len__()
                print(f"目标控件长度为：{attrlen}")
                for i in range(attrlen):
                    pos = frozen_poco(**kwargs).children().__getitem__(i).get_position()
                    position.append(pos)
            else:
                attrlen = frozen_poco(**kwargs).__len__()
                print(f"目标控件长度为：{attrlen}")
                for i in range(attrlen):
                    pos = frozen_poco(**kwargs).__getitem__(i).get_position()
                    position.append(pos)
        return position

    def poco_find_name(self, **kwargs):
        """
        功能描述：查询目标控件的name属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件name
        """
        name = []
        with poco.freeze() as frozen_poco:
            attrlen = frozen_poco(**kwargs).__len__()
            print(f"目标控件长度为：{attrlen}")
            for i in range(attrlen):
                nametmp = frozen_poco(**kwargs).__getitem__(i).get_name()
                name.append(nametmp)
        return name

    def poco_find_attrs_name(self, target=None, **kwargs):
        """
        功能描述：查询目标控件的name和pos属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件name和pos
        """
        attrs = {}
        try:
            with poco.freeze() as frozen_poco:
                if target == "children":
                    attrlen = frozen_poco(**kwargs).children().__len__()
                    for i in range(attrlen):
                        pos = frozen_poco(**kwargs).children().__getitem__(i).get_position()
                        name = frozen_poco(**kwargs).children().__getitem__(i).get_name()
                        attrs.update({name: pos})
                else:
                    attrlen = frozen_poco(**kwargs).__len__()
                    for i in range(attrlen):
                        pos = frozen_poco(**kwargs).__getitem__(i).get_position()
                        name = frozen_poco(**kwargs).__getitem__(i).get_name()
                        attrs.update({name: pos})
        except:
            pass
        return attrs

    def poco_find_attrs_text(self, **kwargs):
        """
        功能描述：查询目标控件的text和pos属性。为提高查询效率，需要冻结poco
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 目标控件name和pos
        """
        attrs = {}
        with poco.freeze() as frozen_poco:
            attrlen = frozen_poco(**kwargs).__len__()
            print(f"目标控件长度为：{attrlen}")
            for i in range(attrlen):
                pos = frozen_poco(**kwargs).__getitem__(i).get_position()
                text = frozen_poco(**kwargs).__getitem__(i).get_text()
                attrs.update({text: pos})
        return attrs

    def poco_fuzzy_match_click(self, keyword, attrs):
        """
        功能描述：通过name属性，模糊匹配控件。匹配成功，触发点击；匹配失败，截图
        适用平台：Android,IOS
        :param keyword: name属性，模糊匹配关键词
        :param attrs: 控件属性集合
        :return: 控件位置点击
        """
        for item in attrs.keys():
            print(f"item:{item}")
            if keyword in item:
                print_log(f"匹配成功：{keyword}")
                pos = attrs.get(item)
                self.poco_pos(pos)
            else:
                print_log(f"匹配失败：{keyword}")

    def poco_poll_click_brother(self, **kwargs):
        """
        功能描述：轮询点击目标控件的兄弟节点
        适用范围：Android,IOS
        :param kwargs: 目标控件
        :return: None
        """
        num = poco(**kwargs).parent().child().__len__()
        for i in range(num - 1):
            poco(**kwargs).parent().child()[i].click()
            sleep(10.0)
            show_screen()
            if i == num - 2:
                break

    def poco_poll_click_attrs(self, **kwargs):
        """
        功能描述：轮询点击所有目标控件节点
        适用范围：Android,IOS
        :param kwargs:
        :return:
        """
        num = self.poco_find_all(**kwargs)
        for i in range(num):
            pos = poco(**kwargs).__getitem__(i).get_position()
            self.poco_pos(pos)
            sleep(10.0)
            show_screen()
            if i == num - 1:
                break

    def poco_swipe(self, posa, posb):
        """
        功能描述:封装poco的swipe函数，不选中UI
        适用范围：Android,IOS
        :param posa: 起始位置，相对坐标
        :param posb: 结束位置，相对坐标
        :return: None
        """
        poco.swipe(posa, posb, duration=0.5)
        sleep(1.0)

    def find_target_pos(self, **kwargs):
        """
        功能描述：寻找符合目标要求，且x=0.5的坐标点
        适用范围：Android，IOS
        :param kwargs:目标控件
        :return:None
        """
        pos = self.poco_find_pos(**kwargs)
        position = []
        for item in pos:
            if round(item[0], 1) == 0.5:
                position.append(item)
        print_log(f"目标位置：{position}")
        return position

    def touch_real_pos(self, **kwargs):
        """
        功能描述：部分机型，poco的click事件，坐标点击存在偏移。点击操作改成点击真实坐标
        适用平台：Android,IOS
        :param kwargs: 控件
        :return: 点击目标控件
        """
        pos = poco(**kwargs).get_position()
        pos[0] = pos[0] * width
        pos[1] = pos[1] * height
        msg = f"点击{kwargs}，位置在{pos}"
        print_log(msg)
        return touch(pos)

    def close_assistivetouch(self):
        """
        功能描述：关闭IOS的辅助触控功能

        适用范围：IOS

        :return: None
        """
        switch_list = [
            Template(r"switch_on_se.png", record_pos=(0.369, -0.509), resolution=(640, 1136)),
            Template(r"switch_on_6.png", record_pos=(0.388, -0.567), resolution=(750, 1334)),
            Template(r"switch_on_6p.png", record_pos=(0.386, -0.595), resolution=(1242, 2208)),
            Template(r"switch_on_x.png", record_pos=(0.387, -0.697), resolution=(1125, 2436)),
            Template(r"switch_on_11promax.png", record_pos=(0.387, -0.697), resolution=(1242, 2688))
        ]
        if platform == "IOS":
            s = c.session()
            w, h = s.window_size()
            stop_app("com.apple.Preferences")
            start_app("com.apple.Preferences")
            swipe(center, down)
            ios_ver = G.DEVICE.device_status()['os']['version']
            if "10" in ios_ver:
                self.poco_click(type="SearchField")
                text("AssistiveTouch")
                self.poco_pos([0.5, 0.12])
                if exists_imgs(switch_list):
                    pos = poco(name="AssistiveTouch", type="Switch").get_position()
                    start_point = (pos[0] * w, pos[1] * h)
                    swipe(start_point, center)
                    self.poco_click(name="AssistiveTouch", type="Switch")
                else:
                    print_log(f"辅助触控未开启")
            else:
                self.poco_click(type="SearchField")
                text("辅助触控")
                if "11" in ios_ver:
                    self.poco_click(name="辅助触控")
                elif "12" in ios_ver:
                    self.poco_click(name="重设…")
                elif "13" in ios_ver:
                    self.poco_click(name="触控")
                self.poco_click(name="辅助触控")
                if exists_imgs(switch_list):
                    pos = poco(name="辅助触控", type="Switch").get_position()
                    start_point = (pos[0] * w, pos[1] * h)
                    swipe(start_point, center)
                    self.poco_click(name="辅助触控", type="Switch")
                else:
                    print_log(f"辅助触控未开启")
