import numpy as np

import transform.augmentation.augmentation as augmentation


class NoiseAugmentation(augmentation.Augmentation):
    """
    Add salt and pepper noise to image
    prob: Probability of the noise
    rec: default to 50 percent of images get random noise
    at present: prob is 0-25
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)
        if self.truth("bounding_box_only"):
            return
        self.kwargs["prob"] = args[0]
        self.kwargs["randomSeed"] = args[1]

    def update_image(self, mask=False):
        if mask:
            return self.mask
        # Divide by two to match frontend preview
        prob = float(self.kwargs["prob"]) / 100 / 2
        seed = self.kwargs["randomSeed"]

        output = np.copy(self.img)
        thres = 1 - prob

        np.random.seed(seed)
        r = np.random.uniform(size=(self.img.shape[0], self.img.shape[1]))
        output[r < prob] = 0
        output[r > thres] = 1

        return output


if __name__ == "__main__":
    augmentation.test_augmentation(
        NoiseAugmentation, [10, 5235123], {"bounding_box_only": False}
    )
