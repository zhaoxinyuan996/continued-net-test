import os
import time

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

flag = False


def _common(x, y):
    global flag
    length = len(x)
    print(11111, int(length / 20))
    if length > 200:
        plt.figure(figsize=(int(length / 20), 6))
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(x, y)
    plt.xlabel("时间")
    plt.ylabel("延迟(ms)")
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.3)
    plt.tick_params(labelsize=8)

    ax = plt.gca()
    if length > 200:
        xmajorLocator = MultipleLocator(int(length / 100))  # 刻度间隔
    else:
        xmajorLocator = MultipleLocator(5)  # 刻度间隔
    # 设置主刻度标签的位置,标签文本的格式
    ax.xaxis.set_major_locator(xmajorLocator)
    flag = True


def show(x, y):
    if not flag:
        _common(x, y)
    plt.show()


def save(x, y, dir, protocol):
    if not flag:
        _common(x, y)
    plt.savefig(os.path.join(dir, '%s-%s.jpg' % (protocol, time.strftime('%m_%d_%H_%M_%S'))))


if __name__ == '__main__':
    show([str(i) for i in range(20000)], [1,2,3,3,4,3,4,2,5,4] * 2000)
