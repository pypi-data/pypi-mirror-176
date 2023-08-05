from copy import deepcopy
import cv2
import numpy as np

import transform.augmentation.augmentation as augmentation
from transform.helper.crop_to_center import crop_to_center
from transform.helper.polygon import (
    Polygon,
    scale_points,
    scale_points_xy,
    shift_points,
)
from transform.helper.round_half import round_half


class ResizeAugmentation(augmentation.Augmentation):
    def __init__(
        self, img, annotations=None, mask=None, args=None, how=None, **kwargs
    ):
        super().__init__(img, annotations, mask, args, **kwargs)
        self.kwargs["how"] = args[0]
        self.kwargs["width"] = args[1]
        self.kwargs["height"] = args[2]

    def pre_call(self, img, annotations, mask):
        if self.kwargs["how"] not in [
            "Stretch to",
            "Fill (with center crop) in",
            "Fit (reflect edges) in",
            "Fit (black edges) in",
            "Fit (white edges) in",
            "Fit within",
        ]:
            raise ValueError(
                f"resize type `{self.kwargs['how']}` not implemented!"
            )
        if self.kwargs["how"] == "Fit within":
            img = self.img
            mask = self.mask
            annotations = self.annotations
            width = self.kwargs["width"]
            height = self.kwargs["height"]

            img_width = img.shape[1]
            img_height = img.shape[0]
            dimensions = (width, height)

            aspect_ratio = img_height / img_width
            if dimensions[1] is None:
                self.kwargs["height"] = round(dimensions[0] * aspect_ratio)
            elif dimensions[0] is None:
                self.kwargs["width"] = round(dimensions[1] / aspect_ratio)
        return img, annotations, mask

    # def post_call(self, img, annotations, mask):
    #     ann_shape = [annotations["height"],annotations["width"]]
    #     for i, (dim1, dim2) in enumerate(zip(ann_shape, img.shape)):
    #         if dim1 != dim2:
    #             print("Warning: Annotation dimensions don't match image dimensions")
    #             delta = np.abs((dim1-dim2)/dim2)
    #             if np.max(delta) < 0.01:
    #                 print("Dimension delta is less than 1%, manually adjusting annotation to match image")
    #                 ann_shape[i] = dim2
    #     annotations["height"] = ann_shape[0]
    #     annotations["width"] = ann_shape[1]

    #     return img, annotations, mask

    def update_image(self, mask=False):
        img = self.mask if mask else self.img
        how = self.kwargs["how"]
        width = self.kwargs["width"]
        height = self.kwargs["height"]

        dimensions = (width, height)

        if how == "Stretch to":

            width = int(width)
            height = int(height)
            # width = dimensions[0]
            # height = dimensions[1]
            dim = (width, height)

            # resize image
            interpolation_method = (
                cv2.INTER_NEAREST if mask else cv2.INTER_AREA
            )
            return cv2.resize(img, dim, interpolation=interpolation_method)

        dimensions = (dimensions[1], dimensions[0])

        if how == "Fill (with center crop) in":
            for i in range(2, len(img.shape)):
                dimensions = (*dimensions, img.shape[i])
            img = crop_to_center(dimensions, img)
            return img

        elif how == "Fit (reflect edges) in":
            img = self.resize_and_pad_image(
                img, dimensions, cv2.BORDER_REFLECT, mask=mask
            )
            return img

        elif how == "Fit (black edges) in":
            img = self.resize_and_pad_image(
                img, dimensions, cv2.BORDER_CONSTANT, [0, 0, 0], mask=mask
            )
            return img

        elif how == "Fit (white edges) in":
            color = [0, 0, 0] if mask else [1, 1, 1]
            img = self.resize_and_pad_image(
                img, dimensions, cv2.BORDER_CONSTANT, color, mask=mask
            )
            return img

        elif how == "Fit within":
            img = self.resize_image(img, dimensions, mask=mask)
            return img
        return img

    def update_annotations(self):
        img = self.img
        annotations = self.annotations
        how = self.kwargs["how"]
        width = self.kwargs["width"]
        height = self.kwargs["height"]

        img_width = img.shape[1]
        img_height = img.shape[0]
        dimensions = (width, height)

        annotations["width"] = dimensions[0]
        annotations["height"] = dimensions[1]

        if how == "Stretch to":
            # get annotation size relative to new image size
            horizontal_scale_factor = width / img.shape[1]
            vertical_scale_factor = height / img.shape[0]

            # find new boxes
            new_boxes = []

            # for each label, rescale them to be new image scale
            for box in annotations["boxes"]:
                name = box["label"]
                nX = horizontal_scale_factor * box["x"]
                nY = vertical_scale_factor * box["y"]
                nWidth = horizontal_scale_factor * box["width"]
                nHeight = vertical_scale_factor * box["height"]

                nX = round_half(nX)
                nY = round_half(nY)
                nWidth = round_half(nWidth)
                nHeight = round_half(nHeight)

                new_box = {
                    "label": name,
                    "x": nX,
                    "y": nY,
                    "width": nWidth,
                    "height": nHeight,
                }

                polygon = Polygon(box)
                if polygon.valid():
                    new_box["points"] = polygon.apply(
                        scale_points_xy(
                            horizontal_scale_factor, vertical_scale_factor
                        )
                    )

                new_boxes.append(new_box)

            new_annotation = {
                "key": annotations.get("key"),
                "boxes": new_boxes,
                "width": width,
                "height": height,
            }

            return new_annotation

        dimensions = (dimensions[1], dimensions[0])

        if how == "Fill (with center crop) in":
            for annotation in annotations.get("boxes", []):
                x_shift = -(img_width / 2 - width / 2)
                y_shift = -(img_height / 2 - height / 2)

                annotation["x"] += x_shift
                annotation["y"] += y_shift

                polygon = Polygon(annotation)
                if polygon.valid():
                    annotation["points"] = polygon.apply(
                        shift_points(x_shift, y_shift)
                    )
            return annotations

        elif how == "Fit (reflect edges) in":
            annotations = self.resize_fit_annotations_reflect(
                img.shape, dimensions, annotations
            )
            return annotations

        elif how == "Fit (black edges) in":
            annotations = self.resize_fit_annotations(
                img.shape, dimensions, annotations
            )
            return annotations

        elif how == "Fit (white edges) in":
            annotations = self.resize_fit_annotations(
                img.shape, dimensions, annotations
            )
            return annotations

        elif how == "Fit within":
            annotations = self.resize_fit_annotations(
                img.shape, dimensions, annotations, pad=False
            )
            return annotations

    def resize_image(self, img, dimensions, mask=False):
        scale, _ = self.get_scale_and_direction(img.shape, dimensions)
        new_width = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        interpolation_method = cv2.INTER_NEAREST if mask else cv2.INTER_LINEAR
        resized = cv2.resize(
            img, (new_width, new_height), interpolation=interpolation_method
        )
        return resized

    def resize_and_pad_image(
        self, img, dimensions, how, color=[0, 0, 0], mask=False
    ):
        """
        Resizes image with fit option
        :param img: <np.ndarray>
        :param dimensions: <tuple>
        :param how: <cv2.borderType>
        :param color: <list>
        :return: <np.ndarray>
        """
        resized = self.resize_image(img, dimensions, mask=mask)
        new_width = resized.shape[1]
        new_height = resized.shape[0]

        top = int((dimensions[0] - new_height) / 2)
        bottom = int((dimensions[0] - new_height) / 2)
        left = int((dimensions[1] - new_width) / 2)
        right = int((dimensions[1] - new_width) / 2)
        # for images with odd pixels values, we need to add a pixel to the padding here - JS 12-20-20
        if ((dimensions[0] - new_height) % 2) != 0:
            top += 1
        if ((dimensions[1] - new_width) % 2) != 0:
            left += 1
        img = cv2.copyMakeBorder(
            resized, top, bottom, left, right, how, value=color
        )
        return img

    def get_scale_and_direction(self, old_shape, new_shape):
        """
        Returns the scale and direction of the output image to the input image for the resize fit option
        """
        new_width = new_shape[1]
        new_height = new_shape[0]

        old_width = old_shape[1]
        old_height = old_shape[0]

        if new_width / old_width * old_height < new_height:
            # vertical center; fit width with extra vertical space
            scale = new_width / old_width
            pad_direction = "y"
        else:
            # horizontal center; fit height with extra horizontal space
            scale = new_height / old_height
            pad_direction = "x"
        return scale, pad_direction

    def resize_fit_annotations_reflect(
        self, old_shape, new_shape, annotations
    ):
        """
        Updates the annotations when resizing with fit option and updates reflections.
        :param scale: <float>
        :param new_shape: <tuple>
        :param pad_direction: <str>
        :param annotations: <dict>
        """
        scale, pad_direction = self.get_scale_and_direction(
            old_shape, new_shape
        )
        to_add = []
        for annotation in annotations.get("boxes", []):
            polygon = Polygon(annotation)
            if polygon.valid():
                polygon.apply(scale_points(scale))

                annotation["points"] = polygon.points
                points = polygon.points

            annotation["x"] = int(annotation["x"] * scale)
            annotation["y"] = int(annotation["y"] * scale)
            annotation["width"] = int(annotation["width"] * scale)
            annotation["height"] = int(annotation["height"] * scale)
            if pad_direction not in ("x", "y"):
                raise Exception("pad_direction is not x or y!")
            elif pad_direction == "y":
                padding_height = int((new_shape[0] - old_shape[0] * scale) / 2)
                new_y = {
                    "left": padding_height - annotation["y"],
                    "right": padding_height
                    + annotation["y"]
                    + 2 * (old_shape[0] * scale - annotation["y"]),
                }
                if polygon.valid():
                    new_points_left = [
                        [point[0], padding_height - point[1]]
                        for point in points
                    ]
                    new_points_right = [
                        [
                            point[0],
                            padding_height
                            + point[1]
                            + 2 * (old_shape[0] * scale - point[1]),
                        ]
                        for point in points
                    ]
                odd = True
                while True:
                    if (
                        new_y["left"] + annotation["height"] / 2 > 0
                        or new_y["right"] - annotation["height"] / 2
                        < new_shape[0]
                    ):
                        new_box = {
                            "label": annotation["label"],
                            "x": annotation["x"],
                            "y": int(new_y["left"]),
                            "width": annotation["width"],
                            "height": annotation["height"],
                        }
                        if polygon.valid():
                            new_box["points"] = deepcopy(new_points_left)
                        to_add.append(new_box)
                        new_box_2 = {
                            "label": annotation["label"],
                            "x": annotation["x"],
                            "y": int(new_y["right"]),
                            "width": annotation["width"],
                            "height": annotation["height"],
                        }
                        if polygon.valid():
                            new_box_2["points"] = deepcopy(new_points_right)
                        to_add.append(new_box_2)
                        if odd:
                            translate_left = -(
                                2 * (old_shape[0] * scale - annotation["y"])
                            )
                            translate_right = 2 * annotation["y"]

                            new_y["left"] += translate_left
                            new_y["right"] += translate_right

                            if polygon.valid():
                                for i, point in enumerate(new_points_left):
                                    point[1] -= 2 * (
                                        old_shape[0] * scale
                                        - annotation["points"][i][1]
                                    )
                                for i, point in enumerate(new_points_right):
                                    point[1] += 2 * annotation["points"][i][1]
                        else:
                            translate_left = -(2 * annotation["y"])
                            translate_right = 2 * (
                                old_shape[0] * scale - annotation["y"]
                            )

                            new_y["left"] += translate_left
                            new_y["right"] += translate_right

                            if polygon.valid():
                                for i, point in enumerate(new_points_left):
                                    point[1] -= 2 * annotation["points"][i][1]
                                for i, point in enumerate(new_points_right):
                                    point[1] += 2 * (
                                        old_shape[0] * scale
                                        - annotation["points"][i][1]
                                    )
                        odd = not odd
                    else:
                        break
                annotation["y"] += padding_height
                if polygon.valid():
                    annotation["points"] = polygon.apply(
                        shift_points(0, padding_height)
                    )
            else:
                padding_width = int((new_shape[1] - old_shape[1] * scale) / 2)
                new_x = padding_width - annotation["x"]
                new_x = {
                    "left": padding_width - annotation["x"],
                    "right": padding_width
                    + annotation["x"]
                    + 2 * (old_shape[1] * scale - annotation["x"]),
                }
                if polygon.valid():
                    new_points_left = [
                        [padding_width - point[0], point[1]]
                        for point in points
                    ]
                    new_points_right = [
                        [
                            padding_width
                            + point[0]
                            + 2 * (old_shape[1] * scale - point[0]),
                            point[1],
                        ]
                        for point in points
                    ]
                odd = True
                while True:
                    if (
                        new_x["left"] + annotation["width"] / 2 > 0
                        or new_x["right"] - annotation["width"] / 2
                        < new_shape[1]
                    ):
                        new_box = {
                            "label": annotation["label"],
                            "x": int(new_x["left"]),
                            "y": annotation["y"],
                            "width": annotation["width"],
                            "height": annotation["height"],
                        }
                        if polygon.valid():
                            new_box["points"] = deepcopy(new_points_left)
                        to_add.append(new_box)
                        new_box_2 = {
                            "label": annotation["label"],
                            "x": int(new_x["right"]),
                            "y": annotation["y"],
                            "width": annotation["width"],
                            "height": annotation["height"],
                        }
                        if polygon.valid():
                            new_box_2["points"] = deepcopy(new_points_right)
                        to_add.append(new_box_2)
                        if odd:
                            new_x["left"] -= 2 * (
                                old_shape[1] * scale - annotation["x"]
                            )
                            new_x["right"] += 2 * annotation["x"]

                            if polygon.valid():
                                for i, point in enumerate(new_points_left):
                                    point[0] -= 2 * (
                                        old_shape[1] * scale
                                        - annotation["points"][i][0]
                                    )
                                for i, point in enumerate(new_points_right):
                                    point[0] += 2 * annotation["points"][i][0]
                        else:
                            new_x["left"] -= 2 * annotation["x"]
                            new_x["right"] += 2 * (
                                old_shape[1] * scale - annotation["x"]
                            )

                            if polygon.valid():
                                for i, point in enumerate(new_points_left):
                                    point[0] -= 2 * annotation["points"][i][0]
                                for i, point in enumerate(new_points_right):
                                    point[0] += 2 * (
                                        old_shape[1] * scale
                                        - annotation["points"][i][0]
                                    )
                        odd = not odd
                    else:
                        break
                annotation["x"] += padding_width
                if polygon.valid():
                    annotation["points"] = polygon.apply(
                        shift_points(padding_width, 0)
                    )

        annotations["boxes"].extend(to_add)
        annotations["width"] = new_shape[1]
        annotations["height"] = new_shape[0]

        return annotations

    def resize_fit_annotations(
        self, old_shape, new_shape, annotations, pad=True
    ):
        """
        Updates the annotations when resizing with fit option.
        :param scale: <float>
        :param new_shape: <tuple>
        :param pad_direction: <str>
        :param annotations: <dict>
        """
        print("IMAGE SHAPE", self.img.shape)
        print("OLD/NEW", old_shape, new_shape)
        scale, pad_direction = self.get_scale_and_direction(
            old_shape, new_shape
        )
        for annotation in annotations.get("boxes", []):
            annotation["x"] = int(np.round(annotation["x"] * scale))
            annotation["y"] = int(np.round(annotation["y"] * scale))
            annotation["width"] = int(annotation["width"] * scale)
            annotation["height"] = int(annotation["height"] * scale)

            polygon = Polygon(annotation)
            if polygon.valid():
                annotation["points"] = polygon.apply(scale_points(scale))

            if not pad:
                continue

            if pad_direction not in ("x", "y"):
                raise Exception("pad_direction is not x or y!")
            elif pad_direction == "y":
                padding_height = int(
                    np.round((new_shape[0] - old_shape[0] * scale) / 2)
                )
                annotation["y"] += padding_height
                polygonal_shift = shift_points(0, padding_height)
            else:
                padding_width = int(
                    np.round((new_shape[1] - old_shape[1] * scale) / 2)
                )
                annotation["x"] += padding_width
                polygonal_shift = shift_points(padding_width, 0)

            if polygon.valid():
                annotation["points"] = polygon.apply(polygonal_shift)

        annotations["width"] = new_shape[1]
        annotations["height"] = new_shape[0]
        if not pad:
            annotations["width"] = int(old_shape[1] * scale)
            annotations["height"] = int(old_shape[0] * scale)
            # if pad_direction not in ("x", "y"):
            #     raise Exception("pad_direction is not x or y!")
            # elif pad_direction == "y":
            #     padding_height = int(np.round((new_shape[0] - old_shape[0] * scale) / 2))
            #     annotations["height"] -= 2 * padding_height
            # else:
            #     padding_width = int(np.round((new_shape[1] - old_shape[1] * scale) / 2))
            #     annotations["width"] -= 2 * padding_width

        return annotations


if __name__ == "__main__":
    augmentation.test_augmentation(
        ResizeAugmentation,
        ["Fit (reflect edges) in", 400, 1000],
        {"bounding_box_only": False},
    )
    augmentation.test_augmentation(
        ResizeAugmentation,
        ["Fit (reflect edges) in", 1000, 100],
        {"bounding_box_only": False},
        polygonal=True,
    )
