import re
import sys
from enum import Enum
from math import pi, sin, cos
from typing import NamedTuple, Tuple

import shapely.geometry
from shapely.affinity import translate, scale
from shapely.ops import unary_union
import svg.path

from qrpic.geom import complex_to_point, rect_to_geom
from qrpic.itertools import grouper
from qrpic.svgdom.transforms import parse_transforms, Rotate, Translate, Matrix, Scale, SkewX, SkewY


DEFAULT_PPI = 96.0
DEFAULT_SHAPE_RESOLUTION = 32


class ParseError(Exception):
    pass


class Unit(Enum):
    PIXELS = 'px'
    POINTS = 'pt'
    PICAS = 'pc'
    CENTIMETERS = 'cm'
    MILLIMETERS = 'mm'
    INCHES = 'in'
    USER = ''


_CONVERSION_TABLE_INCH_REAL_MEASURES = {
    Unit.POINTS: 1 / 72,
    Unit.PICAS: 1 / 6,
    Unit.CENTIMETERS: 1 / 2.54,
    Unit.MILLIMETERS: 1 / 25.4,
    Unit.INCHES: 1.0,
}
CONVERSION_TABLE_INCH_REAL_MEASURES_REVERSE = {
    unit: 1 / val for unit, val in _CONVERSION_TABLE_INCH_REAL_MEASURES.items()
}


class Measure(NamedTuple):
    value: float
    unit: Unit

    @classmethod
    def from_string(cls, string: str):
        match = re.fullmatch(rf'(\d+(?:.\d+)?)({"|".join(v.value for v in Unit)})', string)

        if match is None:
            raise ValueError

        return cls(float(match.group(1)), Unit(match.group(2)))

    def convert(self, unit: Unit, ppi=DEFAULT_PPI):
        if self.unit == unit:
            return self

        if self.unit is Unit.USER or self.unit is Unit.PIXELS:
            unitless = self.value
        else:
            unitless = _CONVERSION_TABLE_INCH_REAL_MEASURES[self.unit] * ppi * self.value

        if unit is Unit.USER or unit is Unit.PIXELS:
            return Measure(unitless, unit)
        else:
            return Measure(_CONVERSION_TABLE_INCH_REAL_MEASURES[unit] / ppi * unitless, unit)


class Point(NamedTuple):
    x: float
    y: float


class Line(NamedTuple):
    p1: Point
    p2: Point

    @classmethod
    def from_svg_element(cls, elem, ppi=DEFAULT_PPI):
        return cls(
            Point(
                Measure.from_string(elem.attrib['x1']).convert(Unit.USER, ppi).value,
                Measure.from_string(elem.attrib['y1']).convert(Unit.USER, ppi).value,
            ),
            Point(
                Measure.from_string(elem.attrib['x2']).convert(Unit.USER, ppi).value,
                Measure.from_string(elem.attrib['y2']).convert(Unit.USER, ppi).value,
            ),
        )


class Polygon(NamedTuple):
    points: Tuple[Point]

    @classmethod
    def from_svg_element(cls, elem):
        return cls(tuple(parse_points(elem.attrib['points'])))


class Polyline(NamedTuple):
    points: Tuple[Point]

    @classmethod
    def from_svg_element(cls, elem):
        return cls(tuple(parse_points(elem.attrib['points'])))


class Rect(NamedTuple):
    x: float
    y: float
    width: float
    height: float

    @classmethod
    def from_svg_element(cls, elem, ppi=DEFAULT_PPI):
        return cls(
            Measure.from_string(elem.attrib['x']).convert(Unit.USER, ppi).value if 'x' in elem.attrib else 0,
            Measure.from_string(elem.attrib['y']).convert(Unit.USER, ppi).value if 'y' in elem.attrib else 0,
            Measure.from_string(elem.attrib['width']).convert(Unit.USER, ppi).value if 'width' in elem.attrib else 0,
            Measure.from_string(elem.attrib['height']).convert(Unit.USER, ppi).value if 'height' in elem.attrib else 0,
        )


class Ellipse(NamedTuple):
    center: Point
    radius: Point

    @classmethod
    def from_svg_element(cls, elem, ppi=DEFAULT_PPI):
        return cls(
            Point(
                Measure.from_string(elem.attrib['cx']).convert(Unit.USER, ppi).value,
                Measure.from_string(elem.attrib['cy']).convert(Unit.USER, ppi).value,
            ),
            Point(
                Measure.from_string(elem.attrib['rx']).convert(Unit.USER, ppi).value,
                Measure.from_string(elem.attrib['ry']).convert(Unit.USER, ppi).value,
            ),
        )


class Circle(NamedTuple):
    center: Point
    radius: float

    @classmethod
    def from_svg_element(cls, elem, ppi=DEFAULT_PPI):
        return cls(
            Point(
                Measure.from_string(elem.attrib['cx']).convert(Unit.USER, ppi).value,
                Measure.from_string(elem.attrib['cy']).convert(Unit.USER, ppi).value,
            ),
            Measure.from_string(elem.attrib['r']).convert(Unit.USER, ppi).value,
        )


def parse_points(pts):
    return [(float(x), float(y)) for x, y in grouper(re.split(r'[ ,]+', pts), 2)]


def parse_svg_viewbox(root, ppi=DEFAULT_PPI):
    if 'viewBox' in root.attrib:
        x, y, width, height = (Measure.from_string(value.strip()) for value in root.attrib['viewBox'].split(' '))
    else:
        x = Measure(0, Unit.USER)
        y = Measure(0, Unit.USER)
        width = None
        height = None

        if 'width' in root.attrib:
            width = Measure.from_string(root.attrib['width'].strip())
        if 'height' in root.attrib:
            height = Measure.from_string(root.attrib['height'].strip())

        if width is None and height is None:
            raise ParseError('missing width or height or viewBox - unable to determine svg dimensions')

        if width is None:
            width = height
        elif height is None:
            height = width
        else:
            raise AssertionError

    # Convert viewbox units to unitless/user values.
    x, y, width, height = (v.convert(Unit.USER, ppi).value for v in (x, y, width, height))
    viewbox = Rect(x, y, width, height)

    return viewbox


def parse_svg_geometry(elem, resolution=DEFAULT_SHAPE_RESOLUTION, ppi=DEFAULT_PPI):
    geom = parse_svg_group_geometry(elem, resolution, ppi)

    viewbox = parse_svg_viewbox(elem)
    viewbox_geom = rect_to_geom(viewbox)
    geom = viewbox_geom.intersection(geom)

    return geom


def parse_svg_group_geometry(elem, resolution=DEFAULT_SHAPE_RESOLUTION, ppi=DEFAULT_PPI):
    shapes = []

    for child in elem:
        match = re.fullmatch(r'{[^}]*?\}(.*)', child.tag)
        tag = match.group(1)

        if tag == 'rect':
            nested_rc = Rect.from_svg_element(child, ppi)

            geom = shapely.geometry.LinearRing([
                (nested_rc.x, nested_rc.y),
                (nested_rc.x + nested_rc.width, nested_rc.y),
                (nested_rc.x + nested_rc.width, nested_rc.y + nested_rc.height),
                (nested_rc.x, nested_rc.y + nested_rc.height),
            ])

        elif tag == 'path':
            path = svg.path.parse_path(child.attrib['d'])

            # Path specs are always specified in user units, so no conversion necessary.
            # See https://www.w3.org/TR/SVG/paths.html.
            # TODO I need to either define a polygon or a line string or a line ring, depending on whether it is filled
            #   or not.
            geoms = []
            points = []
            for primitive in path:
                if isinstance(primitive, svg.path.Line):
                    points.append(complex_to_point(primitive.end))
                elif isinstance(primitive, svg.path.CubicBezier):
                    for i in range(resolution):
                        x = i / (resolution - 1)
                        pt = complex_to_point(
                            (1 - x)**3 * primitive.start +
                            3 * (1 - x)**2 * x * primitive.control1 +
                            3 * (1 - x) * x**2 * primitive.control2 +
                            x**3 * primitive.end)
                        points.append(pt)
                elif isinstance(primitive, svg.path.QuadraticBezier):
                    for i in range(resolution):
                        x = i / (resolution - 1)
                        pt = complex_to_point(
                            (1 - x)**2 * primitive.start +
                            2 * (1 - x) * x * primitive.control +
                            x**2 * primitive.end)
                        points.append(pt)
                elif isinstance(primitive, svg.path.Close):
                    if points:
                        geoms.append(shapely.geometry.Polygon(points))
                        points = []
                elif isinstance(primitive, svg.path.Move):
                    if points:
                        geoms.append(shapely.geometry.LineString(points))
                        points = []
                elif isinstance(primitive, svg.path.Arc):
                    print('WARNING: Arc paths are not supported yet! See https://gitlab.com/Makman2/qrpic/-/issues/4',
                          file=sys.stderr)
                    points.append(complex_to_point(primitive.end))
                else:
                    print(f'WARNING: Unsupported path primitive encountered: {primitive}', file=sys.stderr)
                    points.append(complex_to_point(primitive.end))

            if points:
                geoms.append(shapely.geometry.LineString(points))

            geom = unary_union(geoms)

        elif tag == 'line':
            line = Line.from_svg_element(child, ppi)

            geom = shapely.geometry.LineString([(line.p1.x, line.p1.y), (line.p2.x, line.p2.y)])

        elif tag == 'polygon':
            poly = Polygon.from_svg_element(child)
            geom = shapely.geometry.Polygon(poly.points)

        elif tag == 'polyline':
            # TODO If polylines have a filling, their shape changes.
            #  Check here the filling attributes and compute shape/geom accordingly.
            polyline = Polyline.from_svg_element(child)
            geom = shapely.geometry.LineString(polyline.points)

        elif tag == 'circle':
            circle = Circle.from_svg_element(child, ppi)

            points = []
            for i in range(resolution):
                angle = i * 2 * pi / resolution
                pt = (circle.center.x + cos(angle) * circle.radius,
                      circle.center.y + sin(angle) * circle.radius)
                points.append(pt)

            geom = shapely.geometry.Polygon(points)

        elif tag == 'ellipse':
            ellipse = Ellipse.from_svg_element(child, ppi)

            points = []
            for i in range(resolution):
                angle = i * 2 * pi / resolution
                pt = (ellipse.center.x + cos(angle) * ellipse.radius.x,
                      ellipse.center.y + sin(angle) * ellipse.radius.y)
                points.append(pt)

            geom = shapely.geometry.Polygon(points)

        elif tag == 'svg':
            nested_shape = parse_svg_geometry(child, resolution, ppi)
            nested_viewbox = parse_svg_viewbox(child, ppi)

            # TODO Rect.from_svg_element doesn't properly take care of all cases for an <svg>-element. A custom
            #  function is needed.
            nested_rc = Rect.from_svg_element(child, ppi)

            geom = translate(
                scale(
                    nested_shape,
                    nested_rc.width / nested_viewbox.width,
                    nested_rc.height / nested_viewbox.height,
                    origin=(nested_viewbox.x, nested_viewbox.y)
                ),
                nested_rc.x - nested_viewbox.x,
                nested_rc.y - nested_viewbox.y,
            )

        elif tag == 'g':
            geom = parse_svg_group_geometry(child, resolution, ppi)

        else:
            continue

        # Apply transformations.

        if 'transform' in child.attrib:
            transformations = parse_transforms(child.attrib['transform'])

            for transform in transformations:
                if isinstance(transform, Translate):
                    geom = shapely.affinity.translate(geom, transform.x, transform.y)
                elif isinstance(transform, Scale):
                    geom = shapely.affinity.scale(geom, transform.x, transform.y, origin=(0, 0))
                elif isinstance(transform, Rotate):
                    geom = shapely.affinity.rotate(geom, transform.angle, (transform.axis_x, transform.axis_y))
                elif isinstance(transform, SkewX):
                    geom = shapely.affinity.skew(geom, xs=transform.angle)
                elif isinstance(transform, SkewY):
                    geom = shapely.affinity.skew(geom, ys=transform.angle)
                elif isinstance(transform, Matrix):
                    geom = shapely.affinity.affine_transform(geom,
                                                             (transform.a, transform.c, transform.b,
                                                              transform.d, transform.e, transform.f))
                else:
                    pass  # Ignore unknown transforms.

        shapes.append(geom)

    shape = unary_union(shapes)

    return shape
