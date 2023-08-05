import warnings

import cv2
import numpy as np


def warpAffine(src, M, dsize, from_bounding_box_only=False):
    """
    Applies cv2 warpAffine, marking transparency if bounding box only

    The last of the 4 channels is merely a marker. It does not specify opacity in the usual way.
    """
    if from_bounding_box_only:
        image = np.dstack((src, np.zeros((src.shape[0], src.shape[1]))))
        if image.shape[-1] != 4:
            if image.shape[-1] > 4:
                raise ValueError("image contains alpha channel")
            warnings.warn(f"image.shape is {image.shape}")
        return cv2.warpAffine(
            image,
            M,
            dsize,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=np.ones((image.shape[-1],)),
        )
    else:
        return cv2.warpAffine(src, M, dsize)
