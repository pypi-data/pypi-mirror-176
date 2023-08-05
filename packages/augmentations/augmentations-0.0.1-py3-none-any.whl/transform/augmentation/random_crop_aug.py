import math
import numpy as np

import transform.augmentation.augmentation as augmentation
from transform.augmentation.crop_aug import CropAugmentation
from transform.augmentation.resize_aug import ResizeAugmentation
from transform.helper.polygon import Polygon, translate_points

from transform.helper.rectangle_conversion import corner_to_center


class RandomCropAugmentation(augmentation.Augmentation):
    """
    Crops image to a random area, updating annotations.
    :param img: <numpy.ndarray> numpy array of shape (height, width, channels)
    :param annotations: <dict> annotations dictionary
    :param scale: <float> ratio of desired output image area to
        input image area, ranging from 0 to 1
    :param fillspace: <str> 'white', 'black', or 'mirror'; what to fill
        extra space with when scale is larger than 1
    :return: <numpy.ndarray> cropped image, <dict> updated annotations
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)
        if self.truth("bounding_box_only"):
            return
        self.kwargs["scale"] = args[0]
        self.kwargs["center_x_normalized"] = args[1]
        self.kwargs["center_y_normalized"] = args[2]

    def pre_call(self, img, augmentations, mask):
        (
            self.left_edge,
            self.right_edge,
            self.top_edge,
            self.bottom_edge,
        ) = self.calculate_edges()
        return img, augmentations, mask

    def calculate_edges(self):
        scale = float(self.kwargs["scale"])
        scale /= 100

        center_x_normalized = self.kwargs["center_x_normalized"]
        center_y_normalized = self.kwargs["center_y_normalized"]

        input_width = self.img.shape[1]
        input_height = self.img.shape[0]

        # get image area
        area = input_width * input_height

        # determine what amount of area is equivalent to image_area * scale
        scaled_area = area * scale

        # determine random pixels to include in the crop,
        # maintaining aspect ratio
        aspect_ratio = input_width / input_height

        output_height = math.sqrt(scaled_area / aspect_ratio)
        output_width = aspect_ratio * output_height

        output_center_x = int(
            (input_width - output_width) * center_x_normalized
            + output_width / 2
        )
        output_center_y = int(
            (input_height - output_height) * center_y_normalized
            + output_height / 2
        )

        left_edge = output_center_x - math.floor(output_width / 2)
        right_edge = output_center_x + math.floor(output_width / 2)

        top_edge = output_center_y - math.floor(output_height / 2)
        bottom_edge = output_center_y + math.floor(output_height / 2)

        return left_edge, right_edge, top_edge, bottom_edge

    def update_image(self, mask=False):
        img = self.mask if mask else self.img
        # An image slice can't be empty
        if self.kwargs["scale"] == 0:
            return np.zeros((1, 1, img.shape[-1]), dtype=np.float64)

        # if self.truth("from_bounding_box_only"):
        #     img = np.zeros(img.shape, dtype=np.float64)
        #     img[
        #         self.top_edge:self.bottom_edge, self.left_edge:self.right_edge
        #     ] = img[
        #         self.top_edge:self.bottom_edge, self.left_edge:self.right_edge
        #     ]
        # else:
        #     img = img[
        #         self.top_edge:self.bottom_edge, self.left_edge:self.right_edge
        #     ]

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
            img, self.annotations, _ = CropAugmentation(
                img,
                self.annotations,
                args=crop_args,
            ).call()

            img, self.annotations, _ = ResizeAugmentation(
                img,
                self.annotations,
                args=["Stretch to", self.img.shape[1], self.img.shape[0]],
            ).call()
        else:
            img = img[
                self.top_edge : self.bottom_edge,
                self.left_edge : self.right_edge,
            ]

        # Later: fill in the newly cropped image “dead pixels” (e.g. those that
        # used to contain image content) with fillspace - white, black, reflect
        # Later: place the image subset on a canvas in equal size
        # to the original image area

        # update annotations for objects to match - requires contextualizing
        # the (X,Y) translation and scale change for each coordinate point

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

        return annotations

    def post_call(self, img, annotations, mask):
        # joseph hack
        if self.kwargs["scale"] == 100:
            return self.img, self.annotations, self.mask
        if self.kwargs["scale"] == 0 and annotations:
            annotations["width"] = 1
            annotations["height"] = 1
        return img, annotations, mask


if __name__ == "__main__":
    # augmentation.test_augmentation(
    #     RandomCropAugmentation,
    #     [50, 0.41244124, 0.5135135],
    #     {"bounding_box_only": False},
    # )

    # augmentation.test_augmentation(
    #     RandomCropAugmentation,
    #     [
    #         [12, 0.21427310369539077, 0.7868610557154996],
    #         [52, 0.28147787862629015, 0.6082678948870588],
    #         [46, 0.5896865117053568, 0.7981967624668186],
    #         [26, 0.3809890837372283, 0.536471178375218],
    #         [47, 0.45922959054125256, 0.5749145453089142],
    #         [1, 0.6388241942412362, 0.1656347115304303],
    #         [46, 0.45505227026212725, 0.5998578608411814],
    #         [21, 0.5621146332805016, 0.8085494440294894],
    #         [46, 0.4282893715965329, 0.44587638759334747],
    #         [26, 0.9740171498697179, 0.49486390235431255],
    #         [36, 0.5653409531275319, 0.8724970703622514],
    #         [42, 0.8138961628228719, 0.2990536224596001],
    #         [16, 0.14014527803917975, 0.9178829145620943],
    #         [99, 0.5661339998309555, 0.8739877183322445],
    #         [69, 0.9018927259078195, 0.3105097979510886],
    #         [83, 0.10209638465186832, 0.0289297536703772],
    #     ],
    #     {"bounding_box_only": True},
    # )

    # augmentation.test_augmentation(
    #     RandomCropAugmentation,
    #     [50, 0.41244124, 0.5135135],
    #     {"bounding_box_only": False},
    #     polygonal=True,
    # )

    augmentation.test_augmentation(
        RandomCropAugmentation,
        [[40, 0.01244124, 0.8135135]],
        {"bounding_box_only": True},
        polygonal=True,
    )
