import numpy as np
from skimage.color import rgb2gray

import transform.augmentation.augmentation as augmentation


# old grayscale
# takes --- 0.19275593757629395 seconds ---
# takes 202.891264 MB


# grayscale the image
# https://scikit-image.org/docs/dev/auto_examples/color_exposure/plot_rgb_to_gray.html
# https://stackoverflow.com/questions/39463019/how-to-copy-numpy-array-value-into-higher-dimensions
class GrayscaleAugmentation(augmentation.Augmentation):
    def update_image(self, mask=False):
        if mask:
            return self.mask
        grayscale = rgb2gray(self.img)
        arr = np.expand_dims(grayscale, axis=2)
        grayscale = np.concatenate((arr, arr, arr), axis=2)
        return grayscale


if __name__ == "__main__":
    augmentation.test_augmentation(
        GrayscaleAugmentation, None, {"bounding_box_only": False}
    )
