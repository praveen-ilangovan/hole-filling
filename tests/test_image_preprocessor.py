"""
Test the image_preprocessor module
"""

# Project specific imports
import numpy as np

# Package specific imports
from hole_filling.image_preprocessor import ImagePreProcessor

def test_image_preprocessing():
    image = np.array( [[1,1,1,1,1],
                       [1,1,1,1,1],
                       [1,1,1,1,1],
                       [1,1,1,1,1]] )
    
    mask = np.array( [[0.9,0.9,0.9,0.9,0.9],
                      [0.9,0.9,0,0.9,0.9],
                      [0.9,0.9,0,0.9,0.9],
                      [0.9,0.9,0.9,0.9,0.9]] )
    
    expected = np.array( [[1,1,1,1,1],
                       [1,1,-1,1,1],
                       [1,1,-1,1,1],
                       [1,1,1,1,1]] )
    
    preprocessor = ImagePreProcessor(image=image, mask=mask)
    res = preprocessor.run()

    assert (res==expected).all()
