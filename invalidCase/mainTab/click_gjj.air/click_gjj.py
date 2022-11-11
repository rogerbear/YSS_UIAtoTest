# -*- encoding=utf8 -*-
__author__ = "roger"

import os
from pathlib import Path

from airtest.core.api import *

auto_setup(__file__, logdir=True)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
touch(Template(r"tpl1665296110389.png", record_pos=(-0.338, 0.082), resolution=(1080, 2220)))
assert_exists(Template(r"tpl1665296142082.png", record_pos=(-0.23, -0.252), resolution=(1080, 2220)),
              "Please fill in the test point.")
