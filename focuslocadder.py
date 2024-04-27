import re
import argparse
import logging

#############################
###
### HoI 4 Focus Localisation Adder, created by Thanasis Lanaras
### Written in Python 3.12.0
###
###    Copyright 2023 Thanasis Lanaras.
###    Licensed under the Apache License, Version 2.0 (the "License");
###    you may not use this file except in compliance with the License.
###    You may obtain a copy of the License at
###
###    http://www.apache.org/licenses/LICENSE-2.0
###
###    Unless required by applicable law or agreed to in writing, software
###    distributed under the License is distributed on an "AS IS" BASIS,
###    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
###    See the License for the specific language governing permissions and
###    limitations under the License.

#############################################################
###
### usage: focuslocadder.py [-h] input output
### 
### Given an national focus file, it adds missing localisation entries
### to a specified localisation file. 
### Note: custom tooltips are not supported. (Planned for future)
### For it to find a focus, the id field should be **immediately after** 
### the focus = { line. Else, it won't be read.
### 
### Positional arguments:
###   input       National Focus file to parse
###   output      Localisation file to write to (must be utf-8-bom)
### 
### Optional arguments:
###   -h, --help  show this help message and exit
###
#############################################################

class FocusLocAdder:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def extract_focus_ids(self):
        focus_ids = []
        inside_focus = False
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                for line in file:
                    if 'focus = {' in line:
                        inside_focus = True
                    elif inside_focus and '}' in line:
                        inside_focus = False
                    elif inside_focus and 'id =' in line:
                        focus_id = re.search(r'id = (.*?)\s', line)
                        if focus_id:
                            focus_ids.append(focus_id.group(1).strip('"'))
                            inside_focus = False  # Set inside_focus to False after extracting the ID
                        else:
                            logging.warning(f"Malformed 'id' field in line: {line.strip()}")
        except FileNotFoundError:
            logging.error(f"File not found: {self.input_file}")
        return focus_ids

    def update_output_file(self):
        focus_ids = self.extract_focus_ids()

        try:
            with open(self.output_file, 'a', encoding='utf-8-sig') as file:
                for focus_id in focus_ids:
                    id_entry = f'{focus_id}: ""\n'
                    desc_entry = f'{focus_id}_desc: ""\n'

                    with open(self.output_file, 'r', encoding='utf-8') as output_file_reader:
                        content = output_file_reader.read()
                        if focus_id not in content:
                            file.write(id_entry)
                        if f'{focus_id}_desc' not in content:
                            file.write(desc_entry)
        except FileNotFoundError:
            logging.error(f"File not found: {self.output_file}")

    def process_files(self):
        self.update_output_file()
        logging.info("Focus tree file successfully updated.")

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Given a national focus file, it adds missing localisation entries to a specified localisation file. Note: custom tooltips are not supported. (Planned for future) For it to find a focus, the id field should be **immediately after**  the focus = { line. Else, it won\'t be read.')
    parser.add_argument('input_file', help='Path to the input file.')
    parser.add_argument('output_file', help='Path to the output file.')

    args = parser.parse_args()
    focus_adder = FocusLocAdder(args.input_file, args.output_file)
    focus_adder.process_files()

if __name__ == "__main__":
    main()
