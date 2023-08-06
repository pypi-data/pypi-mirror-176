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

import PIL.Image
import PIL.ImageGrab


class PixelColor(object):
    def __init__(self):
        pass

    def get_color(self, display: str, x: int, y: int) -> tuple[int]:
        """
        Get the pixel color at the coordinates X and Y

        :param display: X display to grab the image from
        :param x: left position
        :param y: top position
        :return: pixel color as RGB tuple
        """
        image = self.get_image(display=display, x1=x, y1=y, x2=x + 1, y2=y + 1)
        pixels = image.load()
        return pixels[0, 0]

    def get_image(self,
                  display: str,
                  x1: int,
                  y1: int,
                  x2: int,
                  y2: int) -> PIL.Image:
        """
        Get the image from the screen

        :param display: X display to grab the image from
        :param x1: left initial position
        :param y1: top initial position
        :param x2: left final position
        :param y2: top final position
        :return: grabbed PIL.Image
        """
        return PIL.ImageGrab.grab(bbox=(x1, y1, x2, y2),
                                  xdisplay=display)
