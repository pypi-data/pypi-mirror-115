# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aoquality', 'aoquality.tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'matplotlib>=3.1,<4.0', 'python-casacore>=3.0,<4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['aostats = aoquality.tools.aostats:main']}

setup_kwargs = {
    'name': 'aoquality',
    'version': '0.2.0',
    'description': "Python module to access Measurement Sets' quality statistics produced by aoflagger, aoquality or DPPP.",
    'long_description': "# pyaoquality\n\nPython module to access Measurement Sets' quality statistics produced by aoflagger, aoquality or DPPP.",
    'author': '"Florent Mertens"',
    'author_email': '"florent.mertens@gmail.com"',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/flomertens/aoquality/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
