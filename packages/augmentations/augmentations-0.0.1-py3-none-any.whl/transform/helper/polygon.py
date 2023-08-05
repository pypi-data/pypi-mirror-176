from shapely.geometry import Polygon as ShapelyPolygon


def annotation_points(annotation):
    """
    If annotation is polygonal, return points. Otherwise, return None.
    """
    if not annotation:
        return None
    return annotation.get("points", None)


class Polygon:
    def __init__(self, annotation):
        self.annotation = annotation
        self.points = annotation_points(self.annotation)

    def apply(self, func):
        if not self.points:
            return None
        self.points = func(self.points)
        return self.points

    def applied(self, func):
        if not self.points:
            return None
        return func(self.points)

    def valid(self):
        return self.points is not None

    def area(self):
        return ShapelyPolygon(self.points).area


def shift_points(x, y):
    def inner(points):
        return [[point[0] + x, point[1] + y] for point in points]

    return inner


def translate_points(left_edge, top_edge):
    def inner(points):
        return [
            [point[0] - left_edge, point[1] - top_edge] for point in points
        ]

    return inner


def scale_points(scale):
    def inner(points):
        return [[point[0] * scale, point[1] * scale] for point in points]

    return inner


def scale_points_xy(scale_x, scale_y):
    def inner(points):
        return [[point[0] * scale_x, point[1] * scale_y] for point in points]

    return inner


def transform_x(x):
    def inner(points):
        return [[x(point[0]), point[1]] for point in points]

    return inner


def transform_y(y):
    def inner(points):
        return [[point[0], y(point[1])] for point in points]

    return inner
