import os
import re
import time

from typing import Tuple


class Icmp:
    target_ip: str
    _timeout: int = -1

    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.res = []

    def _finally_deal(self):
        max_delay = max(self.res or [0])
        for i in range(len(self.res)):
            self.res[i] = max_delay * 2

    def _ping(self) -> Tuple[str, int]:
        res = os.popen('ping %s -n 1 | findstr "ms" | findstr ":"' % self.target_ip).read()
        res = re.findall(r'=([\d]+)ms', res)
        return time.strftime('%m-%d %H:%M:%S'), int(res[0]) if res else self._timeout

    def first_ping(self) -> bool:
        res = os.popen('ping %s -n 1 | findstr "Ping"' % self.target_ip).read()
        print(res)
        return bool(re.findall(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}', res))

    def test(self, count: int, cell: float, sync_queue):
        for _ in range(count):
            self.res.append(self._ping())
            sync_queue.put(self._ping())
            time.sleep(cell)
        sync_queue.put('end')


if __name__ == '__main__':
    ...
