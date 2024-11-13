"""
module: models

Defines the dataclass and enums used in this module
"""

# Builtin imports
from enum import Enum
from dataclasses import dataclass

# -----------------------------------------------------------------------------#
# Class
# -----------------------------------------------------------------------------#


@dataclass(frozen=True)
class Pixel:
    """
    Dataclass that represents a pixel in the image. It stores three values.
    col, row is the coordinate and value is the color value
    """

    row: int
    column: int
    value: float


class Connectivity(Enum):
    """
    An enum to specify the pixel connectivity.

    While finding the boundaries around the hole, HoleFiller uses this
    connectivity value to find the pixels connected to the hole pixel.

    Example:
    image => Holes have a value of -1

        1   1   1   1   1
        1   1   -1  1   1
        1   1   1   1   1
        1   1   1   1   1

    FOUR => Boundary marked by X
        1   1   X   1   1
        1   X   -1  X   1
        1   1   X   1   1
        1   1   1   1   1

    Eight => Boundary marked by X
        1   X   X   X   1
        1   X   -1  X   1
        1   X   X   X   1
        1   1   1   1   1
    """

    FOUR = 4
    EIGHT = 8
