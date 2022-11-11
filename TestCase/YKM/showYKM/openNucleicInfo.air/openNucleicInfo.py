# -*- encoding=utf8 -*-
__author__ = "roger"

from airtest.core.api import *
auto_setup(__file__,logdir=True)
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
    touch(Template(r"tpl1666690384296.png", record_pos=(-0.359, -0.622), resolution=(1080, 2220)))
    touch(Template(r"tpl1666690545817.png", record_pos=(-0.286, 0.382), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1666690569581.png", record_pos=(-0.198, -0.796), resolution=(1080, 2220)), "出现核酸检测记录标题")

run_case()

