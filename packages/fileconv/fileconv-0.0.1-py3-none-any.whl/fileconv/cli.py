"""
This script will convert .txt , .docx or .doc & .xlsx or .xls / .csv to .pdf
It uses 'fpdf', 'docx2pdf' & 'win32' to execute this task.

The programm crawls over one directory with (possible multiple) subdirectories and identifies files, by their extension and converts them to pdf, while leaving the old ones 


@Author: ovanov
@Date: 26.03.21
"""

import os
import argparse
import sys
import pathlib
from typing import Dict

from tqdm.std import tqdm


from .Converter import Convert

def argument_parser() -> Dict:
    parser = argparse.ArgumentParser('fileconv',description='Command line tool for file conversion to PDF. Supports MS Word, Excel and txt files.')
    parser.add_argument('infile',
    help='This argument should be a filepath to the directory, which should be parsed',
    type=str,
    default=sys.stdin)

    parser.add_argument('--output', '-o',
    help='(required) Give the path and the name of the output directory.',
    nargs='?',
    type=str,
    default=False)

    return parser


def crawler(p, output):
    """
    This function takes the path variable "p" and goes over all directories 
    """
    dir_len = len(next(os.walk(p))[1])
    for root, dirs, files in tqdm(os.walk(p), total=dir_len):
        #os.walk yields a 3-tuple of strings, wich can be concatenated
        if len(root) != 0:
            # maybe the directory is empty or yields no files (empty list), we should make sure that there is no error
            for filename in files:

                ext = pathlib.Path(filename).suffix # get file extension

                if ext == ".docx" or ext == ".doc":
                    file = os.path.join(root, filename)
                    Convert.word_to_pdf(file, ext, filename, output)

                elif ext == ".xlsx" or ext == ".xls":
                    file = os.path.join(root, filename)
                    Convert.excel_to_pdf(file, ext, filename, output)

                elif ext == ".txt":
                    file = os.path.join(root, filename)
                    Convert.txt_to_pdf(file, filename, output)
                
                else:
                    pass
    
        else:
            raise KeyError("The directory is empty")
    return


def main():
    """
    Change the "path" variable, in order to pass the directory
    """
    # get argument parser
    parser = argument_parser()
    args = parser.parse_args()
    args_dict = {
        arg: value for arg, value in vars(args).items()
        if value is not None
    }

    if len(args_dict['infile']) < 1: 
        raise KeyError('Please give a path to a file or a dirctory path.')

    path = args_dict['infile']
    output = args_dict['output']


    crawler(path, output)
    return

if __name__ == "__main__":
    main()
