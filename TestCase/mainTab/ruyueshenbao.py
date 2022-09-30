# -*- coding: utf-8 -*- 
# @Time : 2022/9/30 2:55 下午 
# @Author : roger 
# @File : ruyueshenbao.py

import os
import sys
from pathlib import Path

path = os.path.abspath(Path(__file__).parent.parent.parent.parent)
sys.path.append(path)


from airtest.core.api import *
from airtest.report.report import simple_report

from conf.settings import *

# from common.devices.ios_devices import IOS
# ios = IOS("com.xiaopeng.wda.xctrunner")
# ios.start_xctest()
# sleep(2)
# connect_device("IOS:////127.0.0.1:8100")
# connect_device("Android://127.0.0.1:5037/c6366a94")
# connect_device("Android:///?cap_method=javacap") # 单独跑就需要

from common.common import Common
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)

# 单独跑就需要
"""
platform = G.DEVICE.__class__.__name__
if platform == 'Android':
    from poco.drivers.android.uiautomation import AndroidUiautomationPoco
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)
elif platform == 'IOS':
    import wda

    c = wda.Client(G.DEVICE.addr)
    from poco.drivers.ios import iosPoco

    poco = iosPoco()

auto_setup(__file__, logdir=True)
"""

# yss_app_pkg = "com.digitalgd.dgyss" # 单独跑就需要

common = Common()
def restart_app(pkg):
    common.quit_app(pkg)
    sleep(1)
    start_app(pkg)


def test_app():
    restart_app(test_pkg)
    poco(text="首页").wait_for_appearance(10)
    common = Common()
    common.poco_click_exists(text="办事")

test_app()
caseLogPath = path = os.path.abspath(Path(__file__)).split('/')[-1].replace('.py', '')
print('/Users/roger/Documents/DigitalGD/AutoTetst/UIAutoTest/YSS_UIAtoTest/log/{}/log.txt'.format(
    caseLogPath) + "这是caseLogPath")
simple_report(__file__, logpath=True,
              logfile='/Users/roger/Documents/DigitalGD/AutoTetst/UIAutoTest/YSS_UIAtoTest/log/{}/log.txt'.format(
                  caseLogPath),
              output='/Users/roger/Documents/DigitalGD/AutoTetst/UIAutoTest/YSS_UIAtoTest/log/{}/log.html'.format(
                  caseLogPath))
# ios.stop_xctest()