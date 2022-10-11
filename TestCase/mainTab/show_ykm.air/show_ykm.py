# -*- encoding=utf8 -*-
__author__ = "roger"

from airtest.core.api import *
from common.common import Common
from conf.settings import *
from pathlib import Path
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
    touch(Template(r"tpl1665226194184.png", record_pos=(-0.353, -0.625), resolution=(1080, 2220)))
    touch(Template(r"tpl1665226206907.png", record_pos=(-0.203, 0.101), resolution=(1080, 2220)))

run_this_case()

# report_path = os.path.join(os.path.abspath(Path(__file__).parent), 'resultInfo')
# html_report = LogToHtml(script_root=os.path.abspath(Path(__file__).parent),
#                log_root=os.path.abspath(Path(__file__).parent) + '/log',
#                export_dir=report_path,
#                logfile=os.path.abspath(Path(__file__).parent) + '/log/log.txt', lang='en', plugins=None)
# html_report.report()


