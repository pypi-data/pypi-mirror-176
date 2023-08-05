import math
from skimage import exposure

import transform.augmentation.augmentation as augmentation


class AdjustGammaAugmentation(augmentation.Augmentation):
    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)
        self.kwargs["user_input"] = args[0]

    def update_image(self, mask=False):
        if mask:
            return self.mask
        gamma = int(self.kwargs["user_input"])

        img = exposure.adjust_gamma(
            self.img, (math.pow(2, (-gamma / 2 + 50) / 10) - 1) / 31
        )

        return img


if __name__ == "__main__":
    augmentation.test_augmentation(AdjustGammaAugmentation, [10], {})
