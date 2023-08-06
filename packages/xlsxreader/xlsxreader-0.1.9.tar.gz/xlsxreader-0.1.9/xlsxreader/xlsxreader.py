
import zipfile
import sys
import shutil
from xml.etree import cElementTree as ET
import time
from datetime import datetime, timedelta
import tempfile

EXCEL_STARTDATE = datetime(1899, 12, 30)
# all date styles, there are other styles like fractions etc. so have sort only dates
date_styles = [
    "14",
    "164",
    "165",
    "166",
    "167",
    "168",
    "169",
    "170",
    "171",
    "172",
    "173",
    "174",
    "175",
    "176",
    "177",
    "178",
    "179",
    "180",
    "181",
    "182",
    "183",
    "184",
    "186",
    "187",
    "188",
    "190",
]

# unicode is a python27 object that was merged into str in 3+, for compatibility it is redefined here
if sys.version_info[0] < 3:
    FileNotFoundError = IOError
    PermissionError = Exception
    WindowsError = Exception
    FileExistsError = Exception
    import cgi as html

    PYVER = 2
else:
    unicode = str
    WindowsError = Exception
    import html

    PYVER = 3


def readxlsx(file_name,worksheet_to_read_index=1, return_file_name='unamed',return_file_suffix='.csv', return_file_delete=False,delimiter=',',quote_char='"',end_of_record='\n'):
    """Reads an .xlsx file and returns a python tempfile"""
    #try:
    if True: 
        with zipfile.ZipFile(file_name) as f_zip:

            worksheets = load_workbook(f_zip)
            shared_strings = get_sharedStrings(f_zip)
            styles = get_styles(f_zip)
            temp_file = temp_file = tempfile.NamedTemporaryFile(
                prefix=return_file_name, suffix=return_file_suffix, delete=return_file_delete
            )
            data = scrape(f_zip, worksheets[worksheet_to_read_index]["sheet_path"], shared_strings, styles)
    #except:
    #    return None

    max_row, max_column = data["max_address"]

    for r in range(1, max_row + 1):
        for c in range(1, max_column):
            try:
                value = data[(r, c)]   
            except KeyError:
                value = ""
            temp_file.write(bytes(value + delimiter, encoding="utf-8")) if delimiter not in value else temp_file.write(bytes(quote_char + value + quote_char + delimiter, encoding="utf-8"))
        try:
            value = data[(r, max_column)]
        except KeyError:
            value = ""
        temp_file.write(bytes(value + end_of_record, encoding="utf-8")) if delimiter not in value else temp_file.write(bytes(quote_char + value + quote_char + end_of_record, encoding="utf-8"))

    return temp_file

def load_workbook(f_zip):

    worksheets = {}

    root, ns = get_parsed_root(f_zip, "xl/workbook.xml")
    # worksheet data is stored in sheet1.xml, sheet2.xml ...
    # rId_targets is map of {rId: sheet%.xml}
    rId_targets = get_named_worksheet_rel(f_zip)

    for elem in root.findall("./default:sheets/default:sheet", ns):
        try:
            rId = elem.get("{" + ns["r"] + "}id")
        except KeyError:
            rId = elem.get("id")
        worksheets[int(rId.replace("rId", ""))] = {
            "name": elem.get("name"),
            "sheet_path": rId_targets[rId],
        }

    return worksheets


def get_named_worksheet_rel(f_zip):

    rId_targets = {}

    root, ns = get_parsed_root(f_zip, "xl/_rels/workbook.xml.rels")

    for elem in root.findall("./default:Relationship", ns):
        rId_targets[elem.get("Id")] = elem.get("Target")

    return rId_targets


def get_sharedStrings(f_zip):

    shared_strings = {}

    if "xl/sharedStrings.xml" not in f_zip.NameToInfo.keys():
        return shared_strings

    root, ns = get_parsed_root(f_zip, "xl/sharedStrings.xml")

    for i, tag_si in enumerate(root.findall("./default:si", ns)):
        tag_t = tag_si.findall("./default:r//default:t", ns)
        if tag_t:
            text = "".join([tag.text for tag in tag_t])
        else:
            text = tag_si.findall("./default:t", ns)[0].text
        shared_strings.update({i: text})

    return shared_strings


def get_styles(f_zip):

    styles = {0: "0"}

    if "xl/styles.xml" not in f_zip.NameToInfo.keys():
        return styles

    root, ns = get_parsed_root(f_zip, "xl/styles.xml")
    for i, elem in enumerate(root.findall("./default:cellXfs", ns)[0]):
        styles.update({i: elem.get("numFmtId")})

    return styles


def scrape(f_zip, worksheet_path, shared_strings, styles):

    data = {}

    root, ns = get_parsed_root(f_zip, "xl/" + worksheet_path)

    max_address = (0, 0)

    for elem in root.findall("./default:sheetData/default:row/default:c", ns):

        address = address_converter(elem.get("r"))
        elem_type = elem.get("t")
        style = int(elem.get("s")) if elem.get("s") is not None else 0
        value_elem = elem.find("./default:v", ns)
        value = value_elem.text if value_elem is not None else ""

        if value == "":
            continue
        elif elem_type == "str" or elem_type == "e":
            pass
        elif elem_type == "s":
            value = shared_strings[int(value)]
        elif elem_type == "b":
            value = "True" if value == "1" else "False"
        else:
            test_value = value if "-" not in value else value[1:]
            if test_value.isdigit():
                if styles[style] in date_styles:
                    value = str(EXCEL_STARTDATE + timedelta(days=int(value)))
                else:
                    value = str(value)
            else:
                if styles[style] in date_styles:
                    partialday = float(value) % 1
                    value = str(EXCEL_STARTDATE + timedelta(days=int(value.split('.')[0]), seconds=partialday * 86400))
                else:
                    value = str(value)

        if address[0] > max_address[0]:
            max_address = (address[0], max_address[1])
        if address[1] > max_address[1]:
            max_address = (max_address[0], address[1])

        data.update({address: value})
    data.update({"max_address": max_address})
    return data


def address_converter(cell_address):

    i = 0
    while cell_address[i].isalpha():
        i += 1
    row = int(cell_address[i:])
    column = column_to_num(cell_address[:i])

    return (row, column)


def get_parsed_root(f_zip, path):

    with f_zip.open(path, "r") as file:
        ns = get_register_namespace(file)
    with f_zip.open(path, "r") as file:
        tree = ET.parse(file)
        root = tree.getroot()

    return root, ns


def get_register_namespace(file):

    events = "start", "start-ns"

    ns_map = []

    for event, elem in ET.iterparse(file, events):
        if event == "start-ns":
            elem = ("default", elem[1]) if elem[0] == "" else elem
            ns_map.append(elem)
        if event == "start":
            break
    ns = dict(ns_map)
    if "default" not in ns.keys():
        ns["default"] = ns["x"]

    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)

    return ns


def column_to_num(column_name):

    pos = len(column_name) - 1
    val = 0
    try:
        val = (ord(column_name[0].upper()) - 64) * 26 ** pos
        next_val = column_to_num(column_name[1:])
        val = val + next_val
    except IndexError:
        return val

    return val
