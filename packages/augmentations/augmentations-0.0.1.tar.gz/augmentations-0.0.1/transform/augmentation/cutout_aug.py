import cv2
import transform.augmentation.augmentation as augmentation


class CutoutAugmentation(augmentation.Augmentation):
    """
    Cuts out boxes for occlusion resilience.
    Based on https://arxiv.org/pdf/1708.04552.pdf.
    :param img: <numpy.ndarray>
    :param annotations: <dict>
    :param masks: <dict> format {'masks':[[size1,nX1,nY1],[size2,nX2,nY2],...]}
        size: <int> percent of image width for mask to be
        nX/nY: <float> normalized x and y coordinates for the mask center
    :return: <numpy.ndarray> image with cutout applied, <dict> original annotations
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)
        self.kwargs["masks"] = args[0]["masks"]

    def add_mask(self, size, normalized_x, normalized_y, mask=False):
        height = self.img.shape[0]
        width = self.img.shape[1]

        x = normalized_x * width
        y = normalized_y * height

        w = (size / 100) * width
        h = (size / 100) * height

        pt1 = (int(x - w / 2), int(y - h / 2))
        pt2 = (int(x + w / 2), int(y + h / 2))
        if mask:
            cv2.rectangle(self.mask, pt1, pt2, (0, 0, 0), -1)
        else:
            cv2.rectangle(self.img, pt1, pt2, (0, 0, 0), -1)

    def update_image(self, mask=False):
        masks = self.kwargs["masks"]
        for mi in masks:
            self.add_mask(*mi, mask=mask)
        return self.mask if mask else self.img


if __name__ == "__main__":
    augmentation.test_augmentation(
        CutoutAugmentation,
        [{"masks": [[6, 0.27, 0.94], [13, 0.15, 0.62], [6, 0.63, 0.51]]}],
        {"bounding_box_only": False},
    )
