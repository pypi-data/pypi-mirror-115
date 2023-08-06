# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qrpic', 'qrpic.geom', 'qrpic.itertools', 'qrpic.svgdom']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.7.1,<2.0.0', 'qrcodegen>=1.6.0,<2.0.0', 'svg.path>=4.1,<5.0']

entry_points = \
{'console_scripts': ['qrpic = qrpic.main:run']}

setup_kwargs = {
    'name': 'qrpic',
    'version': '0.3',
    'description': 'Create beautiful QR-codes with perfectly fitting logos!',
    'long_description': 'qrpic\n=====\n\nA command-line tool to create beautiful QR-codes with perfectly fitting logos!\n\nUsage\n-----\n\nqrpic takes (for the moment) only SVG images and produces an output SVG.\nYou invoke it simply with\n\n.. code-block:: bash\n\n    qrpic "data text or link you want in your qr code" path-to-logo.svg\n\nqrpic computes the exact shape of the SVG and removes QR-code pixels that are\nin the way, so they don\'t disturb your logo.\n\nqrpic offers various options to control the logo size, adding shells and buffer\nareas around your logo so it looks proper with just the right amount of spacing.\nFor more info, query ``qrpic --help``::\n\n    usage: qrpic [-h] [--out FILE] [--shell {none,viewbox,convex,boundary-box}]\n                 [--ppi VALUE] [--svg-area VALUE] [--border VALUE]\n                 [--error-correction {high,medium,low}] [--buffer VALUE]\n                 [--shape-resolution VALUE]\n                 TEXT SVG-FILE\n\n    Generates QR-codes with centered logo images from SVGs in a beautiful manner,\n    by not just overlaying them but also removing QR-code pixels properly so they\n    do not interfere with the logo. Note that this tool does not (yet) check\n    whether the generated QR-code is actually valid.\n\n    positional arguments:\n      TEXT                  The QR-code text.\n      SVG-FILE              Logo SVG to center inside the QR code to be generated.\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      --out FILE            Output filename. If none specified, outputs to stdout.\n      --shell {none,viewbox,convex,boundary-box}\n                            Different types of shells to enclose the given SVG\n                            shape where to remove QR-code pixels. none (default):\n                            No shell geometry is applied. Removes pixels as per\n                            geometry inside the given svg. viewbox: Assume the SVG\n                            defined viewbox to be the shell. convex: Applies a\n                            convex hull. boundary-box: Applies a minimal boundary\n                            box around the SVG geometry.\n      --ppi VALUE           Pixels per inch. Can be used to override the default\n                            value of 96 for SVGs as defined per standard.\n      --svg-area VALUE      Relative area of the SVG image to occupy inside the\n                            QR-code (default 0.2).\n      --border VALUE        Amount of border pixels around the final QR-code.\n                            Default is 1.\n      --error-correction {high,medium,low}\n                            QR-code error correction level. By default "high" for\n                            maximum tolerance.\n      --buffer VALUE        A round buffer around the SVG shape/shell to add\n                            (default is 0.04). The buffer is a relative measure.\n                            To deactivate the buffer, just pass 0 as value.\n      --shape-resolution VALUE\n                            The interpolation resolution of circular geometry such\n                            as SVG circles or buffers (default 32).\n\n.. note::\n\n    qrpic is currently very much a prototype. It works, but the SVG parsing and\n    shape extraction capabilities are in the moment limited.\n    If you encounter such a limitation or ugly output, please\n    `file an issue <https://gitlab.com/Makman2/qrpic/issues>`_!\n\nRoadmap\n-------\n\n- Better SVG parsing and shape extraction\n- Support non-vector graphics such as PNG, JPG, etc. Properly handle\n  image transparency\n- QR-code verification step\n- Use minimally necessary QR-code error correction level\n',
    'author': 'Mischa Krueger',
    'author_email': 'makmanx64@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/Makman2/qrpic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
