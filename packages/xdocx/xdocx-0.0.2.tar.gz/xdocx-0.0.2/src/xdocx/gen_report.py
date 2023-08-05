import argparse
import os 
from . import docx_util
from . import template_data

def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('test_case_file', nargs='?', default=None)


def run(options: argparse.Namespace) -> int:
    if os.path.isfile(options.test_case_file) == False:
        print("not test case file.please check your input")
        return 0

    template_data.template_file_gen.generate_template_file()

    xlsx_file_handle = docx_util.get_xlsx_data(options.test_case_file)
    test_case_data = xlsx_file_handle.get_all_testcase()
    report_file_handle = docx_util.write_test_record("template_data.docx","output_report.docx")
    report_file_handle.write_record(test_case_data)
    template_data.template_file_gen.remove_template_file()
    print("finish.")
    return 0