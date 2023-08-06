# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spaces']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spaces',
    'version': '0.1.0',
    'description': 'Utilities for Hugging Face Spaces',
    'long_description': '# Hugging Face Spaces\n\n## Installation\n\n`pip install spaces`\n',
    'author': 'Charles Bensimon',
    'author_email': 'charles@huggingface.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://huggingface.co',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
