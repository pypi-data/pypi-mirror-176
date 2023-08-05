import numpy as np

from transform.helper.bounds import Bounds
import transform.augmentation.augmentation as augmentation
from transform.augmentation.resize_aug import ResizeAugmentation
from transform.helper.polygon import Polygon, translate_points
from transform.helper.rectangle_conversion import corner_to_center


class CropAugmentation(augmentation.Augmentation):
    """
    Crops image to the specified normalized bounds, updating annotations.
    :param img: <numpy.ndarray> numpy array of shape (height, width, channels)
    :param annotations: <dict> annotations dictionary
    :param args: <array<float>>
        0 center_x_normalized: normalized x coordinate of point to crop about
        1 center_y_normalized: normalized y coordinate of point to crop about
        2 width_normalized: normalized width of desired bounds
        3 height_normalized: normalized height of desired bounds
    :return: <numpy.ndarray> cropped image, <dict> updated annotations
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)

        # Don't set anything if bounding box only
        if self.truth("bounding_box_only"):
            return

        if len(args) >= 4:
            self.center_x_normalized = float(args[0])
            self.center_y_normalized = float(args[1])
            self.width_normalized = float(args[2])
            self.height_normalized = float(args[3])

        # Bounds to crop to
        self.bounds = None  # Bounds object
        self.left_edge = None
        self.right_edge = None
        self.top_edge = None
        self.bottom_edge = None

    def pre_call(self, img, annotations, mask):
        edges = self.calculate_edges()

        self.left_edge = edges["left_edge"]
        self.right_edge = edges["right_edge"]
        self.top_edge = edges["top_edge"]
        self.bottom_edge = edges["bottom_edge"]

        return img, annotations, mask

    def get_bounds(self):
        bounds = {
            "x": self.center_x_normalized,
            "y": self.center_y_normalized,
            "width": self.width_normalized,
            "height": self.height_normalized,
        }
        return bounds

    def denormalize_edges(self, edges):
        """Convert normalized edges to integer pixel edges"""
        img_height = self.img.shape[0]
        img_width = self.img.shape[1]

        denormalized_edges = {}
        denormalized_edges["left_edge"] = int(edges["left_edge"] * img_width)
        denormalized_edges["right_edge"] = int(edges["right_edge"] * img_width)
        denormalized_edges["top_edge"] = int(edges["top_edge"] * img_height)
        denormalized_edges["bottom_edge"] = int(
            edges["bottom_edge"] * img_height
        )

        return denormalized_edges

    def calculate_edges(self):
        """Calculate integer pixel edges from provided normalized bounds"""

        bounds = self.get_bounds()
        self.bounds = Bounds(bounds)
        edges = self.bounds.to_edges()
        pixel_edges = self.denormalize_edges(edges)

        return pixel_edges

    def update_image(self, mask=False):
        img = self.mask if mask else self.img
        # An image slice can't be empty
        if self.bounds.area() == 0:
            new_shape = img.shape
            new_shape[0] = 1
            new_shape[1] = 1
            return np.zeros(new_shape, dtype=np.float64)

        if self.truth("from_bounding_box_only"):
            img = np.zeros(img.shape, dtype=np.float64)

            # Crop image part to be resized
            left_edge_norm = self.left_edge / img.shape[1]
            right_edge_norm = self.right_edge / img.shape[1]
            top_edge_norm = self.top_edge / img.shape[0]
            bottom_edge_norm = self.bottom_edge / img.shape[0]
            xywh = corner_to_center(
                (left_edge_norm, top_edge_norm),
                (right_edge_norm, bottom_edge_norm),
            )
            crop_args = [xywh["x"], xywh["y"], xywh["width"], xywh["height"]]
            img, self.annotations = CropAugmentation(
                img,
                self.annotations,
                args=crop_args,
            ).call()

            img, self.annotations = ResizeAugmentation(
                img,
                self.annotations,
                args=["Stretch to", img.shape[1], img.shape[0]],
            ).call()
        else:
            img = img[
                self.top_edge : self.bottom_edge,
                self.left_edge : self.right_edge,
            ]

        return img

    def update_annotations(self):
        # If bounding box only, handle annotations in update_image
        if self.truth("from_bounding_box_only"):
            return self.annotations

        annotations = self.annotations

        for annotation in annotations.get("boxes", []):
            annotation["x"] = annotation["x"] - self.left_edge
            annotation["y"] = annotation["y"] - self.top_edge

            polygon = Polygon(annotation)
            if polygon.valid():
                annotation["points"] = polygon.apply(
                    translate_points(self.left_edge, self.top_edge)
                )

        annotations["width"] = self.right_edge - self.left_edge
        annotations["height"] = self.bottom_edge - self.top_edge

        if self.bounds.area() == 0 and annotations:
            annotations["width"] = 1
            annotations["height"] = 1

        return annotations


if __name__ == "__main__":
    augmentation.test_augmentation(
        CropAugmentation, [0.5, 0.3, 0.4, 0.3], {"bounding_box_only": False}
    )

    augmentation.test_augmentation(
        CropAugmentation,
        [  # fmt: skip
            [
                0.2726894334777813,
                0.7078603887833657,
                0.30367653920398086,
                0.12576187272632122,
            ],
            [
                0.3504072198331767,
                0.6117591510256745,
                0.6515441734440887,
                0.28489124163114954,
            ],
            [
                0.2520697922819326,
                0.49104205744924065,
                0.4388629836952266,
                0.7745176979549652,
            ],
            [
                0.6403667765398218,
                0.6238706175740605,
                0.4810198968162731,
                0.3203561114002791,
            ],
            [
                0.5543942604870682,
                0.31858639955242667,
                0.3569274264541323,
                0.32363901233484205,
            ],
            [
                0.19759975680516162,
                0.6668958003070707,
                0.10182819700554713,
                0.523608863722978,
            ],
            [
                0.2726894334777813,
                0.7078603887833657,
                0.30367653920398086,
                0.12576187272632122,
            ],
            [
                0.3504072198331767,
                0.6117591510256745,
                0.6515441734440887,
                0.28489124163114954,
            ],
            [
                0.2520697922819326,
                0.49104205744924065,
                0.4388629836952266,
                0.7745176979549652,
            ],
            [
                0.6403667765398218,
                0.6238706175740605,
                0.4810198968162731,
                0.3203561114002791,
            ],
            [
                0.5543942604870682,
                0.31858639955242667,
                0.3569274264541323,
                0.32363901233484205,
            ],
            [
                0.19759975680516162,
                0.6668958003070707,
                0.10182819700554713,
                0.523608863722978,
            ],
            [
                0.2726894334777813,
                0.7078603887833657,
                0.30367653920398086,
                0.12576187272632122,
            ],
            [
                0.3504072198331767,
                0.6117591510256745,
                0.6515441734440887,
                0.28489124163114954,
            ],
            [
                0.2520697922819326,
                0.49104205744924065,
                0.4388629836952266,
                0.7745176979549652,
            ],
            [
                0.6403667765398218,
                0.6238706175740605,
                0.4810198968162731,
                0.3203561114002791,
            ],
        ],  # fmt: skip
        {"bounding_box_only": True},
    )

    augmentation.test_augmentation(
        CropAugmentation, [0.5, 0.3, 0.4, 0.3], {}, polygonal=True
    )

    augmentation.test_augmentation(
        CropAugmentation,
        [[0.5, 0.3, 0.4, 0.3]],
        {"bounding_box_only": True},
        polygonal=True,
    )
