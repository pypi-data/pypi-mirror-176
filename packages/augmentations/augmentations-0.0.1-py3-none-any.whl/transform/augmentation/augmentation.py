from copy import deepcopy
import json
import warnings

import rasterio
from skimage.io import imread
from matplotlib import pyplot as plt
import numpy as np
from collections.abc import Iterable

from transform.helper.draw_annotations import draw_annotations
from transform.helper.polygon import Polygon, annotation_points, shift_points
from transform.helper.rectangle_conversion import box_to_edges
from transform.helper.trim_annotations import bound
from transform.helper.crop_to_center import crop_to_center
from transform.helper.bounds import (
    Bounds,
    multipolygon_to_boxes,
    bound_polygon,
    polygon_to_box,
)


class Augmentation:
    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        self.img = img
        self.mask = mask
        self.annotations = annotations
        self.args = args
        self.kwargs = kwargs

        if args and type(args[0]) == list:
            self.kwargs["bounding_box_only"] = True

    def truth(self, key):
        return key in self.kwargs and self.kwargs[key]

    def mask_truth(self, mask):
        if isinstance(mask, np.ndarray):
            return mask.any()
        elif isinstance(mask, Iterable):
            if len(mask) > 0:
                return self.mask_truth(mask[0])
            else:
                return False
        else:
            mask_val = mask
        return mask_val is not None

    def call(self):
        if self.truth("bounding_box_only"):
            return self.bounding_box_only()

        self.img, self.annotations, self.mask = self.pre_call(
            self.img, self.annotations, self.mask
        )
        img = self.update_image()
        if self.mask_truth(self.mask):
            mask = self.update_image(mask=True)
        else:
            mask = self.mask

        if self.truth("increases_size"):
            # If called from bounding box only, don't crop to center
            self.kwargs["crop_to_center"] = not self.truth(
                "from_bounding_box_only"
            )

            if self.kwargs["crop_to_center"]:
                img = crop_to_center(self.img, img)
                if self.mask_truth(self.mask):
                    mask = crop_to_center(self.mask, mask)

        annotations = self.update_annotations() if self.annotations else None

        annotations = self.tighten_bounding_boxes(annotations)

        img, annotations, mask = self.post_call(img, annotations, mask)

        return img, annotations, mask

    # If polygon annotations, tighten rectangular bounding box as well to fit the polygon
    def tighten_bounding_boxes(self, annotations_):
        def tighten(annotations):
            if not annotations:
                return None
            for annotation in annotations["boxes"]:
                points = annotation_points(annotation)
                if points:
                    bounds = polygon_to_box(points)
                    if bounds is not None:
                        annotation["x"] = bounds.x
                        annotation["y"] = bounds.y
                        annotation["width"] = bounds.width
                        annotation["height"] = bounds.height
            return annotations

        if not annotations_:
            return None

        multi_augmentation = isinstance(annotations_, list)
        if multi_augmentation:
            return [tighten(annotations) for annotations in annotations_]

        return tighten(annotations_)

    def pre_call(self, img, annotations, mask):
        return img, annotations, mask

    def post_call(self, img, annotations, mask):
        return img, annotations, mask

    def update_image(self, mask=False):
        pass

    def update_annotations(self):
        return self.annotations

    def bounding_box_only(self):
        self.kwargs["bounding_box_only"] = False
        self.kwargs["from_bounding_box_only"] = True

        image = self.img
        self.img = None

        mask = self.mask
        self.mask = None
        use_mask = True if self.mask_truth(mask) else False

        annotations = self.annotations
        self.annotations = None

        new_image = np.copy(image)
        new_mask = np.copy(mask)

        if not annotations:
            return image, annotations, mask

        new_boxes = []

        for (i, annotation) in enumerate(annotations.get("boxes", [])):
            polygon = Polygon(annotation)

            # Determine bounds
            if polygon.valid():
                edges = polygon_to_box(polygon.points).to_edges()
                left_bound = round(edges["left_edge"])
                right_bound = round(edges["right_edge"])
                top_bound = round(edges["top_edge"])
                bottom_bound = round(edges["bottom_edge"])
            else:
                (left_bound, right_bound, top_bound, bottom_bound) = (
                    round(x) for x in box_to_edges(annotation)
                )

            ripped = image[top_bound:bottom_bound, left_bound:right_bound]
            ripped_mask = (
                mask[top_bound:bottom_bound, left_bound:right_bound]
                if use_mask
                else None
            )

            if i >= len(self.args) or self.args[i] == []:
                new_boxes.append(annotation)
                continue
            arg = self.args[i]

            if not polygon.valid():
                # annotations is mutated later, but this must run before any possible "continue"
                new_boxes.append(annotation)

            if polygon.valid():
                annotation_copy = deepcopy(annotation)
                annotation_copy["x"] = annotation_copy["width"] / 2
                annotation_copy["y"] = annotation_copy["height"] / 2
                annotation_copy["points"] = polygon.applied(
                    shift_points(-left_bound, -top_bound)
                )
                bb_boxes = [annotation_copy]
                bb_input_annotations = {
                    "boxes": bb_boxes,
                    "width": ripped.shape[1],
                    "height": ripped.shape[0],
                }
            else:
                # If no polygon annotations, skip processing annotations to increase performance
                bb_input_annotations = None

            (
                bounding_box_img,
                bb_output_annotations,
                bounding_box_mask,
            ) = self.__class__(
                ripped, bb_input_annotations, ripped_mask, arg, **self.kwargs
            ).call()

            original_width = annotation["width"]
            original_height = annotation["height"]

            annotation["width"] = bounding_box_img.shape[1]
            annotation["height"] = bounding_box_img.shape[0]

            poly_bounds = Bounds(annotation).to_edges()
            p_min_x = poly_bounds["left_edge"]
            p_min_y = poly_bounds["top_edge"]
            (min_x, max_x, min_y, max_y) = map(int, bound(annotation, image))

            # For a bounding box only augmentation, each annotation has only one box
            if (
                bb_output_annotations
                and "boxes" in bb_output_annotations
                and len(bb_output_annotations["boxes"]) > 0
            ):
                bb_output_annotation = bb_output_annotations["boxes"][0]
                bb_polygon = Polygon(bb_output_annotation)
                if polygon.valid() and bb_polygon.valid():
                    bb_output_annotation["points"] = bb_polygon.apply(
                        shift_points(p_min_x, p_min_y)
                    )
                    bounds = Bounds([min_x, max_x, min_y, max_y])
                    multipolygon_pts = bound_polygon(bb_polygon.points, bounds)
                    new_boxes.extend(
                        multipolygon_to_boxes(
                            multipolygon_pts, label=annotation.get("label", "")
                        )
                    )

            inverse_annotation = {
                "x": image.shape[1] / 2
                - (annotation["x"] - annotation["width"] / 2),
                "y": image.shape[0] / 2
                - (annotation["y"] - annotation["height"] / 2),
                "width": image.shape[1],
                "height": image.shape[0],
            }

            # bbi <=> bounding box image
            (bbi_min_x, bbi_max_x, bbi_min_y, bbi_max_y) = map(
                round, bound(inverse_annotation, bounding_box_img)
            )

            width_diff = (max_x - min_x) - (bbi_max_x - bbi_min_x)
            if width_diff > 0:
                max_x -= width_diff
            elif width_diff < 0:
                bbi_max_x += width_diff
            if abs(width_diff) > 3:
                raise Exception(f"width_diff too high: {width_diff}!")

            height_diff = (max_y - min_y) - (bbi_max_y - bbi_min_y)
            if height_diff > 0:
                max_y -= height_diff
            elif height_diff < 0:
                bbi_max_y += height_diff
            if abs(height_diff) > 3:
                raise Exception(f"height_diff too high: {height_diff}!")

            avg_width = (original_width + bounding_box_img.shape[1]) / 2
            avg_height = (original_height + bounding_box_img.shape[0]) / 2

            annotation["width"] = avg_width
            annotation["height"] = avg_height

            # If contains alpha channel
            # Assumes 3 dimensional image (height, width, channels)
            if len(bounding_box_img.shape) != len(ripped.shape):
                warnings.warn(
                    f"Number of dimensions unequal: {bounding_box_img.shape} vs {ripped.shape}"
                )
            if bounding_box_img.shape[-1] > ripped.shape[-1]:
                for y in range(min_y, max_y):
                    for x in range(min_x, max_x):
                        slice = bounding_box_img[
                            bbi_min_y + (y - min_y), bbi_min_x + (x - min_x)
                        ]
                        slice_mask = (
                            bounding_box_mask[
                                bbi_min_y + (y - min_y),
                                bbi_min_x + (x - min_x),
                            ]
                            if use_mask
                            else None
                        )
                        if slice[-1] != 1:
                            new_image[y, x] = slice[:-1]
                            if use_mask:
                                new_mask[y, x] = slice_mask[:-1]
            else:
                new_image[min_y:max_y, min_x:max_x] = bounding_box_img[
                    bbi_min_y:bbi_max_y, bbi_min_x:bbi_max_x
                ]
                if use_mask:
                    new_mask[min_y:max_y, min_x:max_x] = bounding_box_mask[
                        bbi_min_y:bbi_max_y, bbi_min_x:bbi_max_x
                    ]

        annotations["boxes"] = new_boxes

        return new_image, annotations, new_mask


def get_test_labeled_images(
    no_annotations=False,
    multiple=False,
    png=False,
    polygonal=False,
    filename="",
    annotation_string="",
    path="./transform/test/",
):
    def read_from_name(name):
        img = imread(name).astype(np.float64) / 255
        # Read in with three channels since mask dataset is actually PNGs
        if img.shape[-1] > 3:
            img = img[:, :, :3]
        return img

    def mask_from_image_annotations(image, annotation, label2id):
        mask = np.zeros(image.shape[0:2])
        for box in annotation["boxes"][::-1]:
            if "points" not in box:
                x = box["x"]
                y = box["y"]
                w = box["width"]
                h = box["height"]
                box["points"] = [
                    [x - w / 2, y - h / 2],
                    [x + w / 2, y - h / 2],
                    [x + w / 2, y + h / 2],
                    [x - w / 2, y + h / 2],
                ]
            poly = Polygon(box["points"])
            ann_mask = rasterio.features.rasterize(
                [poly], out_shape=(mask.shape[0], mask.shape[1])
            )
            mask[ann_mask == 1] = label2id[box["label"]]
        return mask

    # TODO: Provide a choice of test images rather than hardcoding (e.g. chess, star, etc.)
    img_filename = (
        filename
        if filename
        else "star.jpg"
        if polygonal
        else "IMG_0310.png"
        if png
        else "IMG_0310.JPG"
    )

    if no_annotations:
        annotation = None
        mask = None
    else:
        if not annotation_string:
            if not polygonal:
                annotation_string = (
                    '{"key":"'
                    + img_filename
                    + '","boxes":[{"label":"black-king","x":1755,"y":462,"width":204,"height":326},{"label":"black-rook","x":1503.5,"y":256,"width":159,"height":218},{"label":"black-knight","x":1475.5,"y":1168,"width":193,"height":246},{"label":"black-pawn","x":1597.5,"y":833.5,"width":135,"height":169},{"label":"black-pawn","x":1187.5,"y":537,"width":123,"height":178},{"label":"black-bishop","x":1222.5,"y":832,"width":145,"height":234},{"label":"black-bishop","x":800,"y":226.5,"width":142,"height":241},{"label":"white-king","x":402,"y":602.5,"width":204,"height":343},{"label":"white-pawn","x":775.5,"y":832.5,"width":141,"height":181},{"label":"white-queen","x":1013.5,"y":228,"width":165,"height":278},{"label":"white-knight","x":449,"y":223,"width":182,"height":240},{"label":"white-bishop","x":1154,"y":108.5,"width":130,"height":215},{"label":"white-bishop","x":344.5,"y":978,"width":187,"height":240}],"width":2284,"height":1529}'
                )
                mask = None
            else:
                annotation_string = (
                    '{"key":"'
                    + img_filename
                    + '","width":300,"height":184,"boxes":[{"type":"polygon","label":"star","x":91.2817,"y":76.3750,"width":96.5276,"height":92.7500,"points":[[90.89713541666667,30],[106.11929820747756,60.58333333333333],[139.54552920049616,65.66666666666666],[115.28858850481433,88.5],[122.29059200459878,122.5],[92.19864839242996,106.75],[60.772989827921236,122.75],[68.19177925031188,88.83333333333333],[43.017909524896396,65.33333333333333],[76.94428362504242,61]]}]}'
                )
                labels = ["star"]
                label2id = {l: i + 1 for i, l in enumerate(labels)}
        annotation = json.loads(annotation_string)

    # get image
    img_path = path + img_filename
    image = read_from_name(img_path)
    if not no_annotations and polygonal:
        print("MAKING A MASK")
        mask = mask_from_image_annotations(image, annotation, label2id)

    images = [image]
    annotations = [annotation]
    masks = [mask]

    if multiple:
        if png:
            raise ValueError(
                "Currently cannot use multiple and png flags simultaneously"
            )

        if not polygonal:
            image_paths = [
                path + "masks/90.jpg",
                path + "masks/832.jpg",
                path + "masks/90.jpg",
                path + "masks/832.jpg",
            ]
            images = [read_from_name(path) for path in image_paths]

            ann90 = '{"key":"maksssksksss90.png","width":400,"height":267,"boxes":[{"label":"with_mask","x":63,"y":81,"width":34,"height":42},{"label":"with_mask","x":116.5,"y":103,"width":31,"height":42},{"label":"with_mask","x":193.5,"y":69,"width":27,"height":32},{"label":"with_mask","x":232,"y":72.5,"width":38,"height":45},{"label":"with_mask","x":218,"y":149,"width":40,"height":48},{"label":"with_mask","x":258,"y":31.5,"width":28,"height":27},{"label":"with_mask","x":324,"y":54.5,"width":28,"height":35},{"label":"with_mask","x":281,"y":43,"width":20,"height":22}]}'
            ann832 = '{"key":"maksssksksss832.png","width":309,"height":400,"boxes":[{"label":"mask_weared_incorrect","x":150,"y":162.5,"width":122,"height":167}]}'
            ann_strings = [ann90, ann832, ann90, ann832]
            annotations = [
                json.loads(ann_string) for ann_string in ann_strings
            ]
            masks = [None for im in images]
        else:
            image_paths = [path + "star.jpg" for _ in range(4)]
            images = [read_from_name(path) for path in image_paths]

            annotation_string = (
                '{"key":"'
                + img_filename
                + '","width":300,"height":184,"boxes":[{"type":"polygon","label":"star","x":91.2817,"y":76.3750,"width":96.5276,"height":92.7500,"points":[[90.89713541666667,30],[106.11929820747756,60.58333333333333],[139.54552920049616,65.66666666666666],[115.28858850481433,88.5],[122.29059200459878,122.5],[92.19864839242996,106.75],[60.772989827921236,122.75],[68.19177925031188,88.83333333333333],[43.017909524896396,65.33333333333333],[76.94428362504242,61]]}]}'
            )
            ann_strings = [
                annotation_string,
                annotation_string,
                annotation_string,
                annotation_string,
            ]
            annotations = [
                json.loads(ann_string) for ann_string in ann_strings
            ]
            masks = [
                mask_from_image_annotations(image, annotation, label2id)
                for image, annotation in zip(images, annotations)
            ]

    return images, annotations, masks


def test_augmentation(
    augmentation,
    args,
    kwargs,
    multiple=False,
    no_annotations=False,
    png=False,
    polygonal=False,
):
    images, annotations = get_test_labeled_images(
        no_annotations=no_annotations,
        multiple=multiple,
        png=png,
        polygonal=polygonal,
    )
    if multiple:
        result, annotations = augmentation(
            images, annotations, args, **kwargs
        ).call()
        result = draw_annotations(result[0], annotations[0])
    else:
        image = images[0]
        annotation = annotations[0]
        result, annotations = augmentation(
            image, annotation, args, **kwargs
        ).call()
        result = draw_annotations(result, annotations)

    plt.imshow(result)
    plt.show()
