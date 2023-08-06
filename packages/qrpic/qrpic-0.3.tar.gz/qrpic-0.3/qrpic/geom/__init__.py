from shapely.geometry import box


def rect_to_geom(rect):
    return box(rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)


def complex_to_point(c: complex):
    return c.real, c.imag
