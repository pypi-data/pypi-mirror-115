from .paths import *

def get_current_home_dir():
    return os.path.expanduser('~')

def execute_capture(command):
    exec = os.popen(command).read()
    return exec

def get_ip():
    return os.popen('ipconfig getifaddr en0').read()

def waste():
    pass