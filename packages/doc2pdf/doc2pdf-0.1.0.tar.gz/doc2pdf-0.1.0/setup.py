# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doc2pdf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'doc2pdf',
    'version': '0.1.0',
    'description': 'A package to convert Doc files to PDF.',
    'long_description': None,
    'author': 'Silas Vasconcelos',
    'author_email': 'silasvasconcelos@hotmail.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
