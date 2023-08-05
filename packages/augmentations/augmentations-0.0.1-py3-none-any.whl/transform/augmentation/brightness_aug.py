import transform.augmentation.augmentation as augmentation


class BrightnessAugmentation(augmentation.Augmentation):
    """
    Brightens/darkens image
    :param img: <numpy.ndarray>
    :param amount: <int> percent by which to brighten (-100 to 100)
    :return: <numpy.ndarray> brightened image, <dict> updated annotations
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
        amount /= 100

        self.img += amount
        self.img[self.img > 1] = 1
        self.img[self.img < 0] = 0

        return self.img


if __name__ == "__main__":
    augmentation.test_augmentation(BrightnessAugmentation, [-30], {})
