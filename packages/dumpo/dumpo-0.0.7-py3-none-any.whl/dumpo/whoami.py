import os
import sys

def whoami():
    print(f'__file__={__file__}')
    print(f'sys.path={sys.path}')
    return __file__
