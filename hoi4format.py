#!/usr/bin/python3
import argparse
import os
import re
import glob
import sys

#############################
###
### HoI 4 File Formatter by Yard1, originally for Equestria at War mod
### Classes added by thanasislanaras
### Written in Python 3.5.2
###
### Copyright (c) 2017 Antoni Baum (Yard1)
### Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
### The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###
### usage: hoi4Formatter.py [-h] [-r] [--extensions [EXTENSIONS [EXTENSIONS ...]]]
###                         input
###
### Given a file or folder, format files to follow proper PDX-style indentation. Only indentation is changed.
###
### positional arguments:
###   input                 Technology file name/folder containing files
###
### optional arguments:
###   -h, --help            show this help message and exit
###   -ws, --whitespace     ONLY remove whitespace at the end of the line without
###                         formatting (Default: False)
###   -ic, --ignore_comments
###                         Ignore lines which start with # (or whitespace #)
###                         (Default: False)
###   -r, --recursive       Format files in directories recursively (Default:
###                         False)
###   --extensions [EXTENSIONS [EXTENSIONS ...]]
###                         Which file extensions should be formatted (Default:
###                         .txt .gfx)
###
#############################

class HOI4FileFormatter:
    def __init__(self, args):
        self.args = args
        self.counter = 0

    @staticmethod
    def readable_dir(prospective_dir):
        if not os.path.isdir(prospective_dir):
            raise Exception("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            return prospective_dir
        else:
            raise Exception("readable_dir:{0} is not a readable dir".format(prospective_dir))

    def format_file(self, name):
        print("Reading file " + name + "...")
        with open(name, "r") as f:
            lines = f.read().splitlines()
        names = list()
        new_lines = list()
        open_blocks = 0
        for line in lines:
            if self.args.ignore_comments and re.match("^\s*#", line):
                new_lines.append(line)
                continue
            if self.args.whitespace:
                line = re.sub(r"\s*$", "", line)
                new_lines.append(line)
                continue
            line = line.strip()
            if line == "}":
                line = ('\t' * (open_blocks - 1)) + line
            else:
                line = ('\t' * open_blocks) + line
            line = re.sub(r"\s*$", "", line)
            new_lines.append(line)
            open_blocks += re.sub(r'\".*?\"', '', line).count('{')
            open_blocks -= re.sub(r'\".*?\"', '', line).count('}')
        with open(name, "w") as f:
            f.writelines(str(line) + "\n" for line in new_lines)

    def process_files(self):
        try:
            directory = self.readable_dir(self.args.input)
            is_dir = True
        except:
            print("Not a directory, treating as a file.")
            is_dir = False

        if is_dir:
            if self.args.recursive:
                for file in glob.glob(directory+"/**/*.*", recursive=True):
                    if os.path.splitext(file)[1] in self.args.extensions:
                        try:
                            self.format_file(file)
                            self.counter += 1
                        except:
                            pass
            else:
                for file in glob.glob(directory+"/*.*"):
                    if os.path.splitext(file)[1] in self.args.extensions:
                        try:
                            self.format_file(file)
                            self.counter += 1
                        except:
                            pass
        else:
            self.format_file(self.args.input)
            self.counter += 1
        print("Finished, %s files formatted" % self.counter)


def main():
    if not sys.version_info >= (3, 0):
        sys.exit("Wrong Python version. Version 3.0 or higher is required to run this script!")

    parser = argparse.ArgumentParser(description='Given a file or folder, format files to follow proper PDX-style indentation. Only indentation is changed.')
    parser.add_argument('input', metavar='input', help='Technology file name/folder containing files')
    parser.add_argument('-ws', '--whitespace', action='store_true', required=False, default=False,
                        help='ONLY remove whitespace at the end of the line without formatting (Default: False)')
    parser.add_argument('-ic', '--ignore_comments', action='store_true', required=False, default=False,
                        help='Ignore lines which start with # (or whitespace #) (Default: False)')
    parser.add_argument('-r', '--recursive', action='store_true', required=False, default=False,
                        help='Format files in directories recursively (Default: False)')
    parser.add_argument("--extensions", nargs="*", type=str, required=False, default=[".txt", ".gfx"],
                        help='Which file extensions should be formatted (Default: .txt .gfx)')

    args = parser.parse_args()
    formatter = HOI4FileFormatter(args)
    formatter.process_files()


if __name__ == "__main__":
    main()
