# -*- encoding=utf8 -*-
__author__ = "roger"

from airtest.core.api import *

# auto_setup(__file__)
# connect_device("Android:///?cap_method=javacap")

from common.common import Common
from conf.settings import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

common = Common()
def restart_app(pkg):
    common.quit_app(pkg)
    sleep(1)
    start_app(pkg)


def run_case():
    restart_app(test_pkg)
    touch(Template(r"tpl1666686666841.png", record_pos=(-0.36, -0.626), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1666686730960.png", record_pos=(-0.001, -0.262), resolution=(1080, 2220)), "展示二维码的小狮子头")


run_case()





