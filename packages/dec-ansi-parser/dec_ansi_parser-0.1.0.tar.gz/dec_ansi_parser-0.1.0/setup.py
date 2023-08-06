# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dec_ansi_parser']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dec_ansi_parser = dec_ansi_parser.formatter:main']}

setup_kwargs = {
    'name': 'dec-ansi-parser',
    'version': '0.1.0',
    'description': 'Terminal control sequence parser',
    'long_description': "# dec_ansi_parser\n\nPure-python terminal control sequence parser, based on [Paul Williams' DEC-compatible parser](https://www.vt100.net/emu/dec_ansi_parser).\n\nChanges from Williams' parser:\n\n* Handles subparameters\n* Allows UTF-8 encoded strings (treated as normal text)\n* Ignores the backslash (0x5C) in a 7-bit string terminator when exiting an OSC or DCS control string\n\nAny invalid UTF-8 sequences are parsed as individual raw bytes.\n\n## Installation\n\n```bash\n$ pip install dec_ansi_parser\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`dec_ansi_parser` was created by yut23. It is licensed under the terms of the BSD 3-Clause license.\n\n## Credits\n\n`dec_ansi_parser` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'yut23',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
