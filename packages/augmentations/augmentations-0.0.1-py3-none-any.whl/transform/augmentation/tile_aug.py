import transform.augmentation.augmentation as augmentation
from transform.helper.polygon import Polygon, translate_points


class TileAugmentation(augmentation.Augmentation):
    """
    Crops image to the specified tile, updating annotations.
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)
        if self.truth("bounding_box_only"):
            return
        self.kwargs["column"] = int(args[0])
        self.kwargs["row"] = int(args[1])
        self.kwargs["columnsTotal"] = int(args[2])
        self.kwargs["rowsTotal"] = int(args[3])

    def pre_call(self, img, augmentations, mask):
        (
            self.left_edge,
            self.right_edge,
            self.top_edge,
            self.bottom_edge,
        ) = self.calculate_edges()
        return img, augmentations, mask

    def calculate_edges(self):
        row = self.kwargs["row"]
        column = self.kwargs["column"]
        rowsTotal = self.kwargs["rowsTotal"]
        columnsTotal = self.kwargs["columnsTotal"]

        input_width = self.img.shape[1]
        input_height = self.img.shape[0]

        output_height = int(input_height / rowsTotal)
        output_width = int(input_width / columnsTotal)

        left_edge = column * output_width
        right_edge = (column + 1) * output_width

        top_edge = row * output_height
        bottom_edge = (row + 1) * output_height

        return left_edge, right_edge, top_edge, bottom_edge

    def update_image(self, mask=False):
        if self.truth("from_bounding_box_only"):
            raise Exception(
                "Tile augmentation cannot be called from bounding box only!"
            )
        else:
            img = self.mask if mask else self.img
            img = img[
                self.top_edge : self.bottom_edge,
                self.left_edge : self.right_edge,
            ]

        return img

    def update_annotations(self):
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


if __name__ == "__main__":
    augmentation.test_augmentation(
        TileAugmentation, [2, 1, 3, 2], {"bounding_box_only": False}
    )

    augmentation.test_augmentation(
        TileAugmentation,
        [1, 1, 3, 2],
        {"bounding_box_only": False},
        polygonal=True,
    )
