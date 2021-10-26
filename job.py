import os
import time
import queue
from sys import stdout

import win32con
import win32console
from icmp import Icmp
from conf import config
from ctypes import CDLL
from threading import Thread
from typing import Tuple, List

from pic import show, save

sync_queue = queue.Queue()
cprint = CDLL('./so/cprint.so').cprint


class Job:
    _test_str = 'ping: %s\tdate: %s\tdelay: %s ms'
    _rate_str = '进度：[%s%s]\t %s/%s'

    def __init__(self):
        self.str_buffer = ''
        self.dir = os.path.join(os.path.dirname(__file__), config.pic_dir)
        self.icmp = Icmp(config.target_ip)

    def _before_run(self):
        print('测试前检查')
        if not self.icmp.first_ping():
            raise Exception('第一次检查失败，请确认【域名/ip/dns】设置正确')
        if not os.path.isdir(self.dir):
            raise Exception('请检查文件路径是否正确\n%s' % config.pic_dir)
        print('状态正常，开始测试')
        time.sleep(1)
        os.system("chcp 65001 & cls")

    def _str_agg(self, row_str: str):
        suffix = (config.string_length - len(row_str.encode('gbk'))) * ' ' + '\n'
        self.str_buffer += row_str + suffix

    def _add_job(self):
        self.thread = Thread(target=self.icmp.test, args=(config.count, config.cell, sync_queue))
        self.thread.start()

    def _main_job(self):
        count = 1
        while self.thread.is_alive():
            out = sync_queue.get()
            if out == 'end':
                break
            self._str_agg('最近%s条记录' % config.row_num)
            self._str_agg(' ')
            for i in self.icmp.res[0 - config.row_num:]:
                self._str_agg(self._test_str % (config.target_ip, *i))
            self._str_agg(' ')
            self._str_agg(self._rate_str % ('>' * int(count * 20 / config.count),
                        ' ' * (20 - int(count * 20 / config.count)),
                        str(count), str(config.count)))
            cprint(self.str_buffer.encode())
            self.str_buffer = ''
            count += 1

    def _to_pic(self):
        x, y = zip(*self.icmp.res)
        if config.show_pic:
            show(x, y)
        print('保存中')
        save(x, y, self.dir, 'ICMP')
        print('运行完成')
        os.system('pause')

    def run(self):
        # 执行前确定满足基本参数条件
        self._before_run()
        # 执行子线程
        self._add_job()
        # 处理主线程控制台任务
        self._main_job()
        # 生成图片
        self._to_pic()


if __name__ == '__main__':
    job = Job()
    job.run()
