from unittest import TestCase
import os
import sys

if sys.version_info[0] == 3:
    from pathlib import Path
else:
    from pathlib2 import Path
    ModuleNotFoundError = ImportError

try:
    import xlsxreader
    print('what the fuck?!')

except ModuleNotFoundError:
    sys.path.append('..')
    import xlsxreader
    print('I am lost')

if 'test' in os.listdir('.'):
    os.chdir('./test')
print('whats')
test_file = xlsxreader.readxlsx('testboo1.xlsx')
#print(str(test_file.read(), encoding="utf-8"))
