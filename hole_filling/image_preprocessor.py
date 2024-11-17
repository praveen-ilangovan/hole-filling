"""
module: image_preprocessor

This module takes in image and mask and converts it into the desired format.

Validations:
    - image and mask must be of same resolution

Process:
    - image and mask are coverted to grayscale and the pixel values are
    normalized to [0,1]
    - the pixels whose intensity are less than 0.5 in the mask, their
    corresponding pixel in the image is set to -1
"""

# Builtin imports
from typing import TYPE_CHECKING
import os

# Project specific imports
import cv2

# Local imports
from .exceptions import HoleFillingException

if TYPE_CHECKING:
    import numpy as np

# -----------------------------------------------------------------------------#
# CV2 Utils
# -----------------------------------------------------------------------------#


def convert_to_grayscale(path: str) -> "np.ndarray":
    """
    Convert the image to a grayscale image. This method returns an numpy array
    in the range of [0..1]

    Args:
        path (str): Path to an image file

    Returns:
        A numpy array in the range of [0..1]

    Raises:
        HoleFillingException
    """
    if not os.path.exists(path):
        raise HoleFillingException(f"FileNotFound: {path}")

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img / 255.0


# -----------------------------------------------------------------------------#
# Class
# -----------------------------------------------------------------------------#


class ImagePreProcessor:
    """
    Takes in an image and mask and produces an array of pixel whose range is
    between 0 and 1. Pixels in the mask whose intensity is less than 0.5, their
    corresponding pixel in the image array is set to -1.

    Args:
        image (np.ndarray): A numpy array of the image in grayscale in the range [0..1]
        mask (np.ndarray): A numpy array of the mask in grayscale in the range [0..1]
    """

    def __init__(self, image: "np.ndarray", mask: "np.ndarray"):
        self.__image = image
        self.__mask = mask

    @classmethod
    def from_images(cls, image_path: str, mask_path: str) -> "ImagePreProcessor":
        """
        Takes in tthe images and convert them to grayscale before creating an
        instance of the class

        Args:
            image_path (str): Location of an image file
            mask_path (str): Location of the mask file

        Returns:
            An instance of this class ImagePreProcessor
        """
        image = convert_to_grayscale(image_path)
        mask = convert_to_grayscale(mask_path)
        return cls(image, mask)

    # -------------------------------------------------------------------------#
    # Methods
    # -------------------------------------------------------------------------#
    def run(self) -> "np.ndarray":
        """
        Find the pixels whose intensity is less than 0.5 in mask and set the
        corresponding pixel in the image to -1.

        Returns:
            updated array
        """
        if self.__image.shape != self.__mask.shape:
            raise HoleFillingException(
                "Resolution mismatch. Image and Mask should be of same resolution."
            )

        for row_index, row in enumerate(self.__mask):
            for col_index, value in enumerate(row):
                if value < 0.5:
                    self.__image[row_index][col_index] = -1.0

        return self.__image
