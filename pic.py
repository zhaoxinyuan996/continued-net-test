import os
import time
import matplotlib.pyplot as plt

flag = False


def _common(x, y):
    global flag
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.3)
    flag = True


def show(x, y):
    if not flag:
        _common(x, y)
    plt.show()


def save(x, y, dir, protocol):
    if not flag:
        _common(x, y)
    plt.savefig(os.path.join(dir, '%s-%s.jpg' % (protocol, time.strftime('%d_%H_%M_%S'))))

if __name__ == '__main__':
    plt.plot([1,2,3,3,4],[1,2,3,4,5])
    plt.xticks(rotation=45)
    plt.show()