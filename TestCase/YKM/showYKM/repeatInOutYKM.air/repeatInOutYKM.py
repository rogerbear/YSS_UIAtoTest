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
    touch(Template(r"tpl1666692618533.png", record_pos=(-0.364, -0.626), resolution=(1080, 2220)))
    sleep(1)
    for _ in range(5):
        touch(Template(r"tpl1666692646695.png", record_pos=(-0.289, 0.379), resolution=(1080, 2220)))
        sleep(1)
        keyevent("BACK")
        sleep(1)
        touch(Template(r"tpl1666693019910.png", record_pos=(0.231, 0.382), resolution=(1080, 2220)))
        sleep(1)
        keyevent("BACK")
        sleep(1)
    assert_exists(Template(r"tpl1666693472253.png", record_pos=(0.001, -0.268), resolution=(1080, 2220)), "二维码狮子头展示正常")


run_case()




