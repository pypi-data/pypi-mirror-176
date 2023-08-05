import transform.augmentation.augmentation as augmentation
from transform.augmentation.hsl import rgb_to_hsv, hsv_to_rgb


def hueShift(arr, amount):
    hsv = rgb_to_hsv(arr)
    hsv[..., 0] = (hsv[..., 0] + amount) % 1.0
    return hsv_to_rgb(hsv)


class HueAugmentation(augmentation.Augmentation):
    """
    Rotates the hue
    :param img: <numpy.ndarray>
    :param amount: <int> degrees by which to brighten (-180 to 180)
    :return: <numpy.ndarray> rotated image, <dict> updated annotations
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
        amount /= 360

        return hueShift(self.img * 255, amount) / 255


if __name__ == "__main__":
    augmentation.test_augmentation(HueAugmentation, [-30], {})
