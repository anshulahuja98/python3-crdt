import os
import sys


def test():
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    src_path = root_path + "/src"
    file_path = root_path + "/tests/manual/" + sys.argv[1]
    os.system('python {}.py {}'.format(file_path, src_path))


if __name__ == "__main__":
    test()
