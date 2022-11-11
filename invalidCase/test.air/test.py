# -*- encoding=utf8 -*-
__author__ = "roger"

from airtest.core.api import *
from common.common import Common
auto_setup(__file__)
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

touch(Template(r"tpl1667960836325.png", record_pos=(-0.358, -0.692), resolution=(1080, 2376)))
wait(Template(r"tpl1667960864288.png", record_pos=(-0.334, -0.186), resolution=(1080, 2376)))
swipe(Template(r"tpl1667960920444.png", record_pos=(0.001, 0.607), resolution=(1080, 2376)), vector=[-0.0105, -0.4527])
exists(Template(r"tpl1667960930690.png", record_pos=(-0.103, 0.016), resolution=(1080, 2376)))
text("公积金")
keyevent("BACK")
snapshot(msg="这个截图是为了验证团体码图标是否存在.")
sleep(1.0)
assert_exists(Template(r"tpl1667961011856.png", record_pos=(0.13, 0.017), resolution=(1080, 2376)), "请填写测试点")
assert_not_exists(Template(r"tpl1667961018081.png", record_pos=(0.345, 0.012), resolution=(1080, 2376)), "请填写测试点")
assert_equal(poco("com.digitalgd.dgyss:id/tv_title").get_text(), "首页", "测试点：控件的text属性值为首页")
assert_not_equal(str(poco(text="首页").attr("enabled")), "True", "控件的enabled属性值为True")
poco(text="首页").wait_for_appearance(10)
common = Common()
common.poco_click_exists(text="办事")



