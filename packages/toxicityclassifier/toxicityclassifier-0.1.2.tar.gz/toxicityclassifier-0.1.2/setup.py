# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toxicityclassifier']

package_data = \
{'': ['*'], 'toxicityclassifier': ['models/*']}

setup_kwargs = {
    'name': 'toxicityclassifier',
    'version': '0.1.2',
    'description': '',
    'long_description': '# ToxicityClassificator',
    'author': 'D1ffic00lt',
    'author_email': 'dm.filinov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
