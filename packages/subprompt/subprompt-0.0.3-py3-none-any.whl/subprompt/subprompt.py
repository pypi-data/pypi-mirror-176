#!/bin/python3.9

#
#   subprompt is a script to replace matches of a Regex across files
#   with a confirmation prompt.
#   Copyright (C) 2022  Augusto Lenz Gunsch
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#   Contact information available in my website: https://augustogunsch.com
#

import re
import hashlib
import os
from sys import argv, stderr
from os.path import basename
from colorama import init, Fore, Back, Style

init(autoreset=True)

class Filter:
    def __init__(self, regex, sub):
        self.replace_all = False
        self.quit_loop = False
        self.sub_count = 0
        self.match_count = 0

        self.regex = re.compile(regex)
        self.sub = sub

    def _prompt(self, matchobj, line, line_n, fname):
        curr_match = matchobj.group(0)

        if self.quit_loop:
            return curr_match

        replaced_match = self.regex.sub(self.sub, curr_match)

        if replaced_match == curr_match:
            return replaced_match

        self.match_count += 1

        if self.replace_all:
            self.sub_count += 1
            return replaced_match

        highlighted = line.replace(curr_match,
                Back.RED + curr_match + Back.RESET)
        replaced = line.replace(curr_match,
                Back.YELLOW + Fore.BLACK + replaced_match + Back.RESET + Fore.RESET)

        print(Fore.GREEN + Style.BRIGHT + fname)

        print(Fore.YELLOW + Style.BRIGHT + str(line_n), end='')
        print(':{0}'.format(highlighted))

        print('Becomes the following:')

        print(Fore.YELLOW + Style.BRIGHT + str(line_n), end='')
        print(':{0}'.format(replaced))

        print()

        while True:
            answer = input('Confirm the change? [Y/n/a/q] ').lower()

            if answer in ['y', 'yes', '']:
                self.sub_count += 1
                print()
                return replaced_match

            elif answer in ['n', 'no']:
                print()
                return curr_match

            elif answer in ['a', 'all']:
                self.sub_count += 1
                self.replace_all = True
                return replaced_match

            elif answer in ['q', 'quit']:
                self.quit_loop = True
                return curr_match

            print('Invalid answer. Please type again.')

    def filter_file(self, fname):
        with open(fname, 'r') as file:
            contents = file.read()

        lines = contents.splitlines()

        lines = [
                    self.regex.sub(
                        lambda matchobj: self._prompt(matchobj, line, line_n, fname),
                        line
                    )
                    for (line_n, line) in enumerate(lines)
                ]

        new_contents = '\n'.join(lines)

        hash_old = hashlib.md5(contents.encode())
        hash_new = hashlib.md5(new_contents.encode())

        if hash_old.digest() != hash_new.digest():
            with open(fname, 'w') as file:
                file.write(new_contents)
                file.write('\n')

def run(args):
    if len(args) < 3:
        print('usage: {0} [REGEX] [SUB] [FILES...]'.format(basename(__file__)), file=stderr)
        exit(1)

    regex = args[0]
    sub = args[1]
    files = args[2:]

    filter_obj = Filter(regex, sub)

    for file in files:
        # Check if file is writable
        if os.access(file, os.W_OK):
            filter_obj.filter_file(file)

            if filter_obj.quit_loop:
                break

    if filter_obj.match_count == 0:
        print(Fore.RED + Style.BRIGHT + 'No matches found.')
    else:
        print(Fore.YELLOW + Style.BRIGHT + 'Made {0} of {1} substitutions.'
                .format(Fore.WHITE + str(filter_obj.sub_count) + Fore.YELLOW,
                        Fore.WHITE + str(filter_obj.match_count) + Fore.YELLOW))

def main():
    argv.pop(0)
    run(argv)

if __name__ == '__main__':
    main()
