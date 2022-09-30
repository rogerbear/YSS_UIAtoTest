#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 4:48 下午
# @Author  : roger
# @File    : wda.py

__author__ = "neallyl"

import os, sys

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)

from common.lib import *

auto_setup(__file__)


class IOS(object):
    def __init__(self):
        if platform == "IOS":
            self.s = c.session()
            self.w, self.h = self.s.window_size()

    def wda_click(self, **kwargs):
        """
        功能描述：wda库的点击操作。若IOS的poco click未生效，可以采用此方法代替。此方法无日志，无步骤
        适用范围：IOS
        :param kwargs: 目标控件
        :return: None
        """
        print_log(f"点击{kwargs}")
        self.s(**kwargs).tap()
        sleep(0.5)

    def wda_click_exist(self, **kwargs):
        """
        功能描述：wda click前判断是否存在
        适用范围：IOS
        :param kwargs: 目标控件
        :return: None
        """
        for i in range(2):
            try:
                self.wda_click(**kwargs)
            except:
                pass
            # if self.poco_exists(**kwargs):
            #     self.wda_click(**kwargs)
            #     break

    def wda_click_pos(self, **kwargs):
        """
        功能描述：wda库的坐标点击操作。此方法无日志，无步骤

        注意：wda获取的屏幕大小与poco获取的分辨率不一致

        适用范围：IOS

        :param kwargs: 目标控件
        :return: None
        """
        pos = poco(**kwargs).get_position()
        print_log(f"分辨率：{self.w} {self.h}", screenshot=False)
        x = pos[0] * self.w
        y = pos[1] * self.h
        print_log(f"点击{kwargs}，位置在{x},{y}")
        self.s.tap(x, y)
        sleep(0.5)
