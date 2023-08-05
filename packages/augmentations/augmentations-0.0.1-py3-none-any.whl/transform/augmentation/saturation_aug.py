import numpy as np
from PIL import Image, ImageEnhance
import transform.augmentation.augmentation as augmentation


class SaturationAugmentation(augmentation.Augmentation):
    """
    Adjusts the saturation
    :param img: <numpy.ndarray>
    :param amount: <int> percent by which to saturate or desaturate (-100 to 100)
    :return: <numpy.ndarray> transformed image, <dict> updated annotations
    """

    def __init__(
        self,
        img,
        annotations=None,
        mask=None,
        args=None,
        amount=None,
        **kwargs
    ):
        super().__init__(img, annotations, mask, args, **kwargs)
        self.kwargs["amount"] = args[0]

    def update_image(self, mask=False):
        if mask:
            return self.mask
        amount = int(self.kwargs["amount"])

        if amount <= 0:
            amount = (99 + amount) / 99
        else:
            amount = (100 + amount / (1 - amount / 100)) / 100

        img = Image.fromarray(np.uint8(self.img * 255))
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(amount)
        return np.array(img, np.float64) / 255


# if __name__ == "__main__":
#     augmentation.test_augmentation(HueAugmentation, [-30], {})
