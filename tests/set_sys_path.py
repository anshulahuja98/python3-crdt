import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
src_path = root_path + "/src"
sys.path.insert(0, src_path)
