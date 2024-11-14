"""
module: fmm

Uses OpenCV's Fast Marching Method algorithm to fill the hole region in the
image.

Usage: python q3_fmm <image_path> <mask_path>

fmm [-h] image_path mask_path

positional arguments:
  image_path  Location of an image file
  mask_path   Location of the mask file to be applied to the image file.

options:
  -h, --help  show this help message and exit
"""

# Builtin imports
import argparse
from datetime import datetime
import os

# Project specific imports
import cv2

# -----------------------------------------------------------------------------#
# cv2 fmm
# -----------------------------------------------------------------------------#


def cv2_fmm(image_path: str, mask_path: str) -> None:
    """
    Takes in the image_path and the mask_path, fills the masked region and
    saves the image file.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # invert the mask.
    # OpenCV considers the white region as mask.
    inverted_mask = cv2.bitwise_not(mask)

    # Fill
    dst = cv2.inpaint(img, inverted_mask, 3, cv2.INPAINT_TELEA)

    # Save it
    output_directory = os.path.dirname(image_path)
    filename = f"Filled_fmm_{datetime.now().strftime("%m%d%y_%H%M%S")}.png"
    filepath = os.path.join(output_directory, filename)
    cv2.imwrite(filepath, dst)
    print(f"Filled image written to: {filepath}")


# -----------------------------------------------------------------------------#
# Parser & Main
# -----------------------------------------------------------------------------#


def get_cli_parser() -> argparse.ArgumentParser:
    """
    Returns a simple command line interface

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser("fmm")

    # Positional arguments
    parser.add_argument("image_path", help="Location of an image file")
    parser.add_argument(
        "mask_path", help="Location of the mask file to be applied to the image file."
    )

    return parser


def main() -> None:
    """Main function"""
    parser = get_cli_parser()
    args = parser.parse_args()

    cv2_fmm(args.image_path, args.mask_path)


if __name__ == "__main__":
    main()
