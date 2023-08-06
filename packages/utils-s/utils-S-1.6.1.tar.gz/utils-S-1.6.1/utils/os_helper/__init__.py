from .paths import *


def get_current_home_dir():
    return os.path.expanduser('~')


def execute_capture(command):
    os_exec = os.popen(command).read()
    return os_exec


def get_ip():
    return os.popen('ipconfig getifaddr en0').read()[:-1]


def waste():
    pass