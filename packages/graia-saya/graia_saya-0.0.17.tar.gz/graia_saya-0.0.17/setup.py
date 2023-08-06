# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia',
 'graia.saya',
 'graia.saya.behaviour',
 'graia.saya.builtins',
 'graia.saya.builtins.broadcast']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.7']

extras_require = \
{'broadcast': ['graia-broadcast>=0.12.1'],
 'scheduler': ['graia-scheduler>=0.0.8,<0.0.9']}

setup_kwargs = {
    'name': 'graia-saya',
    'version': '0.0.17',
    'description': '',
    'long_description': 'None',
    'author': 'GreyElaina',
    'author_email': '31543961+GreyElaina@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
