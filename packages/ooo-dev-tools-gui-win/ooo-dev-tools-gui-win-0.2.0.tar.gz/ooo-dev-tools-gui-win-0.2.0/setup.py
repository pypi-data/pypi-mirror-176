# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odevgui_win',
 'odevgui_win.class_args',
 'odevgui_win.keys',
 'odevgui_win.kind']

package_data = \
{'': ['*']}

install_requires = \
['ooo-dev-tools>=0.6.2', 'pywinauto>=0.6.8']

setup_kwargs = {
    'name': 'ooo-dev-tools-gui-win',
    'version': '0.2.0',
    'description': 'Methods for ooo-dev-tools and LibreOffice that require automatic GUI interaction for windows.',
    'long_description': '# ooo-dev-tools-gui-win\n\nThis package contains Automation for use with LIbreOffice and [OOO Development Tools] project.\n\n## Documentation\n\nRead [Documentation]\n\n## Installation\n\n```sh\npip install ooo-dev-tools-gui-win\n```\n\nSee Also:\n\n- [OOO Development Tools - Part 3: Draw & Impress](https://python-ooo-dev-tools.readthedocs.io/en/latest/odev/part3/index.html)\n\n[OOO Development Tools]: https://python-ooo-dev-tools.readthedocs.io/en/latest/index.html\n[Documentation]: https://ooo-dev-tools-gui-win.readthedocs.io/en/latest/index.html\n',
    'author': ':Barry-Thomas-Paul: Moss',
    'author_email': 'vibrationoflife@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Amourspirit/python-ooo-dev-tools-gui-win',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
