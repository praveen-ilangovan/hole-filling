"""
module: hole_filler

For the given grayscale image where the pixel values are in the range of [0..1]
and the hole pixels are set to -1, the class finds the boundary around the hole
and fills the hole using an algorithm.
"""

# Builtin imports
from typing import TYPE_CHECKING, Optional
import tempfile
from datetime import datetime
import os

# Project specific imports
import cv2

# Local imports
from .models import Pixel, Connectivity

if TYPE_CHECKING:
    import numpy as np
    from .weighting import AbstractWeightingMechanism

# -----------------------------------------------------------------------------#
# Class
# -----------------------------------------------------------------------------#


class HoleFiller:
    """
    Class that finds the hole and its boundary and fills it using an algorithm.

    Args:
        image (np.ndarray): A 2D array in tha range of [0..1]. The hole is
            represemted with a value of -1
        weighting (AbstractWeightingMechanism): An instance of WeightingMechanism
            implemented using the AbstractWeigbhtingMechanism class.
        connectivity (Connectivity): Number of pixels the hole is connected to.
            Could be 4 or 8
        output_directory (str): Optional. Output image will be written out to this directory
        debug (bool): If set to true, the boundary pixels are set to black while
            writing to disk. Default to False
    """

    def __init__(
        self,
        image: "np.ndarray",
        weighting: "AbstractWeightingMechanism",
        connectivity: Connectivity = Connectivity.FOUR,
        output_directory: Optional[str] = None,
        debug: bool = False,
    ):
        self.__image = image
        self.__weighting = weighting
        self.__connectivity = connectivity
        self.__output_directory = output_directory
        self.__debug = debug

        # Get the resolution of the image
        self.__rows = self.__image.shape[0]
        self.__columns = self.__image.shape[1]

        # Holes and Boundaries
        self.__holes: set[Pixel] = set()
        self.__boundaries: set[Pixel] = set()

    # -------------------------------------------------------------------------#
    # Properties
    # -------------------------------------------------------------------------#
    @property
    def holes(self) -> set[Pixel]:
        """
        Return the pixels that are holes
        """
        return self.__holes

    @property
    def boundaries(self) -> set[Pixel]:
        """
        Return the pixels that are boundaries
        """
        return self.__boundaries

    # -------------------------------------------------------------------------#
    # Methods
    # -------------------------------------------------------------------------#
    def fill(self) -> None:
        """
        Fill the hole
        """
        self.find_holes_and_boundaries()

        for hole in self.holes:
            hole_color = self.calculate_hole_color(hole)
            self.__image[hole.row][hole.column] = hole_color

        self.save()

    def find_holes_and_boundaries(self) -> None:
        """
        Find the pixels that are holes (whose value is set to -1) and their
        boundary pixels.
        """
        for row_index, row in enumerate(self.__image):
            for col_index, value in enumerate(row):
                if value == -1:
                    # Found a hole
                    hole = Pixel(row_index, col_index, -1)
                    self.__holes.add(hole)

                    # Find its connected pixels
                    connected_pixels = self.__get_connected_pixels(hole)
                    self.__boundaries.update(connected_pixels)

    def calculate_hole_color(self, hole: Pixel) -> float:
        """
        Calculcate the color for the hole
        """
        numerator = 0.0
        denominator = 0.0
        for boundary in self.boundaries:
            weight = self.__weighting.get_weight(hole, boundary)
            numerator += weight * boundary.value
            denominator += weight

        return numerator / denominator

    def save(self) -> None:
        """
        Saves the image
        """
        if self.__debug:
            for boundary in self.boundaries:
                self.__image[boundary.row][boundary.column] = 0

        img = self.__image * 255

        if not self.__output_directory:
            self.__output_directory = tempfile.TemporaryDirectory().name

        filename = f"Filled_c{self.__connectivity.value}_{datetime.now().strftime("%m%d%y_%H%M%S")}.png"
        filepath = os.path.join(self.__output_directory, filename)
        cv2.imwrite(filepath, img)

        print(f"Filled output image written to: {filepath}")

    # -------------------------------------------------------------------------#
    # Methods: Privates
    # -------------------------------------------------------------------------#
    def __get_connected_pixels(self, pixel: Pixel) -> list[Pixel]:
        """
        For a given pixel, based on the connectivity value, return a list of
        connected pixels. Out of bound pixels are ignored

        Args:
            pixel (Pixel): Hole whose connected pixels has to be found.
        """
        connected_pixels = []

        indices_to_check = [
            (pixel.row, pixel.column - 1),
            (pixel.row, pixel.column + 1),
            (pixel.row - 1, pixel.column),
            (pixel.row + 1, pixel.column),
        ]

        if self.__connectivity == Connectivity.EIGHT:
            indices_to_check.extend(
                [
                    (pixel.row - 1, pixel.column - 1),
                    (pixel.row - 1, pixel.column + 1),
                    (pixel.row + 1, pixel.column - 1),
                    (pixel.row + 1, pixel.column + 1),
                ]
            )

        for row, col in indices_to_check:
            # Within the image range
            if (row < 0 or row >= self.__rows) or (col < 0 or col >= self.__columns):
                continue

            # Is it a hole?
            value = self.__image[row][col]
            if value == -1:
                continue

            connected_pixels.append(Pixel(row, col, value))

        return connected_pixels
