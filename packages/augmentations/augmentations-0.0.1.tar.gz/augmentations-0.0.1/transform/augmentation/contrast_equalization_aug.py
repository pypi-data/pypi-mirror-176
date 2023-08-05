from skimage import exposure
import numpy as np

import transform.augmentation.augmentation as augmentation


class ContrastEqualizationAugmentation(augmentation.Augmentation):
    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)
        self.kwargs["how"] = args[0]

    def update_image(self, mask=False):
        if mask:
            return self.mask
        how = self.kwargs["how"]
        img = self.img

        # clip to range 0-1
        np.clip(img, 0, 1, img)

        if how == "Contrast Stretching":
            # grab 2nd and 98 percentile
            p2 = np.percentile(img, 2)
            p98 = np.percentile(img, 98)
            # rescale
            img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
            return img_rescale

        elif how == "Histogram Equalization":
            img_eq = exposure.equalize_hist(img)
            return img_eq

        elif how == "Adaptive Equalization":
            img_adapteq = exposure.equalize_adapthist(img, clip_limit=0.03)
            return img_adapteq

        raise ValueError(
            f"contrast equalization type `{how}` not implemented!"
        )


if __name__ == "__main__":
    augmentation.test_augmentation(
        ContrastEqualizationAugmentation,
        ["Contrast Stretching"],
        {"bounding_box_only": False},
    )
