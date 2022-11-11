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
    touch(Template(r"tpl1666747309185.png", record_pos=(-0.362, -0.624), resolution=(1080, 2220)))
    sleep(3)
    for _ in range(5):
        wait(Template(r"tpl1666747932218.png", record_pos=(0.092, -0.726), resolution=(1080, 2220)))
        touch(Template(r"tpl1666747836200.png", record_pos=(0.096, -0.727), resolution=(1080, 2220)))
        sleep(3)
        keyevent("BACK")
    assert_exists(Template(r"tpl1666747412351.png", record_pos=(0.002, -0.267), resolution=(1080, 2220)), "粤康码狮子头展示正常")


run_case()




