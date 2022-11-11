# -*- encoding=utf8 -*-
__author__ = "roger"

from airtest.core.api import *

auto_setup(__file__)
connect_device("Android:///?cap_method=javacap")

from conf.settings import *
from common.common import Common

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

common = Common()


def restart_app(pkg):
    common.quit_app(pkg)
    sleep(1)
    start_app(pkg)


def run_case():
    restart_app(test_pkg)
    touch(Template(r"tpl1666695489075.png", record_pos=(-0.354, -0.624), resolution=(1080, 2220)))
    sleep(5)
    touch(Template(r"tpl1666696100621.png", target_pos=4, record_pos=(0.063, -0.724), resolution=(1080, 2220)))
    sleep(1)
    swipe(Template(r"tpl1666695833957.png", record_pos=(-0.319, 0.847), resolution=(1080, 2220)),
          vector=[0.0583, -0.17])
    sleep(1)
    touch(Template(r"tpl1666695861728.png", record_pos=(0.418, 0.274), resolution=(1080, 2220)))
    sleep(1)
    assert_exists(Template(r"tpl1666695905409.png", record_pos=(-0.238, -0.73), resolution=(1080, 2220)), "代亲属出示健康码")
    assert_exists(Template(r"tpl1666696119191.png", record_pos=(0.001, -0.264), resolution=(1080, 2220)), "二维码狮子头出现")


run_case()


