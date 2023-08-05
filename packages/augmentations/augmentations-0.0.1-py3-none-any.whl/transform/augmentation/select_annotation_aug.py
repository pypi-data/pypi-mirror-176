import numpy as np
from PIL import Image, ImageDraw

import transform.augmentation.augmentation as augmentation
from transform.helper.polygon import Polygon


def vector_to_raster(points, width, height):
    width = round(width)
    height = round(height)

    points_ints = [tuple(map(round, point)) for point in points]

    # https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask
    img = Image.new("L", (width, height), 0)
    ImageDraw.Draw(img).polygon(points_ints, outline=1, fill=1)
    mask = np.array(img)

    mask_3_channels = np.repeat(mask[..., np.newaxis], 3, axis=2)

    return mask_3_channels


class SelectAnnotationAugmentation(augmentation.Augmentation):
    """
    Crops out anything lying outside polygon. Expects there to be only one annotation.
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)

        if self.truth("bounding_box_only"):
            raise ValueError(
                "Bounding box only is not supported for the Select Annotation Augmentation Step"
            )

    def update_image(self, mask=False):
        img = self.mask if mask else self.img

        img_width = img.shape[1]
        img_height = img.shape[0]

        annotations = self.annotations
        if (
            annotations
            and "boxes" in annotations
            and len(annotations["boxes"]) == 1
        ):
            box = annotations["boxes"][0]

            polygon = Polygon(box)
            if polygon.valid():
                polygon_mask = vector_to_raster(
                    polygon.points, img_width, img_height
                )
                img = img * polygon_mask
        else:
            print(
                "Unexpected annotations inputted to select annotation. Only one box should be passed"
            )

        return img


if __name__ == "__main__":
    augmentation.test_augmentation(
        SelectAnnotationAugmentation, args=[], kwargs={}, polygonal=True
    )
