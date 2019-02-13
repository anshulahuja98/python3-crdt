import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def set_sys_path():
    src_path = root_path + "/src"
    sys.path.insert(0, src_path)


def test():
    src_path = root_path + "/src"
    file_path = root_path + "/tests/manual/" + sys.argv[1]
    os.system('python {}.py {}'.format(file_path, src_path))


if __name__ == "__main__":
    set_sys_path()
    test()
