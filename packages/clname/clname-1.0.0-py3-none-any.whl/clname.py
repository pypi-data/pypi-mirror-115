#!/usr/bin/python3
"""
clname, version 1.0 - Cleans filenames to make them shell-friendly
                      (written for GNU/Linux distributions)
Copyright (C) 2021 Stefan Lepperdinger

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import sys
import re
import argparse

VERSION = '1.0'

# These characters will be removed from the filename
BAD_CHARACTERS = ' \n\t\\[]{}():;"\'<>?|=!$^&*`'


def clean_string(string):
    """Replaces bad characters, i.e., characters in `BAD_CHARACTERS`, with
    underscores and then removes multiple underscores, underscores at the
    beginning, and underscores at the end of `string` if `string` is
    non-empty. Returns an empty string if the input string `string` is
    empty. Returns '_' if `string` is not empty but every character of the
    string is in `BAD_CHARACTERS`.

    :param string: string to be cleaned
    :type string: str

    :return: cleaned string
    :rtype: str

    Examples:

    >>> clean_string('test test')
    'test_test'

    >>> clean_string('')
    ''

    >>> clean_string('     ')
    '_'

    >>> clean_string('()?_[]*')
    '_'

    >>> clean_string('[2341]    hm?   <test>    ')
    '2341_hm_test'

    >>> clean_string('__main__')
    'main'
    """
    if string:
        # Replacing bad characters with underscores
        for character in BAD_CHARACTERS:
            string = string.replace(character, '_')

        # Removing multiple underscores
        string = re.sub(r'_{2,}', '_', string)

        # Removing underscore at the beginning
        string = re.sub(r'^_', '', string)

        # Removing underscore at the end
        string = re.sub(r'_$', '', string)

        # If every character of `string` was in `BAD_CHARACTER`, `string`
        # should be `_` and not empty.
        string = string if string else '_'

    return string


def yes_no_question(question):
    assert type(question) == str, '`question` is not a string.'
    try:
        answer = input(question)
        answered_yes = answer.lower() in ("y", "yes")
    except EOFError:
        answered_yes = False
        print()
    return answered_yes


class File:
    """Objects constructed via this class represent files."""
    def __init__(self,
                 path='',
                 is_directory=None):
        """
        :param path: Path of the file.
        :type path: str

        :param is_directory: True if file is a directory. `is_directory` gets
                             evaluated via `os.path.isdir` if `is_directory` is
                             None.
        :type is_directory: bool or None
        """
        self.path = os.path.normpath(path)
        self.is_directory = (os.path.isdir(path) if is_directory is None
                             else is_directory)
        self.exists = os.path.exists(path)
        self.is_symlink = os.path.islink(path)
        (
            self.is_hidden,
            self.filename,
            self.file_extension,
            self.parent_directory_path
        ) = self.__parse_file_path()

    def __parse_file_path(self):
        # Extracting the filename and the path of its parent directory
        file_path_split = self.path.split('/')
        parent_directory_path = '/'.join(file_path_split[:-1])
        filename_with_extension = file_path_split[-1]

        # Checking if file is hidden, i.e., filename starts with '.'
        if filename_with_extension.startswith('.'):
            is_hidden = True
            filename_with_extension = filename_with_extension[1:]
        else:
            is_hidden = False

        # Extracting the filename extension if it exists
        if '.' in filename_with_extension and not self.is_directory:
            filename_with_extension_split = filename_with_extension.split('.')
            filename = '.'.join(filename_with_extension_split[:-1])
            extension = filename_with_extension_split[-1]
        else:
            filename = filename_with_extension
            extension = None

        return is_hidden, filename, extension, parent_directory_path

    def get_cleaned_file_path(self, rename_extension):
        """Returnes the cleaned path of the file.

        :param rename_extension: if True, also renames the filename extension
                                 (in the case that the file isn't a directory)
        :type rename_extension: bool

        Examples:

        >>> path_1 = '/home/us er/[2021-07-07] - this is a  test    .tx t'

        >>> is_directory = False
        >>> rename_extension = False
        >>> File(path_1, is_directory).get_cleaned_file_path(rename_extension)
        '/home/us er/2021-07-07_-_this_is_a_test.tx t'

        >>> is_directory = True
        >>> rename_extension = False
        >>> File(path_1, is_directory).get_cleaned_file_path(rename_extension)
        '/home/us er/2021-07-07_-_this_is_a_test_.tx_t'

        >>> is_directory = False
        >>> rename_extension = True
        >>> File(path_1, is_directory).get_cleaned_file_path(rename_extension)
        '/home/us er/2021-07-07_-_this_is_a_test.tx_t'

        >>> is_directory = True
        >>> rename_extension = True
        >>> File(path_1, is_directory).get_cleaned_file_path(rename_extension)
        '/home/us er/2021-07-07_-_this_is_a_test_.tx_t'

        Hidden file examples:

        >>> path_2 = '/home/us er/.[2021-07-07] - this is a  test    .tx t'

        >>> is_directory = False
        >>> rename_extension = False
        >>> File(path_2, is_directory).get_cleaned_file_path(rename_extension)
        '/home/us er/.2021-07-07_-_this_is_a_test.tx t'

        >>> is_directory = False
        >>> rename_extension = True
        >>> File(path_2, is_directory).get_cleaned_file_path(rename_extension)
        '/home/us er/.2021-07-07_-_this_is_a_test.tx_t'
        """
        filename = clean_string(self.filename)

        if rename_extension and self.file_extension is not None:
            extension = clean_string(self.file_extension)
        else:
            extension = self.file_extension

        if extension is not None:
            filename += '.' + extension

        if self.is_hidden:
            filename = '.' + filename

        cleaned_file_path = os.path.join(self.parent_directory_path, filename)

        return cleaned_file_path

    def move(self, destination_path, arguments):
        """Tries to move the file to `destination_path`.

        :param destination_path: path of the destination file
        :type destination_path: str

        :param arguments: parsed arguments
        :type arguments: argparse.Namespace
        """
        file_should_be_moved = True

        if os.path.exists(destination_path) and not arguments.force:
            if not arguments.interactive:
                print(f"'{self.path}' -> '{destination_path}'")
            file_should_be_moved = yes_no_question(
                f"'{destination_path}' already exists. overwrite ([y]es)? "
            )

        if arguments.simulate:
            file_should_be_moved = False

        if arguments.verbose:
            print(f"rename: '{self.path}' -> '{destination_path}'")

        if file_should_be_moved:
            try:
                os.rename(self.path, destination_path)
            except Exception as error:
                print(f"{error}", file=sys.stderr)
            else:
                self.path = destination_path

    def list_directory_contents(self):
        """ Returns a list of the file paths of the files in the directory if
        the file is a directory.

        :return: list of the file paths
        :rtype: list of strings
        """
        assert self.is_directory, "File is not a directory."
        try:
            filenames = os.listdir(self.path)
        except PermissionError:
            print(f"Permission Error: Could not access '{self.path}'.",
                  file=sys.stderr)
            filenames = list()

        file_paths = [os.path.join(self.path, filename)
                      for filename in filenames]
        return file_paths

    def detect_filesystem_loop(self):
        """Checks if a symlink creates a filesystem loop, i.e., the target of
        the symlink contains the symlink.

        :return: True if symlink creates a filesystem loop
        :rtype: bool
        """
        assert self.is_symlink, "File is not a symlink."

        link_path = self.path
        target_path = os.readlink(link_path)

        absolute_link_path = os.path.abspath(link_path)
        absolute_target_path = os.path.abspath(target_path)

        is_system_loop = absolute_link_path.startswith(absolute_target_path)

        if is_system_loop:
            print('Filesystem loop detected: symlink: '
                  f"'{link_path}' -> '{target_path}'",
                  file=sys.stderr)

        return is_system_loop

    def clean(self, arguments):
        """Cleans the filename of the file.

        :param arguments: parsed arguments
        :type arguments: argparse.Namespace
        """
        cleaned_path = self.get_cleaned_file_path(arguments.extension)

        if cleaned_path == self.path:
            file_should_be_renamed = False
            if arguments.verbose:
                print(f"nothing to do: '{self.path}'")
        else:
            if arguments.interactive:
                file_should_be_renamed = yes_no_question(
                    f"'{self.path}' -> '{cleaned_path}' [(y)es]? "
                )
            else:
                file_should_be_renamed = True

        if file_should_be_renamed:
            self.move(cleaned_path, arguments)


def construct_files(file_paths):
    files = [File(file_path) for file_path in file_paths]
    return files


def clean_files(file_paths, arguments):
    """Cleans the names of the files.

    :param file_paths: file paths
    :type file_paths: list of strings

    :param arguments: parsed arguments
    :type arguments: argparse.Namespace
    """
    files = construct_files(file_paths)
    for file in files:
        if file.exists:
            file.clean(arguments)
        else:
            print(f"'{file.path}' does not exist.", file=sys.stderr)
            continue

        if arguments.recursive and file.is_directory:
            if file.is_symlink:
                recursion = (arguments.dereference
                             and not file.detect_filesystem_loop())
            else:
                recursion = True
        else:
            recursion = False

        if recursion:
            file_paths = file.list_directory_contents()
            clean_files(file_paths, arguments)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='clname',
        usage='%(prog)s [OPTION]... FILE...',
        description='Clean the name(s) of the FILE(s) to make them '
                    'shell-friendly\n'
                    '(i.e., get rid of characters for which escape characters '
                    '`\\` are necessary.)\n\n',
        epilog='example:\n'
               '  $ ls\n'
               "  '[2021-07-07] - this is a  test    .txt'\n"
               r'  $ clname \[2021-07-07\]\ -\ this\ is\ a\ \ test\ \ \ \ .txt'
               '\n'
               '  $ ls\n'
               '  2021-07-07_-_this_is_a_test.txt',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('paths',
                        nargs='*',
                        help=argparse.SUPPRESS)

    parser.add_argument('-e', '--extension',
                        action='store_true',
                        help='also clean the file extension')
    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='do not prompt before overwriting files')
    parser.add_argument('-L', '--dereference',
                        action='store_true',
                        help='follow symbolic links')
    parser.add_argument('-i', '--interactive',
                        action='store_true',
                        help='prompt before renaming ')
    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help='rename subdirectories and their contents '
                             'recursively')
    parser.add_argument('-s', '--simulate',
                        action='store_true',
                        help='show what would be done without renaming '
                             'anything')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='explain what is being done')
    parser.add_argument('--version',
                        action='store_true',
                        help='show copyright and version info and exit')

    # Testing the examples in the docstrings if the option '--test' is set.
    # ('--test' does not appear in the help message.)
    parser.add_argument('--test',
                        action='store_true',
                        help=argparse.SUPPRESS)

    arguments = parser.parse_args()

    if arguments.simulate:
        arguments.verbose = True

    return arguments


def print_version_info():
    print(f'clname, version {VERSION}',
          'Copyright (C) 2021 Stefan Lepperdinger',
          'License GPLv3+: GNU GPL version 3 or later '
          '<http://gnu.org/licenses/gpl.html>',
          '',
          'This is free software; you are free to change and redistribute it.',
          'There is NO WARRANTY, to the extent permitted by law.',
          sep='\n')


def exit_due_to_missing_operands():
    print('clname: missing operands',
          "Try 'clname --help' for more information.",
          sep='\n',
          file=sys.stderr)
    sys.exit(1)


def run_clname(arguments):
    try:
        clean_files(arguments.paths, arguments)
    except KeyboardInterrupt:
        print('\nclname: Keyboard interrupt. Exiting...', file=sys.stderr)
        sys.exit(1)
    except BrokenPipeError:
        print('\nclname: Broken pipeline. Exiting...', file=sys.stderr)
        sys.exit(1)


def main():
    arguments = parse_arguments()
    if arguments.version:
        print_version_info()
    elif arguments.test:
        print('Testing the examples in the docstrings...')
        import doctest
        doctest.testmod()
    elif not arguments.paths:
        exit_due_to_missing_operands()
    else:
        run_clname(arguments)


if __name__ == '__main__':
    main()
