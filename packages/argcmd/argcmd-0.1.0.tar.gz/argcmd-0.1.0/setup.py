# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['argcmd']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['argcmd-test = argcmd.__main__:main']}

setup_kwargs = {
    'name': 'argcmd',
    'version': '0.1.0',
    'description': '',
    'long_description': "# argcmd - a super-clean, super-simple Class-based API for git-like command line arguments\n\n## Why\n\nI got sick of implementing this multiple times, and other people asked me how to do it too.\n\n## Requirements\n\nPython 3.7 or later.\n\n## Installation\n\nDownload the `*.whl` file from under `https://github.com/lee-b/argcmd/Releases`, and install\nit with `pip install`. `pip` remote install, and `poetry` instructions to follow.\n\n## Usage\n\nSee `src/argcmd/__main__.py` for an example.  You can run this example as `argcmd-test` after\ninstallation (`argcmd-test` will go away when proper unit tests are added instead).\n\n## License\n\nGNU Aferro General Public License v3.0.  See included LICENSE.TXT file for details.\n\n\n## Contacts\n\nRaise a ticket at github.com/lee-b/argcmd/issues, or email me at `leebraid@gmail.com` _if (and only if)_\na ticket isn't appropriate.\n",
    'author': 'Lee Braiden',
    'author_email': 'leebraid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
