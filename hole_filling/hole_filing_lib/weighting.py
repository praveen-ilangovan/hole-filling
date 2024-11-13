"""
module: weighting

Provides an abstract class to implement weighting functions. Also defines a
default weighting mechanism
"""

# Builtin imports
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import math

from hole_filling.hole_filing_lib.models import Pixel

if TYPE_CHECKING:
    from .models import Pixel

# -----------------------------------------------------------------------------#
# Classes
# -----------------------------------------------------------------------------#


class AbstractWeightingMechanism(ABC):
    """
    An abstract class that all weighting mechanism should use to implement
    """

    @abstractmethod
    def get_weight(self, hole: "Pixel", boundary: "Pixel") -> float:
        """
        Takes in the hole and boundary and computes the weight

        Args:
            hole (Pixel): Pixel representing a hole
            boundary (Pixel): Pixel representing the boundary

        Returns:
            Computed weight in float
        """


class DefaultWeightMechanism(AbstractWeightingMechanism):
    """
    Computes the weight between hole and boundary using euclidean distance
    """

    def __init__(self, param_z: int, param_e: float):
        super().__init__()
        self.__param_z = param_z
        self.__param_e = param_e

    def get_weight(self, hole: Pixel, boundary: Pixel) -> float:
        """
        Takes in the hole and boundary and computes the weight

        Args:
            hole (Pixel): Pixel representing a hole
            boundary (Pixel): Pixel representing the boundary

        Returns:
            Computed weight in float
        """
        dist = math.dist((hole.row, hole.column), (boundary.row, boundary.column))
        denominator = math.pow(dist, self.__param_z) + self.__param_e
        return 1 / denominator
