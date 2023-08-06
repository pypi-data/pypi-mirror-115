import re
from typing import NamedTuple


class Matrix(NamedTuple):
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float


class Translate(NamedTuple):
    x: float
    y: float


class Scale(NamedTuple):
    x: float
    y: float


class Rotate(NamedTuple):
    angle: float
    axis_x: float
    axis_y: float


class SkewX(NamedTuple):
    angle: float


class SkewY(NamedTuple):
    angle: float


def parse_transforms(transforms_spec):
    transforms = []
    for match in re.finditer(r'([a-zA-Z0-9]+)\(([^()]*)\)', transforms_spec):
        id = match.group(1)
        args = [float(arg) for arg in re.split(r'\s+|\s*,\s*', match.group(2))]

        if id == 'matrix':
            if len(args) != 6:
                raise ValueError('matrix transform requires exactly 6 arguments')

            transform = Matrix(*args)

        elif id == 'translate':
            if len(args) < 1:
                raise ValueError('translate transform requires arguments')
            if len(args) > 2:
                raise ValueError('translate transform does not accept more than 2 arguments')

            x = args[0]
            y = args[1] if len(args) == 2 else 0

            transform = Translate(x, y)

        elif id == 'scale':
            if len(args) < 1:
                raise ValueError('scale transform requires arguments')
            if len(args) > 2:
                raise ValueError('scale transform does not accept more than 2 arguments')

            x = args[0]
            y = args[1] if len(args) == 2 else x

            transform = Scale(x, y)

        elif id == 'rotate':
            if len(args) != 1 and len(args) != 3:
                raise ValueError('rotate transform requires either 1 or 3 arguments')

            angle = args[0]
            axis_x, axis_y = args[1:3] if len(args) == 3 else (0, 0)

            transform = Rotate(angle, axis_x, axis_y)

        elif id == 'skewX':
            if len(args) != 1:
                raise ValueError('skewX transform requires exactly 1 argument')

            angle = args[0]

            transform = SkewX(angle)

        elif id == 'skewY':
            if len(args) != 1:
                raise ValueError('skewY transform requires exactly 1 argument')

            angle = args[0]

            transform = SkewY(angle)

        else:
            raise ValueError(f'unknown transform "{id}"')

        transforms.append(transform)

    # Transforms are applied right-to-left.
    return list(reversed(transforms))
