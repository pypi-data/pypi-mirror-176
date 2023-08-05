import json

from skimage.io import imread
import matplotlib.pyplot as plt
from transform.helper.bounds import (
    Bounds,
    bound_polygon,
    multipolygon_to_boxes,
)

from transform.helper.polygon import Polygon
from transform.helper.rectangle_conversion import corner_to_center
from transform.helper.rectangle_conversion import box_to_edges
from transform.helper.draw_annotations import draw_annotations


def bound(annotation, img):
    """
    Deals with annotations, including those that have bounds beyond the image:
     - Returns cropped bounds for those beyond the image
     - Returns original bounds for those not beyond the image
    :param annotation: <dict> {'x', 'y', 'width', 'height'}
    :param img: <np.ndarray>
    :return: <tuple> (min_x, max_x, min_y, max_y)
    """

    input_width = img.shape[1]
    input_height = img.shape[0]

    x = annotation["x"]
    y = annotation["y"]
    width = annotation["width"]
    height = annotation["height"]

    if (
        (x - width / 2 < 0)
        or (y - height / 2 < 0)
        or (x + width / 2 > input_width)
        or (y + height / 2 > input_height)
    ):

        if (
            (x - width / 2 > input_width)
            or (y - height / 2 > input_height)
            or (x + width / 2 < 0)
            or (y + height / 2 < 0)
        ):
            # entirely out of frame
            return

        if x - width / 2 < 0:
            min_x = 0
        else:
            min_x = int(x - width / 2)

        if y - height / 2 < 0:
            min_y = 0
        else:
            min_y = int(y - height / 2)

        if x + width / 2 > input_width:
            max_x = input_width
        else:
            max_x = int(x + width / 2)

        if y + height / 2 > input_height:
            max_y = input_height
        else:
            max_y = int(y + height / 2)

        if (max_x < min_x) or (max_y < min_y):
            print(f"min_x: {min_x}")
            print(f"max_x: {max_x}")
            print(f"min_y: {min_y}")
            print(f"max_y: {max_y}")
            raise Exception(
                "max_x is less than min_x or max_y is less than min_y"
            )
    else:
        (min_x, max_x, min_y, max_y) = box_to_edges(annotation)
    return (min_x, max_x, min_y, max_y)


def trim_annotations(img, annotations, mask, keep=20):
    """
    Deals with annotations that have bounds beyond the image:
     - Drops annotations that
            + don't have newArea/oldArea > keep% and also
            + donn't have newArea/imageArea > keep%
     - Crops annotations that do have enough area.

    :param img: <numpy.ndarray> numpy array of shape (height, width, channels)
    :param annotations: <div> annotations dictionary
    :param keep: <float> minimum fraction of original area needed
        to be kept as an annotation, ranging from 0 to 1
    :return: <numpy.ndarray> unmodified image, <dict> kept annotations
    """
    if not annotations:
        return img, annotations, mask

    keep = float(keep) / 100

    annotations_to_keep = []

    img_width = img.shape[1]
    img_height = img.shape[0]

    image_area = img_width * img_height

    for annotation in annotations.get("boxes", []):
        if annotation is None:
            # Bad data was passed
            continue

        polygon = Polygon(annotation)

        boxes_to_check = []

        ann_bounds = bound(annotation, img)

        # if out of bounds
        if not ann_bounds:
            continue

        if polygon.valid():
            bounds = Bounds([0, img_width, 0, img_height])
            multipolygon_pts = bound_polygon(polygon.points, bounds)
            boxes_to_check.extend(
                multipolygon_to_boxes(
                    multipolygon_pts, label=annotation.get("label", "")
                )
            )
        else:
            boxes_to_check.append(annotation)

        if polygon.valid():
            ann_area = polygon.area()
        else:
            ann_area = annotation["width"] * annotation["height"]
        if ann_area <= 0:
            print(
                "trim_annotations: annotation area",
                ann_area,
                "is not positive!",
            )
            continue
        (min_x, max_x, min_y, max_y) = ann_bounds
        for box in boxes_to_check:
            polygon = Polygon(box)
            if polygon.valid():
                area_in_bounds = polygon.area()
            else:
                area_in_bounds = (max_x - min_x) * (max_y - min_y)

            if (
                area_in_bounds / ann_area >= keep
                or area_in_bounds / image_area >= keep
            ):
                dictionary = corner_to_center((min_x, min_y), (max_x, max_y))
                annotation["x"] = dictionary["x"]
                annotation["y"] = dictionary["y"]
                annotation["width"] = dictionary["width"]
                annotation["height"] = dictionary["height"]
                annotations_to_keep.append(box)
            else:
                continue
                # print(f"not enough area to keep: {area_in_bounds / total_area} but {keep} needed")

    annotations["boxes"] = annotations_to_keep

    return img, annotations, mask


if __name__ == "__main__":
    from transform.augmentation.random_crop_aug import (
        RandomCropAugmentation,
    )  # for testing

    annotation_string = '{"key":"IMG_0310.JPG","boxes":[{"label":"black-king","x":1755,"y":462,"width":204,"height":326},{"label":"black-rook","x":1503.5,"y":256,"width":159,"height":218},{"label":"black-knight","x":1475.5,"y":1168,"width":193,"height":246},{"label":"black-pawn","x":1597.5,"y":833.5,"width":135,"height":169},{"label":"black-pawn","x":1187.5,"y":537,"width":123,"height":178},{"label":"black-bishop","x":1222.5,"y":832,"width":145,"height":234},{"label":"black-bishop","x":800,"y":226.5,"width":142,"height":241},{"label":"white-king","x":402,"y":602.5,"width":204,"height":343},{"label":"white-pawn","x":775.5,"y":832.5,"width":141,"height":181},{"label":"white-queen","x":1013.5,"y":228,"width":165,"height":278},{"label":"white-knight","x":449,"y":223,"width":182,"height":240},{"label":"white-bishop","x":1154,"y":108.5,"width":130,"height":215},{"label":"white-bishop","x":344.5,"y":978,"width":187,"height":240}],"width":2284,"height":1529}'
    annotation_dict = json.loads(annotation_string)

    # get image
    img_path = "./data/IMG_0310.JPG"
    image = imread(img_path)

    result, annotations = RandomCropAugmentation(
        img=image, annotations=annotation_dict, scale=50, fillspace=None
    ).call()
    img, trimmed_annotations = trim_annotations(result, annotations, 0)

    img = draw_annotations(img, trimmed_annotations)

    print(trimmed_annotations)

    plt.imshow(img)
    plt.show()
