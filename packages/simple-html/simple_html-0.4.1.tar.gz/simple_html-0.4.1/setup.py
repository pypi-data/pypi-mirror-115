# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_html']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typed-ast==1.4.3']}

setup_kwargs = {
    'name': 'simple-html',
    'version': '0.4.1',
    'description': 'Template-less html rendering in Python',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
