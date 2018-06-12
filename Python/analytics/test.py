import os
import subprocess
from shutil import copy
from itertools import chain



paths = ('D:\\1', 'D:\\3')
for root, dirnames, filenames in chain.from_iterable(os.walk(path) for path in paths):
    for filename in filenames:
        print(str(root)+str(filename))