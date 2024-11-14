"""
module: flood_fill

A simple flood fill algorithm iterates through each pixel and, when a hole is
detected, calculates the mean value of its neighboring non-hole pixels and
assigns this mean as the new value for the hole.

usage: flood_fill [-h] image_path mask_path connectivity

positional arguments:
  image_path    Location of an image file
  mask_path     Location of the mask file to be applied to the image file.
  connectivity  Specify the pixel connectivity. Supported values: 4,8

options:
  -h, --help    show this help message and exit
"""

# Builtin imports
import argparse
from datetime import datetime
import os
import statistics
from typing import TYPE_CHECKING

# Project specific imports
import cv2

# Local imports
from hole_filling.image_preprocessor import ImagePreProcessor

if TYPE_CHECKING:
    import numpy as np

HOLE_VALUE = -1


# -----------------------------------------------------------------------------#
# Flood Fill
# -----------------------------------------------------------------------------#
def flood_fill(img: "np.ndarray", connectivity: int = 4) -> "np.ndarray":
    """
    Simple flood filler

    Args:
        img (np.ndarray): An array representing the grayscale image to be
            filled. The region to be filled has a pixel value of -1.
        connectivity (int): Number of neighbouring pixels to be considered for
            fill value

    Returns:
        An array with the region filled
    """
    # Get the resolution of the image
    rows, cols = img.shape

    neighbours = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    if connectivity == 8:
        neighbours.extend([(-1, -1), (-1, 1), (1, 1), (1, -1)])

    for row_index, row in enumerate(img):
        for col_index, value in enumerate(row):
            if value == HOLE_VALUE:  # Found a hole
                # check the neighbours
                boundaries = []
                for dr, dc in neighbours:
                    nr, nc = row_index + dr, col_index + dc

                    # check if its a valid pixel
                    if nr < 0 or nr >= rows:
                        continue
                    if nc < 0 or nc >= cols:
                        continue

                    if img[nr][nc] != HOLE_VALUE:  # Found a boundary
                        boundaries.append(img[nr][nc])

                img[row_index][col_index] = statistics.mean(boundaries)

    return img


def save_image(img: "np.ndarray", filepath: str) -> None:
    """
    Writes out the image

    Args:
        img (np.ndarray): An array representation of the image to be written out.
        filepath (str): Path to write the img to.
    """
    img = img * 255
    cv2.imwrite(filepath, img)


# -----------------------------------------------------------------------------#
# Parser & Main
# -----------------------------------------------------------------------------#


def get_cli_parser() -> argparse.ArgumentParser:
    """
    Returns a simple command line interface

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser("flood_fill")

    # Positional arguments
    parser.add_argument("image_path", help="Location of an image file")
    parser.add_argument(
        "mask_path", help="Location of the mask file to be applied to the image file."
    )
    parser.add_argument(
        "connectivity",
        type=int,
        help="Specify the pixel connectivity. Supported values: 4,8",
    )

    return parser


def main() -> None:
    """Main function"""
    parser = get_cli_parser()
    args = parser.parse_args()

    connectivity = args.connectivity
    if connectivity not in (4, 8):
        print("WARNING: Invalid connectivity value. Using a value 4.")
        connectivity = 4

    # Preprocess the image and mask
    preprocessor = ImagePreProcessor.from_images(args.image_path, args.mask_path)
    processed_img = preprocessor.run()

    # Fill it
    filled_img = flood_fill(processed_img, connectivity)

    # Save it
    output_directory = os.path.dirname(args.image_path)
    filename = f"Filled_floodFill_c{connectivity}_{datetime.now().strftime("%m%d%y_%H%M%S")}.png"
    filepath = os.path.join(output_directory, filename)
    save_image(filled_img, filepath)

    print(f"Filled image written to: {filepath}")


if __name__ == "__main__":
    main()
