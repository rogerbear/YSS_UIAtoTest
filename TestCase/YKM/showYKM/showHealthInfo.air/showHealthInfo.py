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
    touch(Template(r"tpl1666688880599.png", record_pos=(-0.361, -0.622), resolution=(1080, 2220)))
    touch(Template(r"tpl1666688913769.png", record_pos=(-0.196, 0.219), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1666688932256.png", record_pos=(-0.22, -0.421), resolution=(1080, 2220)), "请填写测试点")
    assert_exists(Template(r"tpl1666688953232.png", record_pos=(-0.231, 0.134), resolution=(1080, 2220)), "请填写测试点")

run_case()
