import os
import sys
import time
import queue
import keyboard

from icmp import Icmp
from conf import config
from ctypes import CDLL
from pic import show, save
from threading import Thread

ascii_img = r'''
╔═════════════════════════════════════════╗
║            /)  (\                       ║
║       .-._((,~~.))_.-,     //""""/""/   ║
║        `-.   @@   ,-'     //    /  /    ║
║          / ,o--o. \      //╲   /  /     ║
║         ( ( .__. ) )    //   ╲/,,/      ║
║          ) `----' (    //               ║
║         /          \  ()                ║
║        /            \//                 ║
║       /              \                  ║
╚═════════════════════════════════════════╝'''

sync_queue = queue.Queue()
c_print = CDLL('./so/cprint.so').cprint


class LoopList:
    def __init__(self, size):
        self._size = size
        self._list = [['/', '/']] * size
        self._index = 0

    def put(self, ele):
        if self._index == self._size - 1:
            self._list[self._index] = ele
            self._index = 0

        else:
            self._list[self._index] = ele
            self._index += 1

    def gen(self):
        c = self._size
        i = self._index
        if i == self._size:
            i = 0
        while c > 0:
            yield self._list[i]
            i += 1
            if i == self._size:
                i = 0
            c -= 1


class Monitor:
    @staticmethod
    def catch(icmp: Icmp):
        while icmp.enable:
            if keyboard.is_pressed('enter'):
                icmp.enable = False
                return
            time.sleep(0.01)


class Job:
    _test_str = 'ping: %s\tdate: %s\tdelay: %s ms'
    _rate_str = '进度：[%s%s]\t %s/%s'

    def __init__(self):
        self.str_buffer = ''
        if getattr(sys, 'frozen', False):
            self.dir = os.path.join(os.path.dirname(sys.executable), config.pic_dir)
        elif __file__:
            self.dir = os.path.join(os.path.dirname(__file__), config.pic_dir)

        self.icmp = Icmp(config.target_ip)
        self.monitor = Monitor()
        self.loop_list = LoopList(config.row_num)

    def _before_run(self):
        print('测试前检查')
        if not self.icmp.first_ping():
            raise Exception('第一次检查失败，请确认【域名/ip/dns】设置正确')
        if not os.path.isdir(self.dir):
            print(self.dir)
            raise Exception('请检查文件路径是否正确\n%s' % self.dir)
        print('状态正常，开始测试')
        print(ascii_img)
        print('power by 【战斧奶牛】')
        time.sleep(1)
        os.system("chcp 65001 & cls")

    def _str_agg(self, row_str: str):
        suffix = (config.string_length - len(row_str.encode('gbk'))) * ' ' + '\n'
        self.str_buffer += row_str + suffix

    def _add_job(self):
        self.thread = Thread(target=self.icmp.test, args=(config.count, config.cell, sync_queue))
        self.thread.start()

    def _monitor_job(self):
        Thread(target=self.monitor.catch).start()

    def _main_job(self):
        count = 1
        while self.thread.is_alive():
            out = sync_queue.get()
            if out == 0:
                break
            self.loop_list.put(out)
            self._str_agg('最近%s条记录' % config.row_num)
            self._str_agg(' ')
            for i in self.loop_list.gen():
                self._str_agg(self._test_str % (config.target_ip, *i))
            self._str_agg(' ')
            self._str_agg(self._rate_str % ('>' * int(count * 20 / config.count),
                        ' ' * (20 - int(count * 20 / config.count)),
                        str(count), str(config.count)))
            c_print(self.str_buffer.encode())
            self.str_buffer = ''
            count += 1

    def _to_pic(self):
        if not self.icmp.res:
            print('无可用记录')
            return
        x, y = zip(*self.icmp.res)
        if config.show_pic:
            show(x, y)
        print('保存中')
        save(x, y, self.dir, 'ICMP')
        print('运行完成')
        print(ascii_img)
        print('power by 【战斧奶牛】\n')
        os.system('pause')

    def run(self):
        # 执行前确定满足基本参数条件
        self._before_run()
        # 执行测速子线程
        self._add_job()
        # 执行主控制台子线程
        Thread(target=self._main_job).start()
        # 主线程监控键盘事件
        self.monitor.catch(self.icmp)
        # 生成图片
        self._to_pic()


if __name__ == '__main__':
    job = Job()
    job.run()
    # loop = LoopList(5)
    # for i in range(1, 20):
    #     loop.put(i)
    #     for j in loop.gen():
    #         print(j, end=' ')
    #     print('')

