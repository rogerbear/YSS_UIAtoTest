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
    touch(Template(r"tpl1666746614430.png", record_pos=(-0.356, -0.626), resolution=(1080, 2220)))
    sleep(3)
    wait(Template(r"tpl1666748163990.png", record_pos=(0.098, -0.728), resolution=(1080, 2220)))
    touch(Template(r"tpl1666746669270.png", record_pos=(0.096, -0.728), resolution=(1080, 2220)))
    sleep(1)
    assert_exists(Template(r"tpl1666746838431.png", record_pos=(-0.187, 0.174), resolution=(1080, 2220)), "家庭成员信息展示")

run_case()



