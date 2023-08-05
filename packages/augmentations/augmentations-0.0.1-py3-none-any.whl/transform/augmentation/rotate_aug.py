import numpy as np
import cv2
import math
import copy
import transform.augmentation.augmentation as augmentation
from transform.helper.polygon import Polygon, shift_points
from transform.helper.warpAffine import warpAffine


class RotateAugmentation(augmentation.Augmentation):
    """
    Rotates the image about its center and transforms annotations:
    counterclockwise for positive degree and clockwise for negative degree.
    :param img: <numpy.ndarray>
    :param annotations: <dict>
    :param degree: <int> angle by which to rotate
        (positive is counterclockwise)
    :param fillspace: <str> 'white', 'black', or 'mirror';
        what to fill extra space with when scale is larger than 1
    :return: <numpy.ndarray> rotated image, <dict> updated annotations
    """

    def __init__(self, img, annotations=None, mask=None, args=None, **kwargs):
        super().__init__(img, annotations, mask, args, **kwargs)
        self.kwargs["increases_size"] = True
        self.kwargs["degree"] = args[0]

    def update_image(self, mask=False):
        img = self.mask if mask else self.img
        self.kwargs["degree"] = float(self.kwargs["degree"])

        # rotate image
        rotated_img = self.rotate_image(img, self.kwargs["degree"])

        # crop to center
        final_img = rotated_img
        self.annotation_info = {
            "x_increment": (final_img.shape[1] - img.shape[1]) / 2,
            "y_increment": (final_img.shape[0] - img.shape[0]) / 2,
            "new_width": final_img.shape[1],
            "new_height": final_img.shape[0],
        }

        # OPTIONAL: fill in "dead pixels" of img canvas with fillspace argument

        return final_img

    def update_annotations(self):
        if self.truth("crop_to_center"):
            origin = (self.img.shape[1] / 2, self.img.shape[0] / 2)
        else:
            origin = (
                self.annotation_info["new_width"] / 2,
                self.annotation_info["new_height"] / 2,
            )

        # update annotations
        for (i, annotation) in enumerate(self.annotations.get("boxes", [])):
            if not self.truth("crop_to_center"):
                annotation["x"] += self.annotation_info["x_increment"]
                annotation["y"] += self.annotation_info["y_increment"]

                polygon = Polygon(annotation)
                if polygon.valid():
                    annotation["points"] = polygon.apply(
                        shift_points(
                            self.annotation_info["x_increment"],
                            self.annotation_info["y_increment"],
                        )
                    )

            new_annotation = RotateAugmentation.rotate_annotation(
                origin, annotation, self.kwargs["degree"]
            )
            self.annotations["boxes"][i] = new_annotation
        return self.annotations

    # https://blog.paperspace.com/data-augmentation-for-object-detection-rotation-and-shearing/
    def rotate_image(self, image, angle):
        """Rotate the image counterclockwise.

        Rotate the image such that the rotated image is enclosed inside the
        tightest rectangle. The area not occupied by the pixels of the original
        image is colored black.

        Parameters
        ----------

        image : numpy.ndarray
            numpy image

        angle : float
            angle by which the image is to be rotated. Positive angle is
            counterclockwise.

        Returns
        -------

        numpy.ndarray
            Rotated Image

        """
        # get dims, find center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # perform the actual rotation and return the image
        image = warpAffine(
            image, M, (nW, nH), self.truth("from_bounding_box_only")
        )

        # image = cv2.resize(image, (w,h))

        return image

    # adapted from
    # https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    @staticmethod
    def rotate_point(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        :param angle: <float> Angle in radians.
            Positive angle is counterclockwise.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    @staticmethod
    def rotate_annotation(origin, annotation, degree):
        """
        Rotates an annotation's bounding box by `degree`
            counterclockwise about `origin`.
        Assumes cropping from center to preserve image dimensions.
        :param origin: <tuple> down is positive
        :param annotation: <dict>
        :param degree: <int> degrees by which to rotate
            (positive is counterclockwise)
        :return: <dict> annotation after rotation
        """
        # Don't mutate annotation
        new_annotation = copy.deepcopy(annotation)
        # new_annotation = annotation

        angle = math.radians(degree)
        origin_x, origin_y = origin
        origin_y *= -1

        x = annotation["x"]
        y = annotation["y"]

        new_x, new_y = map(
            lambda x: round(x * 2) / 2,
            RotateAugmentation.rotate_point(
                (origin_x, origin_y), (x, -y), angle
            ),
        )

        new_annotation["x"] = new_x
        new_annotation["y"] = -new_y

        width = annotation["width"]
        height = annotation["height"]

        left_x = x - width / 2
        right_x = x + width / 2
        top_y = y - height / 2
        bottom_y = y + height / 2

        c1 = (left_x, top_y)
        c2 = (right_x, top_y)
        c3 = (right_x, bottom_y)
        c4 = (left_x, bottom_y)

        c1 = RotateAugmentation.rotate_point(origin, c1, angle)
        c2 = RotateAugmentation.rotate_point(origin, c2, angle)
        c3 = RotateAugmentation.rotate_point(origin, c3, angle)
        c4 = RotateAugmentation.rotate_point(origin, c4, angle)

        x_coords, y_coords = zip(c1, c2, c3, c4)
        new_annotation["width"] = round(max(x_coords) - min(x_coords))
        new_annotation["height"] = round(max(y_coords) - min(y_coords))

        def rotate_points(points):
            return [
                RotateAugmentation.rotate_point(origin, point, -angle)
                for point in points
            ]

        polygon = Polygon(annotation)
        if polygon.valid():
            new_annotation["points"] = polygon.apply(rotate_points)

        return new_annotation


if __name__ == "__main__":
    # augmentation.test_augmentation(
    #     RotateAugmentation, [123], {"bounding_box_only": False}
    # )
    # augmentation.test_augmentation(
    #     RotateAugmentation, [[40], [14], [1], [12], [-14], [15], [53], [40], [14], [1], [12], [-14], [15], [53], [40], [14], [1], [12], [-14], [15], [53]], {
    #         "bounding_box_only": True
    #     }, png=True  # fmt: skip
    # )
    # augmentation.test_augmentation(
    #     RotateAugmentation, [123], {"bounding_box_only": False}, polygonal=True
    # )
    augmentation.test_augmentation(
        RotateAugmentation,
        [[170]],
        {"bounding_box_only": True},
        polygonal=True,
    )
    augmentation.test_augmentation(
        RotateAugmentation, [[50]], {"bounding_box_only": True}, polygonal=True
    )
