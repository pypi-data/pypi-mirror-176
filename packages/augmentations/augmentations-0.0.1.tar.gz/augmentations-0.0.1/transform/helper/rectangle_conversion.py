import unittest
import warnings


class TestCoordinateConversions(unittest.TestCase):
    def test_corner_to_center(self):
        self.assertEqual(
            corner_to_center((0, 0), (2, 2)),
            {"x": 1, "y": 1, "width": 2, "height": 2},
        )
        self.assertEqual(
            corner_to_center((0, 0), (2, 2), (0, 2), (2, 0)),
            {"x": 1, "y": 1, "width": 2, "height": 2},
        )
        self.assertEqual(
            corner_to_center((-5, 1), (9, 4)),
            {"x": 2, "y": 2.5, "width": 14, "height": 3},
        )
        self.assertWarns(Warning, corner_to_center, (1, 4), (1, 4))
        self.assertWarns(Warning, corner_to_center, (-2, -3), (-2, 5))
        self.assertRaises(
            Exception, corner_to_center, (-2, -3), (-4, 5), (10, 10), (9, -1)
        )
        self.assertRaises(Exception, corner_to_center, (0, 0), (2, 2), (0, 2))

    def test_center_to_corner(self):
        self.assertTupleEqual(
            center_to_corner({"x": 1, "y": 1, "width": 2, "height": 2}),
            ((0, 0), (2, 0), (2, 2), (0, 2)),
        )
        self.assertTupleEqual(
            center_to_corner({"x": -10, "y": -4, "width": 6, "height": 4}),
            ((-13, -6), (-7, -6), (-7, -2), (-13, -2)),
        )
        self.assertTupleEqual(
            center_to_corner({"x": 1, "y": 2, "width": 7, "height": 3}),
            ((-2.5, 0.5), (4.5, 0.5), (4.5, 3.5), (-2.5, 3.5)),
        )
        self.assertWarns(
            Warning,
            center_to_corner,
            {"x": 1, "y": 6, "width": 0, "height": 1},
        )
        self.assertWarns(
            Warning,
            center_to_corner,
            {"x": 3, "y": -5, "width": 0, "height": 0},
        )


def is_rectangle(c1, c2):
    return (c1[0] != c2[0]) and (c1[1] != c2[1])


def corner_to_center(c1, c2, c3=None, c4=None):
    """
    Converts coordinates from corner points to center/dimensions.

    c1, c2 or c1, c2, c3, c4: coordinates in form (x, y); can be in any order

    Returns dictionary of form {x, y, width, height}
    """
    if not ((c1 and c2 and not c3 and not c4) or (c1 and c2 and c3 and c4)):
        raise Exception("Invalid arguments passed")

    if c3 and c4:
        x_coordinates, y_coordinates = zip(c1, c2, c3, c4)
    else:
        if not is_rectangle(c1, c2):
            warnings.warn("Degenerate rectangle")
        x_coordinates, y_coordinates = zip(c1, c2)

    left_bound = min(x_coordinates)
    right_bound = max(x_coordinates)
    top_bound = min(y_coordinates)
    bottom_bound = max(y_coordinates)

    if c3 and c4:
        if not (
            x_coordinates.count(left_bound) == 2
            and x_coordinates.count(right_bound) == 2
            and y_coordinates.count(top_bound) == 2
            and y_coordinates.count(bottom_bound) == 2
        ):
            raise Exception("Rectangle coordinates don't match up")

    center_x = (left_bound + right_bound) / 2
    center_y = (top_bound + bottom_bound) / 2
    width = right_bound - left_bound
    height = bottom_bound - top_bound

    return {"x": center_x, "y": center_y, "width": width, "height": height}


def center_to_corner(dictionary):
    """
    Converts coordinates from center/dimensions to corner points.

    dictionary: dictionary in the form {x, y, width, height}

    Returns points in the form c1, c2, c3, c4, in the order shown below.

    c1 ---- c2
    |        |
    |        |
    c4 ---- c3
    """

    left_bound, right_bound, top_bound, bottom_bound = box_to_edges(dictionary)

    c1 = (left_bound, top_bound)
    c2 = (right_bound, top_bound)
    c3 = (right_bound, bottom_bound)
    c4 = (left_bound, bottom_bound)

    return c1, c2, c3, c4


def box_to_edges(dictionary):
    """
    :return: left_bound, right_bound, top_bound, bottom_bound
    """
    x = dictionary["x"]
    y = dictionary["y"]
    width = dictionary["width"]
    height = dictionary["height"]

    if width == 0 or height == 0:
        warnings.warn("Degenerate rectangle")

    left_bound = x - width / 2
    right_bound = x + width / 2
    top_bound = y - height / 2
    bottom_bound = y + height / 2

    return left_bound, right_bound, top_bound, bottom_bound


if __name__ == "__main__":
    unittest.main()
