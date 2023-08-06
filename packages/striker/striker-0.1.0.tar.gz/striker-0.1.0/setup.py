# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['striker',
 'striker.core',
 'striker.core._base',
 'striker.core.hook',
 'striker.core.mixin',
 'striker.core.plugin',
 'striker.mixins',
 'striker.plugins']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.12,<2.0', 'typeguard>=2.13,<3.0']

extras_require = \
{'rich': ['rich>=12.5,<13.0', 'rich-argparse>=0.2.1,<0.3.0']}

setup_kwargs = {
    'name': 'striker',
    'version': '0.1.0',
    'description': 'Minimal and Modular PyTorch Framework',
    'long_description': 'None',
    'author': '0phoff',
    'author_email': '0phoff@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
