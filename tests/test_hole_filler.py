"""
Test the hole_filler module
"""

# Project specific imports
import numpy as np
import pytest

# Package specific imports
from hole_filling.hole_filing_lib.hole_filler import HoleFiller
from hole_filling.hole_filing_lib.weighting import DefaultWeightMechanism
from hole_filling.hole_filing_lib.models import Pixel, Connectivity

@pytest.fixture(scope="session")
def weighting():
    return DefaultWeightMechanism(3,0.01)

def test_find_holes(weighting):
    image = np.array( [[1,1,1,1,1],
                       [1,1,-1,1,1],
                       [1,1,-1,1,1],
                       [1,1,1,1,1]] )

    hf = HoleFiller(image, weighting)
    hf.find_holes_and_boundaries()

    assert not hf.holes - set([Pixel(1,2,-1), Pixel(2,2,-1)])

#-----------------------------------------------------------------------------#
# Boundaries - Connectivity - 4
#-----------------------------------------------------------------------------#
def test_find_boundaries(weighting):
    image = np.array( [[1,1,1,1,1],
                       [1,1,-1,1,1],
                       [1,1,1,1,1],
                       [1,1,1,1,1]] )

    hf = HoleFiller(image, weighting)
    hf.find_holes_and_boundaries()

    expected = set()
    expected.update( [Pixel(1,1,1), Pixel(1,3,1), Pixel(0,2,1), Pixel(2,2,1)] )

    assert not hf.boundaries - expected

def test_find_boundaries_two_holes(weighting):
    image = np.array( [[1,1,1,1,1],
                       [1,1,-1,1,1],
                       [1,1,-1,1,1],
                       [1,1,1,1,1]] )

    hf = HoleFiller(image, weighting)
    hf.find_holes_and_boundaries()

    expected = set()
    expected.update( [Pixel(1,1,1), Pixel(1,3,1),
                      Pixel(2,1,1), Pixel(2,3,1),
                      Pixel(0,2,1), Pixel(3,2,1)] )

    assert not hf.boundaries - expected

def test_find_boundaries_corner_holes(weighting):
    image = np.array( [[1,1,-1,1,1],
                       [-1,1,1,1,1],
                       [1,1,1,1,-1],
                       [1,-1,1,1,1]] )

    hf = HoleFiller(image, weighting)
    hf.find_holes_and_boundaries()

    expected = set()
    expected.update( [Pixel(0,1,1), Pixel(1,2,1), Pixel(0,3,1),
                      Pixel(2,3,1), Pixel(1,4,1), Pixel(3,4,1),
                      Pixel(3,0,1), Pixel(2,1,1), Pixel(3,2,1),
                      Pixel(2,0,1), Pixel(1,1,1), Pixel(0,0,1)] )

    assert not hf.boundaries - expected

#-----------------------------------------------------------------------------#
# Boundaries - Connectivity - 8
#-----------------------------------------------------------------------------#
def test_find_boundaries_c8(weighting):
    image = np.array( [[1,1,1,1,1],
                       [1,1,-1,1,1],
                       [1,1,1,1,1],
                       [1,1,1,1,1]] )

    hf = HoleFiller(image, weighting, connectivity=Connectivity.EIGHT)
    hf.find_holes_and_boundaries()

    expected = set()
    expected.update( [Pixel(1,1,1), Pixel(1,3,1), Pixel(0,2,1), Pixel(2,2,1),
                      Pixel(0,1,1), Pixel(0,3,1), Pixel(2,1,1), Pixel(2,3,1)] )

    assert not hf.boundaries - expected

def test_find_boundaries_two_holes_c8(weighting):
    image = np.array( [[1,1,1,1,1],
                       [1,1,-1,1,1],
                       [1,1,-1,1,1],
                       [1,1,1,1,1]] )

    hf = HoleFiller(image, weighting, connectivity=Connectivity.EIGHT)
    hf.find_holes_and_boundaries()

    expected = set()
    expected.update( [Pixel(1,1,1), Pixel(1,3,1),
                      Pixel(2,1,1), Pixel(2,3,1),
                      Pixel(0,2,1), Pixel(3,2,1),
                      Pixel(0,1,1), Pixel(0,3,1),
                      Pixel(3,1,1), Pixel(3,3,1)] )

    assert not hf.boundaries - expected

def test_find_boundaries_corner_holes_c8(weighting):
    image = np.array( [[1,1,-1,1,1],
                       [-1,1,1,1,1],
                       [1,1,1,1,-1],
                       [1,-1,1,1,1]] )

    hf = HoleFiller(image, weighting, connectivity=Connectivity.EIGHT)
    hf.find_holes_and_boundaries()

    expected = set()
    expected.update( [Pixel(0,1,1), Pixel(1,2,1), Pixel(0,3,1),
                      Pixel(2,3,1), Pixel(1,4,1), Pixel(3,4,1),
                      Pixel(3,0,1), Pixel(2,1,1), Pixel(3,2,1),
                      Pixel(2,0,1), Pixel(1,1,1), Pixel(0,0,1),
                      Pixel(1,3,1), Pixel(2,2,1), Pixel(3,3,1)] )

    assert not hf.boundaries - expected
