# -*- encoding=utf8 -*-
__author__ = "roger"

from airtest.core.api import *
# auto_setup(__file__)
# connect_device("Android:///?cap_method=javacap")

from conf.settings import *
from common.common import Common
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

common = Common()
def restart_app(pkg):
    common.quit_app(pkg)
    sleep(1)
    start_app(pkg)

def noLoginShowYKM():
    """
    @caseID:0001
    @desc:未登录时点击粤康码
    @auth:rogerzhao
    @priority:severity(冒烟)/P0(发布性)/P1/P2
    """
    restart_app(test_pkg)
    touch(Template(r"tpl1666681708053.png", record_pos=(-0.36, -0.626), resolution=(1080, 2220)))
    touch(Template(r"tpl1666682000563.png", record_pos=(0.206, 0.104), resolution=(1080, 2220)))
    touch(Template(r"tpl1666682030681.png", record_pos=(0.008, -0.03), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1666682336805.png", threshold=0.6, record_pos=(0.003, -0.62), resolution=(1080, 2220)), "找不到人脸识别图标")

noLoginShowYKM()



