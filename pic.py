import os
import time
import matplotlib.pyplot as plt

flag = False


def _common(x, y):
    global flag
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(x,y)
    plt.xlabel("时间")
    plt.ylabel("延迟(ms)")
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.3)
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
    plt.plot([1,2,3,3,4],[1,2,3,4,5])
    plt.xticks(rotation=45)
    plt.show()