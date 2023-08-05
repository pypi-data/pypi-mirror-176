import cv2

import transform.augmentation.augmentation as augmentation


class BlurAugmentation(augmentation.Augmentation):
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
        amount = int(float(self.kwargs["amount"]))
        if amount == 0:
            return self.img
        if amount % 2 == 0:
            amount -= 1
        return cv2.GaussianBlur(self.img, (amount, amount), 0)


if __name__ == "__main__":
    augmentation.test_augmentation(BlurAugmentation, [7.75], {})
