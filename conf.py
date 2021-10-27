import yaml
import argparse
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Union, Callable

parser = argparse.ArgumentParser()
parser.usage = '123'
parser.add_argument("-n", "--count", help='执行次数')
parser.add_argument("-P", "--port", help='端口号(icmp协议不需要)')
parser.add_argument("-p", "--protocol", choices=('icmp', ), help='协议选择，可选icmp')
params = parser.parse_args()


class Config(BaseModel):
    port: Optional[int]
    count: int
    target_ip: str
    protocol: List[str]
    cell: float
    row_num: int
    show_pic: bool
    pic_dir: str
    string_length: int
    range: Union[str, Callable]

    def __init__(self):
        dic = {}
        with open('config.yml', encoding='utf-8') as f:
            dic.update(yaml.load(f.read(), Loader=yaml.SafeLoader))
        dic.update({k: v for k, v in params.__dict__.items() if v is not None})
        super(Config, self).__init__(**dic)
        exec('self.range=lambda i:' + self.range)


try:
    config = Config()
except ValidationError as e:
    print('请确认yaml或命令行包含以下参数！')
    print('\n'.join([i['loc'][0] for i in e.errors()]))

if __name__ == '__main__':
    config = Config()
