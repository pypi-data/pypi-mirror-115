# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musamusa_mustextfile']

package_data = \
{'': ['*'], 'musamusa_mustextfile': ['contexts/*']}

setup_kwargs = {
    'name': 'musamusa-mustextfile',
    'version': '0.0.1',
    'description': '.mus -> AnnotatedText',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
