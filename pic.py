import os
import time

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

flag = False
length_edge = 1600  # 画布限制，2 ^ 16像素内，这里直接限制了最长

def _common(x, y, datail_graph):
    global flag
    length = len(x)
    if datail_graph:
        if length > length_edge:
            plt.figure(figsize=(400, 6))
        else:
            plt.figure(figsize=(int(length / 5), 6))
    plt.xlim(0, len(x) - 1)
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    plt.rcParams['axes.unicode_minus'] = False

    plt.plot(x, y)
    plt.ylabel("延迟(ms)")
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.3)
    plt.tick_params(labelsize=8)

    ax = plt.gca()
    if datail_graph:
        if length > length_edge:
            step = 1
            while int(length / 2000):
                step += 1
                length -= 2000
            xmajorLocator = MultipleLocator(step)  # 刻度间隔
        else:
            xmajorLocator = MultipleLocator(1)  # 低于1600条 画布长度自适应
        # 设置主刻度标签的位置,标签文本的格式
        ax.xaxis.set_major_locator(xmajorLocator)
    flag = True


def show(x, y, step):
    if not flag:
        _common(x, y, step)
    plt.show()


def save(x, y, dir, protocol, step):
    if not flag:
        _common(x, y, step)
    plt.savefig(os.path.join(dir, '%s-%s.jpg' % (protocol, time.strftime('%m_%d_%H_%M_%S'))))


if __name__ == '__main__':
    show([str(i) for i in range(170)], [1,2,3,3,4,3,4,2,5,4] * 17, 1)
