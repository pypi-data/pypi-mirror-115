#!/usr/bin/env python3
import sys
from argparse import ArgumentParser, Action, ArgumentError
from math import sqrt
from xml.etree import ElementTree

from qrcodegen import QrCode
from shapely.affinity import translate, scale
from shapely.geometry import Polygon, box

from qrpic.geom import rect_to_geom
from qrpic.svgdom import parse_svg_geometry, parse_svg_viewbox


def main(args):
    ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')
    tree = ElementTree.parse(args.svg)
    root = tree.getroot()

    viewbox = parse_svg_viewbox(root, args.ppi)

    if args.shell == 'viewbox':
        geom = rect_to_geom(viewbox)
    else:
        geom = parse_svg_geometry(root, args.shape_resolution, args.ppi)
        if args.shell == 'none':
            pass
        elif args.shell == 'convex':
            geom = geom.convex_hull
        elif args.shell == 'boundary-box':
            geom = box(*geom.bounds)
        else:
            raise AssertionError('invalid shell type supplied')

    viewbox_geom = rect_to_geom(viewbox)
    shape = viewbox_geom.intersection(geom)

    error_correction_mapping = {
        'high': QrCode.Ecc.HIGH,
        'medium': QrCode.Ecc.MEDIUM,
        'low': QrCode.Ecc.LOW,
    }
    qrcode = QrCode.encode_text(args.text, error_correction_mapping[args.error_correction])

    # Transforming the shape appropriately to intersect with QR code pixels.
    scale_factor = sqrt(qrcode.get_size()**2 * args.svg_area / (viewbox.width * viewbox.height))
    embedded_image_x = (qrcode.get_size() - scale_factor * viewbox.width) / 2
    embedded_image_y = (qrcode.get_size() - scale_factor * viewbox.height) / 2

    transformed_shape = translate(
        scale(
            shape,
            scale_factor,
            scale_factor,
            origin=(viewbox.x, viewbox.y),
        ),
        embedded_image_x - viewbox.x,
        embedded_image_y - viewbox.y,
    )

    if args.buffer > 0:
        transformed_shape = transformed_shape.buffer(
            args.buffer * scale_factor * sqrt(viewbox.width**2 + viewbox.height**2),
            args.shape_resolution)

    for y in range(qrcode.get_size()):
        for x in range(qrcode.get_size()):
            if qrcode.get_module(x, y):
                pixelshape = Polygon([(x, y), (x+1, y), (x+1, y+1), (x, y+1)])
                if pixelshape.intersects(transformed_shape):
                    # We use inofficial internas of qrcodegen that might break.
                    qrcode._modules[y][x] = False
                    continue

    qrcode_svg_root = ElementTree.fromstring(qrcode.to_svg_str(args.border))

    # Embed given SVG.
    root = tree.getroot()
    root.attrib['x'] = str(embedded_image_x + args.border)
    root.attrib['y'] = str(embedded_image_y + args.border)
    root.attrib['width'] = str(scale_factor * viewbox.width)
    root.attrib['height'] = str(scale_factor * viewbox.height)

    qrcode_svg_root.append(root)
    qrcode_svg_tree = ElementTree.ElementTree(qrcode_svg_root)

    # Write to file.
    qrcode_svg_tree.write(args.out)


class SVGAreaArgumentAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0 or values > 1:
            raise ArgumentError(self, 'value must lie between 0 and 1.')

        setattr(namespace, self.dest, values)


class BorderArgumentAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0:
            raise ArgumentError(self, 'value must be greater than or equal to 0.')

        setattr(namespace, self.dest, values)


class BufferArgumentAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0:
            raise ArgumentError(self, 'value must be greater than 0 or equal to 0.')

        setattr(namespace, self.dest, values)


class BufferResolutionAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 6:
            raise ArgumentError(self, 'value must be >= 6.')

        setattr(namespace, self.dest, values)


def create_arg_parser():
    parser = ArgumentParser(description='Generates QR-codes with centered logo images from SVGs in a beautiful '
                                        'manner, by not just overlaying them but also removing QR-code pixels properly '
                                        'so they do not interfere with the logo.\n\n'
                                        'Note that this tool does not (yet) check whether the generated QR-code is '
                                        'actually valid.')
    parser.add_argument('text', metavar='TEXT',
                        help='The QR-code text.')
    parser.add_argument('svg', metavar='SVG-FILE',
                        help='Logo SVG to center inside the QR code to be generated.')
    parser.add_argument('--out', default=sys.stdout.buffer, metavar='FILE',
                        help='Output filename. If none specified, outputs to stdout.')
    parser.add_argument('--shell', default='none', choices=('none', 'viewbox', 'convex', 'boundary-box'),
                        help='Different types of shells to enclose the given SVG shape where to remove QR-code '
                             'pixels.\n'
                             'none (default): No shell geometry is applied. Removes pixels as per geometry inside the '
                             'given svg.\n'
                             'viewbox: Assume the SVG defined viewbox to be the shell.\n'
                             'convex: Applies a convex hull.\n'
                             'boundary-box: Applies a minimal boundary box around the SVG geometry.')
    parser.add_argument('--ppi', default=96, type=float, metavar='VALUE',
                        help='Pixels per inch. Can be used to override the default value of 96 for SVGs as defined '
                             'per standard.')
    parser.add_argument('--svg-area', default=0.2, type=float, action=SVGAreaArgumentAction, metavar='VALUE',
                        help='Relative area of the SVG image to occupy inside the QR-code (default 0.2).')
    parser.add_argument('--border', default=1, type=int, action=BorderArgumentAction, metavar='VALUE',
                        help='Amount of border pixels around the final QR-code. Default is 1.')
    parser.add_argument('--error-correction', default='high', choices=('high', 'medium', 'low'),
                        help='QR-code error correction level. By default "high" for maximum tolerance.')
    parser.add_argument('--buffer', default=0.04, type=float, action=BufferArgumentAction, metavar='VALUE',
                        help='A round buffer around the SVG shape/shell to add (default is 0.04). The buffer is a '
                             'relative measure. To deactivate the buffer, just pass 0 as value.')
    parser.add_argument('--shape-resolution', default=32, type=int, action=BufferResolutionAction, metavar='VALUE',
                        help='The interpolation resolution of circular geometry such as SVG circles or buffers '
                             '(default 32).')

    return parser


def run():
    args = create_arg_parser().parse_args()
    sys.exit(main(args))


if __name__ == '__main__':
    run()
