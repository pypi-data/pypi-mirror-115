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

except ModuleNotFoundError:
    sys.path.append('..')
    import  xlsxreader

if 'test' in os.listdir('.'):
    os.chdir('./test')

test_file = xlsxreader.readxlsx("testbook1.xlsx")
print(str(test_file.read(), encoding="utf-8"))
