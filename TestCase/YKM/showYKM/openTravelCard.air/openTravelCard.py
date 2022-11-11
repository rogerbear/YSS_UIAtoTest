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
    touch(Template(r"tpl1666689854503.png", record_pos=(-0.357, -0.62), resolution=(1080, 2220)))
    touch(Template(r"tpl1666689869629.png", record_pos=(0.27, 0.221), resolution=(1080, 2220)))
    touch(Template(r"tpl1666689900606.png", record_pos=(-0.347, 0.228), resolution=(1080, 2220)))
    touch(Template(r"tpl1666689925502.png", record_pos=(0.003, 0.384), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1666690668606.png", record_pos=(0.007, -0.013), resolution=(1080, 2220)), "出现通行卡箭头")


run_case()


