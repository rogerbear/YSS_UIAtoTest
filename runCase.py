# coding = utf-8
# author:roger

import os

current_path = os.path.abspath(__file__)
print(current_path.split('/')[-2])
import datetime
import io
import shutil
from argparse import *

import jinja2
from airtest.cli.runner import AirtestCase, run_script
from airtest.core.api import connect_device
from airtest.report.report import LogToHtml

from tools import *


class Air_Case_Handler(AirtestCase):
    def __init__(self, dev_id):
        super(Air_Case_Handler, self).__init__()
        if deviceType.upper() == "WEB":
            pass
        else:
            self.dev = connect_device(dev_id)

    def setUp(self):
        super(Air_Case_Handler, self).setUp()

    def tearDown(self):
        super(Air_Case_Handler, self).tearDown()

    def run_case(self, case_dir, device):
        start_time = datetime.datetime.now()
        start_time_fmt = start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        results = []

        # 创建存放log的目录
        # root_log = log_path
        # if os.path.isdir(root_log):
        #     shutil.rmtree(root_log)
        # else:
        #     os.makedirs(root_log)

        def add_case(caseDirName, caseName):
            case_log = os.path.join(root_path, "logReport/" + caseDirName)
            print(case_log.split('/')[-2:], "这是caselog")
            # script_run_log = os.path.join(case_log, caseDirName + '.log')
            if os.path.isdir(case_log):
                # print(case_log)
                shutil.rmtree(case_log)
            else:
                # pdb.set_trace()
                # 创建存放运行结果的目录
                os.makedirs(case_log)

            if deviceType.upper() == "WEB":
                args = Namespace(log=case_log, recording=None, script=script,
                                 language="zh")
            elif deviceType.upper() == "APP":
                args = Namespace(device=device, log=case_log, script=script, no_image=False,
                                 recording=None, language="zh")
            else:
                args = Namespace(device=device, log=case_log, recording=None, script=script,
                                 language="zh")
            try:
                run_script(args, AirtestCase)
            except AssertionError as e:
                pass
            finally:
                html_save_dir = ''
                for root, dir, files in os.walk(case_log):
                    for html_log in dir:
                        if '.log' in html_log:
                            html_save_dir = html_log
                # 存放html文件的目录
                html = os.path.join(html_save_dir, "log.html")
                report_path = case_log
                html_report = LogToHtml(script_root=script,
                                        log_root=case_log,
                                        export_dir=report_path,
                                        logfile=os.path.join(case_log, 'log.txt'),
                                        lang='en',
                                        plugins=['poco.utils.airtest.report'])
                html_report.report("log_template.html", output_file=html)
                # rpt = report.LogToHtml(script, case_log)
                # rpt.report("log_template.html", output_file=html)
                result = {}
                # 把手写脚本和录制脚本放在列表中
                if caseName.endswith(".py"):
                    # result["name"] = caseName.replace('.py', '')
                    result['name'] = "".join(
                        [current_path.split('/')[-2], '/logReport/', caseDirName, '/', caseDirName, '.log'])
                elif caseName.endswith(".air"):
                    # result["name"] = caseName.replace('.air', '')
                    result['name'] = "".join(
                        [current_path.split('/')[-2], '/logReport/', caseDirName, '/', caseDirName, '.log'])
                result["result"] = html_report.test_result
                results.append(result)

        # 添加脚本
        for file in get_filelist(case_dir, []):
            if file.endswith(".py"):
                caseName = file
                caseDirName = file.replace(".py", "").split('/')[-1]
                # print(caseDirName+"*******************")
                script = os.path.join(case_dir, file)
                add_case(caseDirName, caseName)
            elif file.endswith(".air"):
                caseName = file
                caseDirName = file.replace(".air", "")
                script = os.path.join(case_dir, file)
                add_case(caseDirName, caseName)

        end_time = datetime.datetime.now()
        end_time_fmt = end_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        duration = (end_time - start_time).seconds

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            extensions=(),
            autoescape=True
        )

        template = env.get_template(template_name, template_path)
        project_name = root_path.split("\\")[-1]
        success = 0
        fail = 0
        for res in results:
            if res['result']:
                success += 1
            else:
                fail += 1
        report_name = "report_" + end_time.strftime("%Y%m%d%H%M%S") + ".html"
        html = template.render(
            {"results": results, "device": device, "stime": start_time_fmt, 'etime': end_time_fmt, 'duration': duration,
             "project": project_name, "success": success, "fail": fail})
        output_file = os.path.join(root_path, "report", report_name)
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    for device in devices:
        try:
            test = Air_Case_Handler(device)
            test.run_case(case_path, device)
        except Exception as e:
            pass
