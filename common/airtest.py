#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 6:25 下午
# @Author  : roger
# @File    : airtest.py

__author__ = "neallyl"

import os, sys

from airtest.aircv.keypoint_base import print_run_time

curPath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(curPath)

from common.lib import *
from common.android import Android
from common.ios import IOS

ios = IOS()
android = Android()
auto_setup(__file__)


class Airtest(object):
    def __init__(self):
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.task_day = datetime.date.today().strftime("%Y-%m-%d")
        if platform == "IOS":
            self.s = c.session()
            self.w, self.h = self.s.window_size()

    def run_monkey(self, times, pkg=None):
        """
        功能描述：运行monkey
        适用范围：Android，IOS
        :param times: Android表示monkey点击次数；IOS表示运行时长
        :param pkg: 包名
        :return:None
        """
        if platform == 'Android':
            cmd = f"monkey -p {pkg} --throttle 250 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes --pct-appswitch 5 --pct-touch 25 --pct-motion 50 --pct-trackball 15 --pct-anyevent 5 -s 1000 {str(times)} -v -v -v 100"
            print_log(f"执行中", screenshot=False)
            G.DEVICE.shell(cmd)
        elif platform == 'IOS':
            start_url, stop_url = get_ios_monkey_url(pkg)
            c.http.get(start_url)
            # G.DEVICE.driver.http.get(start_url)
            print_log(f"monkey运行中")
            sleep(times)
            c.http.get(stop_url)
            # G.DEVICE.driver.http.get(stop_url)
            print_log(f"本次monkey运行结束")

    def quit_app(self, pkg):
        """
        功能描述：退出app
        适用范围：Android,IOS
        :param pkg: 包名
        :return: None
        """
        print_log(f"关闭{pkg}", screenshot=False)
        try:
            stop_app(pkg)  # AirtestIDE需要更新1.2.6以后，IOS上该指令才生效。
        except:
            pass
        sleep(1.0)

    def init_result(self, content):
        """
        功能描述：发布性用例结果，上传结果至idb

        适用范围：Android，IOS

        :param content:统计数据.content内容如下：
        (device_name,task_day,testcase,instance,rom,datetime,platform,result,status,product)

        :return:None
        """
        from common.Idb import Idb
        idb = Idb()
        try:
            print_log(f"content={content}")
            idb.insert_result_qa(content)
            log(f"统计初始化成功")
        except:
            log(f"统计初始化失败")

    def insert_monkey_result(self, content):
        """
        功能描述：monkey任务数据，上传结果至idb

        适用范围：Android，IOS

        :param content:统计数据.content内容如下：
        (device_name,task_day,sences,times,rom,datetime,platform,result,product)

        :return:None
        """
        from common.Idb import Idb
        idb = Idb()
        try:
            print_log(f"content={content}")
            idb.insert_result_monkey(content)
            log(f"monkey结果上传成功")
        except:
            log(f"monkey结果上传失败")

    def update_result(self, path):
        """
        功能描述:更新用例执行结果

        适用范围:Android，IOS

        :param path:默认传参__file__
        :return:None
        """
        if get_irma_ext() == "on":
            from common.Idb import Idb
            idb = Idb()
            try:
                testcase = get_testcase(path)[1]
                idb.update_result_qa(testcase, self.date_time)
                log(f"结果更新成功")
            except:
                log(f"结果更新失败")
        else:
            print_log("不触发统计")

    def ocr_text_exist(self, text, num=0, full_match=1):
        """
        功能描述：判断ocr文字是否存在
        适用范围：Android，IOS
        :param text: 关键词
        :param num: 第几个关键词，默认第一个
        :param full_match: 是否全匹配
        :return:
        """
        sleep(1)
        if not os.path.exists(pic_filepath):
            os.makedirs(pic_filepath)
            snapshot
        for i in range(2):
            millis = str(int(round(time.time() * 1000)))
            img_path = os.path.join(pic_filepath, millis + ".png")
            if platform == 'Android':
                screen = G.DEVICE.snapshot()
                pil_img = cv2_2_pil(screen)
                pil_img.save(img_path, quality=99, optimize=True)
            elif platform == 'IOS':
                c.screenshot(img_path)
            # result = antalService.get_text_ocr_res(text, img_path, full_match)
            x, y = smartService.get_text_ocr_res(text, img_path)
            return x, y
            # x, y = vpfservice.get_text_ocr_res(text, img_path)
            # print_log(f"文字识别结果：{result}")
            # if len(result) > 0:
            #     return result[num][0], result[num][1]
        return 0, 0

    def ocr_text_click(self, text, num=0):
        """
        功能描述：识别图像中的文字，并点击
        适用范围：Android，IOS
        :param text: 关键词
        :param num: 关键词的索引
        :return:None
        """
        x, y = self.ocr_text_exist(text, num)
        if x > 0 and y > 0:
            if platform == 'Android':
                print_log(f"click {text} coordinate：{int(x), int(y)}")
                touch((int(x), int(y)))
            elif platform == 'IOS':
                scale = self.s.scale
                print_log(f"click {text} coordinate：{int(x / scale), int(y / scale)},scale: {scale}")
                self.s.click(int(x / scale), int(y / scale))
        else:
            print_log(f"click {text} not found")
        sleep(1.0)

    def remove_pic(self):
        """
        功能描述：删除ocr过程图片
        适用范围：Android，IOS
        :return: None
        """
        if os.path.exists(pic_filepath):
            shutil.rmtree(pic_filepath)

    def touch_imgs(self, pic):
        """
        功能描述：多张图片，匹配点击。用于兼容多分辨率设备的图像识别失败的问题。

        适用范围：Android，IOS

        :param pic: 图片列表
        :return:
        """
        flag = 0
        if isinstance(pic, list):
            for item in pic:
                if exists(item):
                    touch(item)
                    flag = 1
                    break
                else:
                    continue
            if flag == 0:
                assert_equal(0, 1, f"图片不存在")
        else:
            assert_equal(0, 1, f"pic不是列表")

    def get_screen_text(self, img_file=None):
        """
        根据提供的截图路径获取截图文字，不传则截取当前整个页面快照作为识别对象
        :param img_file:
        :return:
        """
        if not img_file:
            img_file = self.save_screen_shot()
        if not os.path.exists(img_file):
            return "Error：要识别的图片路径不存在."
        upload_url = vpfservice.upload_oss_url(img_file)
        res = vpfservice.get_ocr_res(upload_url)  # 文字识别
        word_res = res.get('data').get('word_boxes')
        # 返回列表结构：[{'rect': [508, 8, 693, 48], 'word': '15985135'}]
        print('word res:', word_res)
        return word_res

    def save_screen_shot(self):
        """
        保存快照，路径是项目路径/pic/时间戳.png
        适用：Android、IOS
        :return:
        """
        millis = str(int(round(time.time() * 1000)))
        img_path = os.path.join(pic_filepath, millis + ".png")
        if platform == 'Android':
            screen = G.DEVICE.snapshot()
            pil_img = cv2_2_pil(screen)
            pil_img.save(img_path, quality=99, optimize=True)
        elif platform == 'IOS':
            screen = c.screenshot(img_path)
        return img_path

    @print_run_time
    def partial_screen_shot(self, file_name=None, absolute=0, x_min=0, y_min=0, x_max=0, y_max=0):
        """
        适用：
        截图，返和图片路径，absolute指定是否是绝对坐标，默认是相对坐标，不传或全部为0则是全局截图
        :param x_min:
        :param y_min:
        :param x_max:
        :param y_max:
        :return:
        """
        if not file_name:
            millis = str(int(round(time.time() * 1000)))
            img_path = os.path.join(pic_filepath, millis + ".png")
        else:
            img_path = os.path.join(pic_filepath, file_name + ".png")
        is_horizonal, width, height = get_orientation_size()
        screen = G.DEVICE.snapshot()
        part_screen = screen
        if x_min or y_min or x_max or y_max:
            if not absolute:
                part_screen = aircv.crop_image(screen, (x_min * width, y_min * height, x_max * width, y_max * height))
            else:
                part_screen = aircv.crop_image(screen, (x_min, y_min, x_max, y_max))

        if platform == 'Android':
            pil_img = cv2_2_pil(part_screen)
            pil_img.save(img_path, quality=30)

        elif platform == 'IOS':
            aircv.imwrite(img_path, part_screen, 99)
        return img_path

    def find_text_in_ocr_res(self, keyword, ocr_res):
        """
        结合get_screen_text使用，找出OCR识别结果中，是否包含要查询的关键字
        OCR识别结果格式：[{'rect': [508, 8, 693, 48], 'word': '15985135'}]
        :param text:
        :param ocr_res:
        :return:
        """
        if not isinstance(keyword, str):
            keyword = str(keyword)
        has_keyword = False
        if ocr_res == [] or len(ocr_res) == 0:
            return has_keyword
        for item in ocr_res:
            if item.get('word').find(keyword) != -1:
                has_keyword = True
                # print('有关键字，item word:', item['word'])
                break
            else:
                continue
        return has_keyword

    def touch_retry(self, v, times, **kwargs):
        """
        功能描述：touch点击重试。使用adb点击重试
        适用范围：Android,IOS
        """
        if platform == 'Android':
            pos = touch(v, times, **kwargs)
            sleep(2)
            for i in range(times):
                if exists(v):
                    print_log(f"第{i + 1}次点击未生效，重试一次")
                    android.adb_touch(pos[0], pos[1])

        else:
            touch(v, times, **kwargs)

    def text(self, keywords, is_screenshot=True, enter=False):
        """
        封装源生text，增加截图
        """
        text(keywords, enter)
        sleep(1.0)
        if is_screenshot:
            show_screen()
