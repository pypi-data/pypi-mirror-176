from geojson import Feature
from turfpy.transformation import bbox_clip
from shapely.geometry import Polygon
from shapely.validation import make_valid


class Bounds:
    """
    An abstract state representing a bounding box.

    One of the following representations:
        -{
            'x': <float> | <int>,
            'y': <float> | <int>,
            'width': <float> | <int>,
            'height: <float> | <int>
        }
        -[left_edge: <float>, right_edge: <float>, top_edge: <float>, bottom_edge: <float>]
    """

    def __init__(self, bounds):
        if isinstance(bounds, dict):
            if all([part in bounds for part in ("x", "y", "width", "height")]):
                self.x = bounds["x"]
                self.y = bounds["y"]
                self.width = bounds["width"]
                self.height = bounds["height"]
            else:
                raise ValueError(
                    "Received dictionary bounds, but does not contain necessary keys"
                )
        elif isinstance(bounds, list):
            if (
                len(bounds) == 4
                and bounds[1] >= bounds[0]
                and bounds[3] >= bounds[2]
            ):
                self.x = (bounds[0] + bounds[1]) / 2
                self.y = (bounds[2] + bounds[3]) / 2
                self.width = bounds[1] - bounds[0]
                self.height = bounds[3] - bounds[2]
            else:
                raise ValueError("Received list, but format is incorrect")

    def to_edges(self):
        """Returns edges"""
        left_edge = self.x - self.width / 2
        right_edge = self.x + self.width / 2
        top_edge = self.y - self.height / 2
        bottom_edge = self.y + self.height / 2

        return {
            "left_edge": left_edge,
            "right_edge": right_edge,
            "top_edge": top_edge,
            "bottom_edge": bottom_edge,
        }

    def area(self):
        return self.width * self.height

    def contains(self, x, y):
        edges = self.to_edges()
        left_edge = edges["left_edge"]
        right_edge = edges["right_edge"]
        top_edge = edges["top_edge"]
        bottom_edge = edges["bottom_edge"]
        return left_edge < x < right_edge and top_edge < y < bottom_edge

    def deserialized(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def slope(self):
        return (self.y2 - self.y1) / (self.x2 - self.x1)

    def as_f_x(self, x):
        delta_x = x - self.x1
        return self.slope() * delta_x + self.y1

    def as_f_y(self, y):
        delta_y = y - self.y1
        return delta_y / self.slope() + self.x1


# Bounds, but can tell where a ray (directed line) intersects
class IntersecterBounds(Bounds):
    def __init__(self, bounds):
        super().__init__(bounds.deserialized())

    def find_intersection_point(self, line):
        edges = self.to_edges()
        left_edge = edges["left_edge"]
        right_edge = edges["right_edge"]
        top_edge = edges["top_edge"]
        bottom_edge = edges["bottom_edge"]

        intersection_point = None

        # Left
        if (
            line.x1 > line.x2
            and top_edge < line.as_f_x(left_edge) < bottom_edge
        ):
            intersection_point = (left_edge, line.as_f_x(left_edge))

        # Right
        if (
            line.x1 < line.x2
            and top_edge < line.as_f_x(right_edge) < bottom_edge
        ):
            intersection_point = (right_edge, line.as_f_x(right_edge))

        # Top
        if (
            line.y1 > line.y2
            and left_edge < line.as_f_y(top_edge) < right_edge
        ):
            intersection_point = (line.as_f_y(top_edge), top_edge)

        # Bottom
        if (
            line.y1 < line.y2
            and left_edge < line.as_f_y(bottom_edge) < right_edge
        ):
            intersection_point = (line.as_f_y(bottom_edge), bottom_edge)

        return intersection_point


# Returns tightest bounding box of a polygon
def polygon_to_box(points):
    if (
        not points
        or not isinstance(points, list)
        or len(points) == 0
        or not isinstance(points[0], list)
        or len(points[0]) < 1
    ):
        return None

    x_min = points[0][0]
    x_max = points[0][0]
    y_min = points[0][1]
    y_max = points[0][1]

    for point in points:
        x_min = min(x_min, point[0])
        x_max = max(x_max, point[0])
        y_min = min(y_min, point[1])
        y_max = max(y_max, point[1])

    return Bounds([x_min, x_max, y_min, y_max])


def bound_polygon(points, bounds):
    edges = bounds.to_edges()
    bbox = [
        edges["left_edge"],
        edges["top_edge"],
        edges["right_edge"],
        edges["bottom_edge"],
    ]
    p = Polygon(points)
    p = make_valid(p)
    f = Feature(geometry=p)
    bc = bbox_clip(f, bbox)
    if not bc or "coordinates" not in bc["geometry"]:
        return []

    multipolygon_pts = bc["geometry"]["coordinates"]
    if bc["geometry"]["type"] == "MultiPolygon":
        multipolygon_pts = [pts[0] for pts in multipolygon_pts]
    return multipolygon_pts


def multipolygon_to_boxes(multipolygon_pts, label=""):
    boxes = []
    for polygon_pts in multipolygon_pts:
        bounds = polygon_to_box(polygon_pts)
        if bounds is not None:
            deserialized = bounds.deserialized()

            boxes.append(
                {
                    "type": "polygon",
                    "label": label,
                    "x": deserialized["x"],
                    "y": deserialized["y"],
                    "width": deserialized["width"],
                    "height": deserialized["height"],
                    "points": polygon_pts,
                }
            )
    return boxes


def bound_polygon_old(points, bounds):
    if len(points) < 1:
        return points

    # Allow bounded points to circle back to beginning
    points.append(points[0])

    intersecter_bounds = IntersecterBounds(bounds)

    points_bounded = []
    outside_points_stack = []
    for point in points:
        (x2, y2) = point
        contained = intersecter_bounds.contains(x2, y2)
        if contained:
            if len(outside_points_stack) > 0:
                (x1, y1) = outside_points_stack.pop()
                outside_points_stack.clear()
                ray = Line(x2, y2, x1, y1)
                intersection_point = (
                    intersecter_bounds.find_intersection_point(ray)
                )
                if not intersection_point:
                    raise Exception(
                        "bound_polygon: no intersection point found"
                    )

                points_bounded.append(intersection_point)

            points_bounded.append(point)
        else:
            outside_points_stack.append(point)
            if len(points_bounded) == 0:
                continue
            (x1, y1) = points_bounded[-1]
            ray = Line(x1, y1, x2, y2)
            intersection_point = intersecter_bounds.find_intersection_point(
                ray
            )
            if not intersection_point:
                raise Exception("bound_polygon: no intersection point found")

            points_bounded.append(intersection_point)
    return points_bounded
