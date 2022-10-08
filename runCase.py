# coding = utf-8
# author:roger

import datetime
import io
import shutil
from argparse import *

import airtest.report.report as report
import jinja2
from airtest.cli.runner import AirtestCase, run_script
from airtest.core.api import connect_device

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
        root_log = log_path
        if os.path.isdir(root_log):
            shutil.rmtree(root_log)
        else:
            os.makedirs(root_log)

        for file in get_filelist(case_dir, []):
            if file.endswith(".py"):
                caseName = file
                caseDirName = file.replace(".py", "").split('/')[-1]
                # print(caseDirName+"*******************")
                script = os.path.join(case_dir, file)

                case_log = os.path.join(root_path, "log/" + caseDirName)
                # print(case_log+"******************")

                if os.path.isdir(case_log):
                    # print(case_log)
                    shutil.rmtree(case_log)

                else:
                    os.makedirs(case_log)

                html = os.path.join(case_log, "log.html")
                if deviceType.upper() == "WEB":
                    args = Namespace(log=case_log, recording=None, script=script,
                                     language="zh")
                elif deviceType.upper() == "APP":
                    args = Namespace(device=device, log=case_log, recording=caseDirName + ".mp4", script=script,
                                     language="zh")
                else:
                    args = Namespace(device=device, log=case_log, recording=None, script=script,
                                     language="zh")
                try:
                    run_script(args, AirtestCase)
                except AssertionError as e:
                    pass
                finally:
                    rpt = report.LogToHtml(script, case_log)
                    rpt.report("log_template.html", output_file=html)
                    result = {}
                    result["name"] = caseName.replace('.py', '')
                    result["result"] = rpt.test_result
                    results.append(result)

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
        test = Air_Case_Handler(device)
        test.run_case(case_path, device)
