# -*- encoding=utf8 -*-
__author__ = "roger"

from pathlib import Path
from airtest.core.api import *
from common.common import Common
from conf.settings import *
from airtest.report.report import LogToHtml

auto_setup(__file__)
common = Common()

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
def restart_app(pkg):
    common.quit_app(pkg)
    sleep(1)
    start_app(pkg)

def run_this_case():
    restart_app(test_pkg)
    touch(Template(r"tpl1665296110389.png", record_pos=(-0.338, 0.082), resolution=(1080, 2220)))
    assert_exists(Template(r"tpl1665296142082.png", record_pos=(-0.23, -0.252), resolution=(1080, 2220)),
                  "Please fill in the test point.")
# simple_report(__file__, logpath=True, output=os.path.abspath(Path(__file__).parent) + '/log/result.html')
run_this_case()

# report_path = os.path.join(os.path.abspath(Path(__file__).parent), 'resultInfo')
# html_report = LogToHtml(script_root=os.path.abspath(Path(__file__).parent),
#                log_root=os.path.abspath(Path(__file__).parent) + '/log',
#                export_dir=report_path,
#                logfile=os.path.abspath(Path(__file__).parent) + '/log/log.txt', lang='en', plugins=None)
# html_report.report()
