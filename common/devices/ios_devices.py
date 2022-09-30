# -*- coding: utf-8 -*-
# @Time    : 2021-5-26 13:47
# @Author  : Paner

import os, sys,time
import subprocess
import threading
import _thread
from loguru import logger
from tidevice._wdaproxy import WDAService

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)

from multiprocessing import Process
from tidevice._usbmux import Usbmux
from tidevice import Device
from tidevice._relay import relay

class IOS():
    def __init__(self,pkg):
        self.pkg = pkg
        self._usbmux = Usbmux()
        self.device_thread = ""
        self.device_thread = ""
        self.p =""
        self.serv = ""

    def get_udid(self):
        devices = self._usbmux.device_list()
        for d in devices:
            if d['UDID']:
                return d['UDID']
            elif d['SerialNumber']:
                return d['SerialNumber']
            else:
                return None

    def start_xctest(self):
        d = self.get_udid()
        device = Device(d)
        self.serv = WDAService(device, self.pkg)
        self.serv.start()
        time.sleep(5)
        cmd = [sys.executable, '-m',  "tidevice", "-u", d, "relay", "8100", "8100"]
        logger.debug(cmd)
        self.p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        # serv.start()
        # while serv._service.running:
        #     time.sleep(1)


        # self.device_thread = Process(target=device.xctest,
        #              args=(self.pkg, None, None, {"USB_PORT": 8100}))
        # self.device_thread.run()
        # self.device_thread = threading.Thread(target=device.xctest, args=(self.pkg, None, None, {"USB_PORT": 8100},))
        # self.device_thread.daemon = False
        # self.device_thread.start()
        # time.sleep(5)
        #
        # self.relay_thread = threading.Thread(target=relay, args=(device, 8100, 8100, False,))
        # self.relay_thread.daemon = True
        # self.relay_thread.start()
        # _thread.start_new_thread(self._run_case, (task_id, case, device_id,), daemon=True)
        # self.relay_thread = Process(target=relay, args=(device, 8100, 8100, False))
        # self.relay_thread.run()


    def stop_xctest(self):
        if self.p:
            self.p.terminate()
        elif self.serv._service.running:
            self.serv.stop()

if __name__ == "__main__":
    # main()
    ios = IOS("com.xiaopeng.wda.xctrunner")
    ios.start_xctest()