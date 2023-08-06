import unittest
import os
import sys

if sys.version_info[0] == 3:
    from pathlib import Path
else:
    from pathlib2 import Path
    ModuleNotFoundError = ImportError

try:
    from xlsxreader import readxlsx

except ModuleNotFoundError:
    sys.path.append('..')
    from xlsxreader import readxlsx

if 'test' in os.listdir('.'):
    os.chdir('./test')

class TestXlsxReaderOutput(unittest.TestCase):
    
    def test_file_path_output(self):
        self.maxDiff = None
        with open('./testbook1.csv', encoding='utf-8-sig') as file:
            correct_out = file.read()
        #print(correct_out)
        #for i in range(10): print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        test_file = readxlsx('./testbook1.xlsx')
        test_file.seek(0)
        test_out = str(test_file.read(), encoding='utf-8')
        #print(test_out)
        self.assertEqual(correct_out, test_out)

if __name__ == '__main__':
    unittest.main()