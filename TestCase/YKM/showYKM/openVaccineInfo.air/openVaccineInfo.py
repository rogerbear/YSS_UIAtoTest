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
    touch(Template(r"tpl1666691040051.png", record_pos=(-0.362, -0.626), resolution=(1080, 2220)))
    sleep(1)
    touch(Template(r"tpl1666691225539.png", record_pos=(0.225, 0.382), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1666691099827.png", record_pos=(-0.201, -0.769), resolution=(1080, 2220)), "疫苗接种记录标题")

run_case()


