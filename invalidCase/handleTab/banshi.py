# -*- coding: utf-8 -*- 
# @Time : 2022/10/9 3:49 下午 
# @Author : roger 
# @File : banshi.py

import os
import sys
from pathlib import Path
p = os.path.abspath(Path(__file__).parent)
path = os.path.abspath(Path(__file__).parent.parent.parent.parent)
sys.path.append(path)
from airtest.core.api import *
from conf.settings import *
connect_device("Android:///?cap_method=javacap")  # 单独跑就需要
from common.common import Common
common = Common()
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)

auto_setup(__file__) # 单独跑就需要
yss_app_pkg = "com.digitalgd.dgyss"  # 单独跑就需要
def restart_app(pkg):
    common.quit_app(pkg)
    sleep(1)
    start_app(pkg)

def run_test():
    restart_app(test_pkg)
    poco(text="首页").wait_for_appearance(10)
    common = Common()
    common.poco_click_exists(text="办事")

run_test()


# report_name = os.path.abspath(Path(__file__)).split('/')[-1].replace('.py', '')
# report_path = os.path.join(os.path.abspath(Path(__file__).parent), report_name)
#
# html_report = LogToHtml(script_root=os.path.abspath(Path(__file__).parent),
#                log_root=report_path + '/log',
#                export_dir=report_path,
#                logfile=report_path + '/log/log.txt', lang='en', plugins=None)
# html_report.report()


# caseLogPath = os.path.abspath(Path(__file__)).split('/')[-1].replace('.py', '')
# caseParentPath = os.path.abspath(Path(__file__).parent)
# simple_report(__file__, logpath=True,
#               logfile=caseParentPath + '/log/log.txt',
#               output=caseParentPath + '/log/log.html')

# ios.stop_xctest()
