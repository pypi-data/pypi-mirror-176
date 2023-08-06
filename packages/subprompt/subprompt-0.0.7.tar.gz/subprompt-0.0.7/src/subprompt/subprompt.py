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
import argparse
from sys import argv, stderr
from colorama import init, Fore, Back, Style

init(autoreset=True)

class Filter:
    def __init__(self, args):
        self.replace_all = False
        self.quit_loop = False
        self.sub_count = 0
        self.match_count = 0

        self.regex = re.compile(args.regex)
        self.sub = args.r
        self.delete = args.d
        self.spread = args.n+1

        self.lines_to_delete = []

    def _number_lines(_, lines, start_n):
        return [Fore.YELLOW + Style.BRIGHT +
                str(n + start_n + 1) +
                Fore.RESET + Style.RESET_ALL +
                ':' + line
                for (n, line) in enumerate(lines)]

    def _prompt(self, matchobj, lines, line, line_n, fname):
        curr_match = matchobj.group(0)

        if self.quit_loop:
            return curr_match

        if not self.delete:
            replaced_match = self.regex.sub(self.sub, curr_match)

            if replaced_match == curr_match:
                return replaced_match

        self.match_count += 1

        if self.replace_all:
            self.sub_count += 1
            if self.delete:
                self.lines_to_delete.append(line_n)
                return None
            return replaced_match

        start_n = max(0, line_n - self.spread)
        end_n = min(len(lines)+1, line_n + self.spread)
        rel_line_n = line_n-start_n
        cut = lines[start_n:end_n]

        highlighted = line.replace(curr_match,
                Back.RED + curr_match + Back.RESET)

        cut_highlighted = cut
        cut_highlighted[rel_line_n] = highlighted
        cut_highlighted = self._number_lines(cut_highlighted, start_n)

        cut_replaced = cut

        if not self.delete:
            cut_replaced[rel_line_n] = line.replace(curr_match,
                    Back.YELLOW + Fore.BLACK + replaced_match + Back.RESET + Fore.RESET)
        else:
            cut_replaced.pop(rel_line_n)

        cut_replaced = self._number_lines(cut_replaced, start_n)

        print(Fore.GREEN + Style.BRIGHT + fname)

        print(''.join(cut_highlighted))
        print('Becomes the following:')
        print()
        print(''.join(cut_replaced))


        while True:
            answer = input('Confirm the change? [Y/n/a/q] ').lower()

            if answer in ['y', 'yes', '']:
                self.sub_count += 1
                print()
                if self.delete:
                    self.lines_to_delete.append(line_n)
                    return None
                return replaced_match

            elif answer in ['n', 'no']:
                print()
                return curr_match

            elif answer in ['a', 'all']:
                self.sub_count += 1
                self.replace_all = True
                if self.delete:
                    self.lines_to_delete.append(line_n)
                    return None
                return replaced_match

            elif answer in ['q', 'quit']:
                self.quit_loop = True
                return curr_match

            print('Invalid answer. Please type again.')

    def filter_file(self, fname):
        with open(fname, 'r') as file:
            contents = file.read()

        lines = contents.splitlines(keepends=True)

        lines = [
                    self.regex.sub(
                        lambda matchobj: self._prompt(matchobj, lines, line, line_n, fname),
                        line
                    )
                    for (line_n, line) in enumerate(lines)
                ]

        if self.delete:
            for line in reversed(self.lines_to_delete):
                lines.pop(line)

            self.lines_to_delete = []

        new_contents = ''.join(lines)

        hash_old = hashlib.md5(contents.encode())
        hash_new = hashlib.md5(new_contents.encode())

        if hash_old.digest() != hash_new.digest():
            with open(fname, 'w') as file:
                file.write(new_contents)

def run(args):
    parser = argparse.ArgumentParser(description='Modifies lines matched by a regex interactively')
    parser.add_argument('regex', metavar='REGEX', type=str)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-d', help='delete line', action='store_true')
    action.add_argument('-r', help='replace match with expression', type=str)
    parser.add_argument('files', metavar='FILES', nargs='+', type=str)
    parser.add_argument('-n', help='size of lines preview (default=3)', type=int, default=3)

    args = parser.parse_args(args)

    filter_obj = Filter(args)

    for file in args.files:
        # Check if file is writable
        if os.access(file, os.W_OK):
            filter_obj.filter_file(file)

            if filter_obj.quit_loop:
                break
        else:
            print('WARNING: File {0} is not writable. Skipping...'.format(file))

    if filter_obj.match_count == 0:
        print(Fore.RED + Style.BRIGHT + 'No matches found.')
    else:
        print(Fore.YELLOW + Style.BRIGHT + 'Made {0} of {1} substitutions.'
                .format(Fore.WHITE + str(filter_obj.sub_count) + Fore.YELLOW,
                        Fore.WHITE + str(filter_obj.match_count) + Fore.YELLOW))

def main():
    run(argv[1:])

if __name__ == '__main__':
    main()
