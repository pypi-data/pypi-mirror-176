import cv2
import numpy as np

from transform.helper.polygon import annotation_points
from transform.helper.rectangle_conversion import center_to_corner


# adapted from https://blog.paperspace.com/data-augmentation-for-bounding-boxes
def draw_annotations(img, annotations, color=[1, 0, 0]):
    """Draws annotations on `image`

    :param image: <numpy.ndarray>
    :param annotations: <dict>
    :param color: <list> rgb ranging from 0 to 1
    :return: <numpy.ndarray> image with bounding boxes drawn on it
    """

    for annotation in annotations.get("boxes", []):

        pt1, pt3, pt2, pt4 = center_to_corner(annotation)

        pt1 = int(pt1[0]), int(pt1[1])
        pt2 = int(pt2[0]), int(pt2[1])

        thickness = int(max(img.shape[:2]) / 200)

        img = cv2.rectangle(img.copy(), pt1, pt2, color, thickness)

        pts = annotation_points(annotation)
        if pts:
            pts = np.array(pts, dtype=np.int32)
            pts = np.reshape(pts, (-1, 1, 2))
            img = cv2.polylines(
                img.copy(), [pts], True, color=[0, 0, 1], thickness=thickness
            )

    return img
