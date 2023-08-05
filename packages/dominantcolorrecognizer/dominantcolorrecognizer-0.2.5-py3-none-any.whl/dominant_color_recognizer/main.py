from __future__ import annotations

import os
import urllib.request
from abc import ABC, abstractmethod
from typing import Any

import extcolors
from colormap import rgb2hex
from PIL import Image

EXTCOLORS_OUTPUT = tuple[list[tuple[Any, Any]]]


class ColorAnalyzer:
    """
    Analyzes given image and extract palette of colors from it.
    """

    RESIZE_VALUE = 1000
    TOLERANCE = 12

    def __init__(self, color_model_reader: ColorModelReader) -> None:
        self._color_model_reader = color_model_reader

    @property
    def color_model_reader(self) -> ColorModelReader:
        return self._color_model_reader

    @color_model_reader.setter
    def color_model_reader(self, color_model_reader: ColorModelReader) -> None:
        self._color_model_reader = color_model_reader

    def get_dominant_colors(self, image_path: str, number_of_colors: int) -> list[str]:
        """
        Extract colors from image using extcolors library.

        :param image_path: path to the image.
        :param number_of_colors: number of colors that should be returned.
        :return: list of dominant colors in color model defined by user
        """
        return self._color_model_reader.convert_palette(
            self.__extract_colors(image_path, number_of_colors)
        )

    def __extract_colors(
        self, image_path: str, number_of_colors: int
    ) -> EXTCOLORS_OUTPUT:
        """
        Extract colors from image using extcolors library.

        :param image_path: path to the image.
        :param number_of_colors: number of colors that should be returned.
        :return: tuple with extracted colors in RGB color model.
        """
        if image_path.startswith("http"):
            urllib.request.urlretrieve(image_path, "test.jpg")
            img = Image.open("test.jpg")
        else:
            img = Image.open(image_path)
        if img.size[0] >= self.RESIZE_VALUE:
            wpercent = self.RESIZE_VALUE / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((self.RESIZE_VALUE, hsize), Image.ANTIALIAS)
            resize_name = image_path[-8:]
            img.save(resize_name)
        else:
            resize_name = image_path
        img_url = resize_name

        result = extcolors.extract_from_path(
            img_url, tolerance=self.TOLERANCE, limit=number_of_colors + 1
        )
        if image_path.startswith("http"):
            os.remove(img_url)

        return result


class ColorModelReader(ABC):
    @abstractmethod
    def convert_palette(self, color_palette: EXTCOLORS_OUTPUT):
        pass


class RGBColorModel(ColorModelReader):
    def convert_palette(self, color_palette: EXTCOLORS_OUTPUT) -> list[str]:
        """

        :param color_palette: raw color palette in EXTCOLORS_OUTPUT defined type
        :return: list of colors in RGB model.
        """
        colors_pre_list = str(color_palette).replace("([(", "").split(", (")[0:-1]
        rgb = [i.split("), ")[0] + ")" for i in colors_pre_list]
        return rgb


class HEXColorModel(ColorModelReader):
    def convert_palette(self, color_palette: EXTCOLORS_OUTPUT) -> list[str]:
        """
        Converts RGB to HEX color model.

        :param color_palette: raw color palette in EXTCOLORS_OUTPUT defined type
        :return: list of colors in HEX model.
        """
        colors_pre_list = str(color_palette).replace("([(", "").split(", (")[0:-1]
        rgb = [i.split("), ")[0] + ")" for i in colors_pre_list]
        hex = [
            rgb2hex(
                int(i.split(", ")[0].replace("(", "")),
                int(i.split(", ")[1]),
                int(i.split(", ")[2].replace(")", "")),
            )
            for i in rgb
        ]

        return hex
