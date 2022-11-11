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
    touch(Template(r"tpl1666688267079.png", record_pos=(-0.359, -0.628), resolution=(1080, 2220)))
    touch(Template(r"tpl1666688354996.png", record_pos=(-0.001, -0.263), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1666688383519.png", record_pos=(0.028, -0.246), resolution=(1080, 2220)), "粤康码放大狮子头")
    touch(Template(r"tpl1666688622078.png", record_pos=(-0.007, 0.414), resolution=(1080, 2220)))


run_case()
