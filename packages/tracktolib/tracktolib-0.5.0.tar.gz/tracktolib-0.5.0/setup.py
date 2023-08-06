# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tracktolib']

package_data = \
{'': ['*']}

install_requires = \
['python-json-logger>=2.0.4,<3.0.0']

setup_kwargs = {
    'name': 'tracktolib',
    'version': '0.5.0',
    'description': 'Utility library for python',
    'long_description': '# Tracktolib\n\n[![Python versions](https://img.shields.io/pypi/pyversions/tracktolib)](https://pypi.python.org/pypi/tracktolib)\n[![Latest PyPI version](https://img.shields.io/pypi/v/tracktolib?logo=pypi)](https://pypi.python.org/pypi/tracktolib)\n[![CircleCI](https://circleci.com/gh/Tracktor/tracktolib/tree/master.svg?style=shield)](https://app.circleci.com/pipelines/github/Tracktor/tracktolib?branch=master)\n\nUtility library for python\n',
    'author': 'Julien Brayere',
    'author_email': 'julien.brayere@tracktor.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tracktor/tracktolib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
