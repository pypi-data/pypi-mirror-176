##
#     Project: PixelColor
# Description: Get the screen pixel color
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import argparse

from .constants import APP_NAME, APP_VERSION, APP_DESCRIPTION


class CommandLineOptions(object):
    """
    Parse command line arguments
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=f'{APP_NAME}',
                                              description=APP_DESCRIPTION)
        self.parser.add_argument('-V',
                                 '--version',
                                 action='version',
                                 version=f'{APP_NAME} v{APP_VERSION}')

    def add_group(self, name: str) -> argparse._ArgumentGroup:
        """
        Add a command-line options group

        :param name: name for the new group
        :return: _ArgumentGroup object with the new command-line options group
        """
        return self.parser.add_argument_group(name)

    def add_screen_arguments(self) -> None:
        """
        Add screen command-line options
        """
        group = self.add_group('Screen')
        group.add_argument('--display',
                           required=False,
                           type=str,
                           default='',
                           help='display to grab the pixel')
        group.add_argument('--x',
                           '-x',
                           required=True,
                           type=int,
                           help='X coordinate to get the pixel color')
        group.add_argument('--y',
                           '-y',
                           required=True,
                           type=int,
                           help='Y coordinate to get the pixel color')

    def add_output_arguments(self) -> None:
        """
        Add output command-line options
        """
        group = self.add_group('Output')
        group.add_argument('--triplets',
                           '-T',
                           action='store_true',
                           required=False,
                           default=False,
                           help='return the color in triplets')
        group.add_argument('--hex',
                           '-H',
                           action='store_true',
                           required=False,
                           default=False,
                           help='return the color in hexadecimal format')
        group.add_argument('--upper',
                           '-U',
                           action='store_true',
                           required=False,
                           default=False,
                           help='return the result in uppercase')

    def parse_options(self) -> argparse.Namespace:
        """
        Parse command-line options

        :return: command-line options
        """
        self.options = self.parser.parse_args()
        # Check for missing options
        if not any(vars(self.options).values()):
            self.parser.print_help()
            self.parser.exit(1)
        return self.options
