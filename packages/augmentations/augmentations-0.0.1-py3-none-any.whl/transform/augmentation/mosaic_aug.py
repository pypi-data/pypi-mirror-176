import numpy as np
import cv2
from copy import deepcopy

import transform.augmentation.augmentation as augmentation
from transform.augmentation.resize_aug import ResizeAugmentation
from transform.helper.polygon import Polygon, shift_points
from transform.helper.trim_annotations import trim_annotations
from transform.helper.draw_annotations import draw_annotations


def show(img, annotations):
    new = draw_annotations(img, annotations)
    cv2.imshow("window", new)
    cv2.waitKey(1000)


class MosaicAugmentation(augmentation.Augmentation):
    def __init__(
        self, imgs, annotations=None, masks=None, args=None, **kwargs
    ):
        super().__init__(imgs, annotations, masks, args, **kwargs)
        self.imgs = imgs
        self.masks = masks
        self.annotations = annotations
        self.kwargs["percentX"] = args[0]
        self.kwargs["percentY"] = args[1]

        for percent in args[:2]:
            if percent <= 0 or percent >= 100:
                raise ValueError("Mosaic percent must be in range (0, 100)!")
        if len(imgs) < 4:
            raise ValueError(
                f"Mosaic must receive 4 images! Only got {len(imgs)}."
            )
        widths = [img.shape[1] for img in imgs]
        heights = [img.shape[0] for img in imgs]
        self.kwargs["width"] = max(widths)
        self.kwargs["height"] = max(heights)
        self.kwargs["randoms"] = args[2]

    def pre_call(self, img, annotations, mask):
        width = int(self.kwargs["width"])
        height = int(self.kwargs["height"])
        percent_x = self.kwargs["percentX"]
        percent_y = self.kwargs["percentY"]
        xf = percent_x / 100
        yf = percent_y / 100

        l_width = int(xf * width)
        l_height = int(yf * height)
        r_width = width - l_width
        r_height = height - l_height

        self.l_width = l_width
        self.l_height = l_height
        self.r_width = r_width
        self.r_height = r_height

        # For [0:l_height, 0:l_width] indexing
        # Note: changing this format will break non-indexing items as well!
        self.quadrants = [
            ((0, l_height), (0, l_width)),
            ((0, l_height), (l_width, width)),
            ((l_height, height), (0, l_width)),
            ((l_height, height), (l_width, width)),
        ]

        return img, annotations, mask

    # Hack: update_image handles annotations as well
    def update_image(self, mask=False):
        randoms = self.kwargs["randoms"]
        width = int(self.kwargs["width"])
        height = int(self.kwargs["height"])

        imgs = self.masks if mask else self.imgs

        channelCount = imgs[0].shape[-1] if len(imgs[0].shape) > 2 else 1
        if (
            not all([img.shape[-1] == channelCount for img in imgs])
            and channelCount > 1
        ):
            raise ValueError("Images must have the same number of channels!")
        mosaic = np.squeeze(
            np.zeros((height, width, channelCount), dtype=np.float64)
        )
        new_annotations = []

        annotations = deepcopy(self.annotations)

        quadrants = self.quadrants

        for i, quadrant in enumerate(quadrants):
            q_height = quadrant[0][1] - quadrant[0][0]
            q_width = quadrant[1][1] - quadrant[1][0]
            img = imgs[i]
            annotation = annotations[i]
            img_height = img.shape[0]
            img_width = img.shape[1]
            if q_height < img_height and q_width < img_width:
                point_norm = randoms[i]
                # flake8: noqa
                l = int(point_norm[0] * (img_width - q_width))
                r = l + q_width
                t = int(point_norm[1] * (img_height - q_height))
                b = t + q_height
                mosaic[
                    quadrant[0][0] : quadrant[0][1],
                    quadrant[1][0] : quadrant[1][1],
                ] = img[t:b, l:r]

                if i == 0 or i == 2:
                    translate_x = -l
                else:
                    translate_x = width - r
                if i == 0 or i == 1:
                    translate_y = -t
                else:
                    translate_y = height - b
                if not annotation:
                    new_annotations.append(None)
                    continue

                for box in annotation["boxes"]:
                    box["x"] = box["x"] + translate_x
                    box["y"] = box["y"] + translate_y

                    polygon = Polygon(box)
                    if polygon.valid():
                        box["points"] = polygon.apply(
                            shift_points(translate_x, translate_y)
                        )

                for box in annotation["boxes"]:
                    box["x"] = box["x"] - quadrant[1][0]
                    box["y"] = box["y"] - quadrant[0][0]

                    polygon = Polygon(box)
                    if polygon.valid():
                        box["points"] = polygon.apply(
                            shift_points(-quadrant[1][0], -quadrant[0][0])
                        )

                _, annotation, _ = trim_annotations(
                    mosaic[
                        quadrant[0][0] : quadrant[0][1],
                        quadrant[1][0] : quadrant[1][1],
                    ],
                    annotation,
                    None,
                )

                for box in annotation["boxes"]:
                    box["x"] = box["x"] + quadrant[1][0]
                    box["y"] = box["y"] + quadrant[0][0]

                    polygon = Polygon(box)
                    if polygon.valid():
                        box["points"] = polygon.apply(
                            shift_points(quadrant[1][0], quadrant[0][0])
                        )

                new_annotations.append(annotation)
            else:
                new_quadrant, resized_annotations, _ = ResizeAugmentation(
                    img, annotation, None, ["Stretch to", q_width, q_height]
                ).call()
                mosaic[
                    quadrant[0][0] : quadrant[0][1],
                    quadrant[1][0] : quadrant[1][1],
                ] = new_quadrant

                for box in annotation["boxes"]:
                    box["x"] = box["x"] - quadrant[1][0]
                    box["y"] = box["y"] - quadrant[0][0]

                    polygon = Polygon(box)
                    if polygon.valid():
                        box["points"] = polygon.apply(
                            shift_points(-quadrant[1][0], -quadrant[0][0])
                        )

                _, annotation, _ = trim_annotations(
                    mosaic[
                        quadrant[0][0] : quadrant[0][1],
                        quadrant[1][0] : quadrant[1][1],
                    ],
                    resized_annotations,
                    None,
                )
                for box in annotation["boxes"]:
                    box["x"] = box["x"] + quadrant[1][0]
                    box["y"] = box["y"] + quadrant[0][0]

                    polygon = Polygon(box)
                    if polygon.valid():
                        box["points"] = polygon.apply(
                            shift_points(quadrant[1][0], quadrant[0][0])
                        )

                new_annotations.append(annotation)
        if not mask:
            self.annotations = new_annotations

        return [mosaic]

    def update_annotations(self):
        annotations = self.annotations

        # Merge annotations
        new_annotations = dict()
        for annotation in annotations:
            if not annotation:
                continue
            new_annotations["key"] = annotations[0].get("key")
        new_annotations["boxes"] = []
        for annotation in annotations:
            if not annotation:
                continue
            new_annotations["boxes"].extend(annotation["boxes"])
        new_annotations["width"] = self.kwargs["width"]
        new_annotations["height"] = self.kwargs["height"]

        return [new_annotations]


if __name__ == "__main__":
    augmentation.test_augmentation(
        MosaicAugmentation,
        [
            40,
            30,
            [[0.124, 0.531], [0.652, 0.622], [0.136, 0.374], [0.834, 0.153]],
        ],
        {"bounding_box_only": False},
        multiple=True,
        png=False,
    )

    augmentation.test_augmentation(
        MosaicAugmentation,
        [
            40,
            30,
            [[0.124, 0.531], [0.652, 0.622], [0.136, 0.374], [0.834, 0.153]],
        ],
        {"bounding_box_only": False},
        multiple=True,
        png=False,
        polygonal=True,
    )
