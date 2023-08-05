import numpy as np
import math
import cv2
import copy

import transform.augmentation.augmentation as augmentation
from transform.helper.polygon import Polygon


class ShearAugmentation(augmentation.Augmentation):
    """
    Shears the image in the horizontal and/or vertical direction. If only shearing in one direction, pass zero to the other shear factor.
    :param img: <numpy.ndarray>
    :param annotations: <dict>
    :param shear_factor_x: <float> shear factor from 0 to 45 degrees in the horizontal direction
    :param shear_factor_y: <float> shear factor from 0 to 45 degrees in the vertical direction
    :param fillspace: <str> 'white', 'black', or 'mirror'; what to fill extra space with
    :return: <numpy.ndarray> sheared image, <dict> updated annotations
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)

        self.kwargs["increases_size"] = True
        if len(args) > 0:
            self.kwargs["shear_factor_x"] = args[0]
        if len(args) > 1:
            self.kwargs["shear_factor_y"] = args[1]

    # Pre-call and post-call happen to be the same for shear
    def pre_call(self, img, annotations, mask):
        # adjust shear intensity in backend
        self.kwargs["shear_factor_x"] = self.kwargs["shear_factor_x"] / 3
        self.kwargs["shear_factor_y"] = self.kwargs["shear_factor_y"] / 3

        return img, annotations, mask

    def post_call(self, img, annotations, mask):
        return self.pre_call(img, annotations, mask)

    def update_image(self, mask=False):
        img = self.mask if mask else self.img
        width = img.shape[1]
        height = img.shape[0]

        shear_factor_x = float(self.kwargs["shear_factor_x"]) / 45
        shear_factor_y = float(self.kwargs["shear_factor_y"]) / 45

        # Shear
        Shear = np.eye(3)
        # Shear[0, 1] = math.tan(self.kwargs["shear_factor_x"] * math.pi / 180)  # x shear (deg)
        # Shear[1, 0] = math.tan(self.kwargs["shear_factor_y"] * math.pi / 180)  # y shear (deg)
        Shear[0, 1] = shear_factor_x  # x shear (deg)
        Shear[1, 0] = shear_factor_y  # y shear (deg)

        # Translation
        Translate = np.eye(3)
        # Translate[0, 2] = .5 * width  # x translation (pixels)
        # Translate[1, 2] = .5 * height  # y translation (pixels)

        # Combined rotation matrix
        M = Translate @ Shear
        flags = cv2.INTER_NEAREST if mask else cv2.INTER_LINEAR
        img = cv2.warpAffine(
            img,
            M[:2],
            dsize=(int(width), int(height)),
            borderValue=(0, 0, 0),
            flags=flags,
        )

        return img

    def update_annotations(self):
        # Shear
        Shear = np.eye(3)
        Shear[0, 1] = math.tan(
            self.kwargs["shear_factor_x"] * math.pi / 180
        )  # x shear (deg)
        Shear[1, 0] = math.tan(
            self.kwargs["shear_factor_y"] * math.pi / 180
        )  # y shear (deg)

        # Translation
        Translate = np.eye(3)

        M = Translate @ Shear

        width = self.img.shape[1]
        height = self.img.shape[0]

        annotations = self.annotations
        new_annotations = copy.deepcopy(self.annotations)
        new_annotations["boxes"] = []

        def update_polygon_annotations(points):
            point_count = len(points)
            points_new = np.ones((point_count, 3))
            coords = np.array(points).reshape(point_count, 2)
            points_new[:, :2] = coords

            points_new = points_new @ M.T

            points_new = np.delete(points_new, np.s_[2], 1)
            return points_new.tolist()

        for annotation in annotations.get("boxes", []):
            x1 = annotation["x"] - (annotation["width"] / 2)
            x2 = annotation["x"] + (annotation["width"] / 2)
            y1 = annotation["y"] - (annotation["height"] / 2)
            y2 = annotation["y"] + (annotation["height"] / 2)

            xy = np.ones((1 * 4, 3))
            coords = np.array([x1, y1, x2, y1, x1, y2, x2, y2]).reshape(4, 2)
            xy[:, :2] = coords

            xy = xy @ M.T
            xy = xy[:, :2].reshape(1, 8)
            x = xy[:, [0, 2, 4, 6]]
            y = xy[:, [1, 3, 5, 7]]

            xy = (
                np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1)))
                .reshape(4, 1)
                .T
            )

            # clip boxes
            xy[:, [0, 2]] = xy[:, [0, 2]].clip(0, width)
            xy[:, [1, 3]] = xy[:, [1, 3]].clip(0, height)

            new_width = float(xy[:, 2] - xy[:, 0])
            new_height = float(xy[:, 3] - xy[:, 1])
            new_x = float(xy[:, 2] + xy[:, 0]) / 2
            new_y = float(xy[:, 3] + xy[:, 1]) / 2

            annotation["x"] = new_x
            annotation["y"] = new_y
            annotation["width"] = new_width
            annotation["height"] = new_height

            polygon = Polygon(annotation)
            if polygon.valid():
                annotation["points"] = polygon.apply(
                    update_polygon_annotations
                )

            if new_width > 0 and new_height > 0:
                new_annotations["boxes"].append(annotation)

        return new_annotations


if __name__ == "__main__":
    augmentation.test_augmentation(
        ShearAugmentation, [20, 20], {"bounding_box_only": False}
    )

    # augmentation.test_augmentation(
    #     ShearAugmentation, [[0, 12], [13, 4], [3, -1], [-5, 2], [6, 3], [8, 12], [15, 4], [6, 2], [38, -32], [44, -19], [-12, -24], [1, 0], [5, -25], [29, 5], [32, 19], [-2, 35]], {
    #         "bounding_box_only": True
    #     }  # fmt: skip
    # )

    augmentation.test_augmentation(
        ShearAugmentation,
        [100, 0],
        {"bounding_box_only": False},
        polygonal=True,
    )

    augmentation.test_augmentation(
        ShearAugmentation,
        [[20, 40]],
        {"bounding_box_only": True},
        polygonal=True,
    )
