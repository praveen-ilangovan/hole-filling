"""
module: cli

This module defines the command line interface using argParse.ArgumentParser

>> python -m hole_filling -h
usage: HoleFilling [-h] [-o OUTPUT_DIRECTORY] [-d] image_path mask_path z e connectivity

positional arguments:
  image_path            Location of an image file
  mask_path             Location of the mask file to be applied to the image file.
  z                     The z value for the default weighting mechanism.
  e                     The e value for the default weighting mechanism.
  connectivity          Specify the pixel connectivity. Supported values: 4,8

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        If provided, the output image will be written to this location
  -d, --debug           If set, the boundary is drawn in black in the output image. Defaults to False
"""

# Builtin imports
import argparse

# -----------------------------------------------------------------------------#
# Functions
# -----------------------------------------------------------------------------#


def get_cli_parser() -> argparse.ArgumentParser:
    """
    Returns a simple command line interface

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser("HoleFilling")

    # Positional arguments
    parser.add_argument("image_path", help="Location of an image file")
    parser.add_argument(
        "mask_path", help="Location of the mask file to be applied to the image file."
    )
    parser.add_argument(
        "z", type=int, help="The z value for the default weighting mechanism."
    )
    parser.add_argument(
        "e", type=float, help="The e value for the default weighting mechanism."
    )
    parser.add_argument(
        "connectivity",
        type=int,
        help="Specify the pixel connectivity. Supported values: 4,8",
    )

    # Optional arguments
    parser.add_argument(
        "-o",
        "--output_directory",
        help="If provided, the output image will be written to this location",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="If set, the boundary is drawn in black in the output image. Defaults to False",
    )

    return parser
