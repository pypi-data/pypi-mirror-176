# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocx_xml']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.3.0,<6.0.0',
 'lxml>=4.9.1,<5.0.0',
 'sphinx-autodoc-typehints>=1.19.5,<2.0.0',
 'sphinx-rtd-theme>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'ocx-xml',
    'version': '0.1.0',
    'description': 'Package for working with the python lxml library when parsing OCX XML files, see https://3docx.org',
    'long_description': None,
    'author': 'ocastrup',
    'author_email': 'ole.christian.astrup@dnv.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
