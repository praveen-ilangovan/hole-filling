"""

"""

# Project specific imports
import pytest

# Package specific imports
from hole_filling.weighting import DefaultWeightMechanism
from hole_filling.models import Pixel

def test_default_weighting():
    dwm = DefaultWeightMechanism(2, 0.1)
    weight = dwm.get_weight(Pixel(1,2,1), Pixel(2,3,1))
    assert weight == pytest.approx(0.4761, rel=1e-3)
