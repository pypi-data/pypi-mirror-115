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
    
    def test_path_dates_styles_output(self):
        with open('./testbook1.csv', encoding='utf-8-sig') as file:
            correct_out = file.read()
        test_file = readxlsx('./testbook1.xlsx')
        test_file.seek(0)
        test_out = str(test_file.read(), encoding='utf-8')
        self.assertEqual(correct_out, test_out)

    def test_path_large_input_output(self):
        with open('./testbook2.csv', encoding='utf-8-sig') as file:
            correct_out = file.read()
        test_file = readxlsx('./testbook2.xlsx')
        test_file.seek(0)
        test_out = str(test_file.read(), encoding='utf-8')
        with open('test.txt', 'w') as file:
            file.write(test_out)
        self.assertEqual(correct_out, test_out)

if __name__ == '__main__':
    unittest.main()