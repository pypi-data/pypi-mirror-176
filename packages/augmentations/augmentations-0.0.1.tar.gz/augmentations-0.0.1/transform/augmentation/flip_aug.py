import numpy as np

import transform.augmentation.augmentation as augmentation
from transform.helper.polygon import Polygon


class FlipAugmentation(augmentation.Augmentation):
    def __init__(
        self, img, annotations=None, mask=None, args=None, how=None, **kwargs
    ):
        super().__init__(img, annotations, mask, args, **kwargs)
        self.kwargs["how"] = args[0]
        if self.kwargs["how"] == "both":
            hor_img, hor_ann, hor_mask = FlipAugmentation(
                self.img, self.annotations, self.mask, ["horizontal"]
            ).call()
            self.img = hor_img
            self.annotations = hor_ann
            self.mask = hor_mask
            self.kwargs["how"] = "vertical"

    def pre_call(self, img, annotations, mask):
        if self.kwargs["how"] not in ["vertical", "horizontal", "both"]:
            raise ValueError(
                f"flip type `{self.kwargs['how']}` not implemented!"
            )
        return img, annotations, mask

    def update_image(self, mask=False):
        img = self.mask if mask else self.img
        if self.kwargs["how"] == "vertical":
            img = np.flipud(img)
        elif self.kwargs["how"] == "horizontal":
            img = np.fliplr(img)
        return img

    def update_annotations(self):
        """
        Flips image and annotations
        """

        # set basics
        img_height = self.img.shape[0]
        img_width = self.img.shape[1]
        new_boxes = []

        if self.kwargs["how"] == "vertical":

            def flip_points_vertical(img_height):
                def inner(points):
                    for point in points:
                        point[1] = img_height - point[1]
                    return points

                return inner

            for annotation in self.annotations.get("boxes", []):
                # Unchanged
                name = annotation["label"]
                width = annotation["width"]
                height = annotation["height"]
                nX = annotation["x"]

                nY = img_height - annotation["y"]

                polygon = Polygon(annotation)
                if polygon.valid():
                    points = polygon.apply(flip_points_vertical(img_height))
                else:
                    points = None

                # create new boxes for each label
                new_box = {
                    "label": name,
                    "x": nX,
                    "y": nY,
                    "width": width,
                    "height": height,
                }
                if points:
                    new_box["points"] = points

                new_boxes.append(new_box)

            # create new annotation
            new_annotation = {
                "key": self.annotations.get("key"),
                "boxes": new_boxes,
                "width": img_width,
                "height": img_height,
            }

            return new_annotation

        elif self.kwargs["how"] == "horizontal":

            def flip_points_horizontal(img_width):
                def inner(points):
                    for point in points:
                        point[0] = img_width - point[0]
                    return points

                return inner

            for annotation in self.annotations.get("boxes", []):
                name = annotation["label"]
                width = annotation["width"]
                height = annotation["height"]
                nY = annotation["y"]

                nX = img_width - annotation["x"]

                polygon = Polygon(annotation)
                if polygon.valid():
                    points = polygon.apply(flip_points_horizontal(img_width))
                else:
                    points = None

                # create new boxes for each label
                new_box = {
                    "label": name,
                    "x": nX,
                    "y": nY,
                    "width": width,
                    "height": height,
                }
                if points:
                    new_box["points"] = points
                new_boxes.append(new_box)

            # create new annotation
            new_annotation = {
                "key": self.annotations.get("key"),
                "boxes": new_boxes,
                "width": img_width,
                "height": img_height,
            }

            return new_annotation
        else:
            return self.annotations


if __name__ == "__main__":
    augmentation.test_augmentation(FlipAugmentation, ["both"], {})
    augmentation.test_augmentation(
        FlipAugmentation,
        [["horizontal"]],
        {"bounding_box_only": True},
        polygonal=True,
    )
