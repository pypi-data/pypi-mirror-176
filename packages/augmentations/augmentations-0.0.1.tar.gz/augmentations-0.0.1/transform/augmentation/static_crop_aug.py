import transform.augmentation.augmentation as augmentation
from transform.augmentation.crop_aug import CropAugmentation


class StaticCropAugmentation(CropAugmentation):
    """
    Crops image to the specified section.
    :param args: <array<float>> Normalized edges
        0 left_edge
        1 right_edge
        2 top_edge
        3 bottom_edge
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)

        if self.truth("bounding_box_only"):
            raise ValueError(
                "Bounding box only is not supported for the Static Crop Preprocessing Step"
            )

        left_edge = float(args[0]) / 100
        right_edge = float(args[1]) / 100
        top_edge = float(args[2]) / 100
        bottom_edge = float(args[3]) / 100

        self.edges = [left_edge, right_edge, top_edge, bottom_edge]
        """{
            "left_edge": left_edge,
            "right_edge": right_edge,
            "top_edge": top_edge,
            "bottom_edge": bottom_edge
        }"""

    def get_bounds(self):
        return self.edges


if __name__ == "__main__":
    augmentation.test_augmentation(
        StaticCropAugmentation, [0, 100, 0, 100], {"bounding_box_only": False}
    )
    augmentation.test_augmentation(
        StaticCropAugmentation,
        [20, 70, 60, 90],
        {"bounding_box_only": False},
        polygonal=True,
    )
