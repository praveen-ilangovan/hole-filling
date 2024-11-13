"""
module: cv2_utils

Provides handy methods to read and write images using opencv library
"""

# Builtin imports
from typing import TYPE_CHECKING

# Project specific imports
import cv2

if TYPE_CHECKING:
    import numpy as np

#-----------------------------------------------------------------------------#
# Functions
#-----------------------------------------------------------------------------#

def convert_to_grayscale(path: str) -> "np.ndarray":
    """
    Convert the image to a grayscale image. This method returns an numpy array 
    in the range of [0..1]

    Args:
        path (str): Path to an image file

    Returns:
        A numpy array in the range of [0..1]
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img/255.0

def save_image(image: 'np.ndarray', filepath: str) -> None:
    """
    Saves the image
    """
    cv2.imwrite(filepath, image)
