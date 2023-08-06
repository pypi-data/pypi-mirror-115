import os
import shutil

def get_last_component(string:str):
    Broken = string.split('/')
    length = len(Broken)

    return Broken[length - 1]

def basePath(URL):
    if URL.endswith('/'):
        URL = URL[:-1]

    Broken = URL.split('/')
    length = len(Broken)

    LastItem = Broken[length - 1]
    NewPath = ''

    for path in Broken:
        Bad = [LastItem, '']

        continuee = False

        for b in Bad:
            if path == b:
                continuee = True

        if continuee:
            continue


        NewPath = NewPath + '/' + path

    return NewPath


def file_exists(path):
    return os.path.isfile(path)

def directory_exists(path):
    return os.path.isdir(path)

def os_walk(file_name, path):
    for r, d, f in os.walk(path):
        for file in f:
            if file == file_name:
                return os.path.abspath(os.path.join(r, file))


def copy(src, dst):
    if os.path.isdir(src):
        if dst.endswith('/'):
            dst = dst + get_last_component(src)
        elif not dst.endswith('/'):
            dst = dst + '/' + get_last_component(src)
        return shutil.copytree(src=src, dst=dst)
    else:
        return shutil.copy(src=src, dst=dst)


if __name__ == '__main__':
    pass