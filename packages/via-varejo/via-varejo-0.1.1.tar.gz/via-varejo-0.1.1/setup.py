# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['via_varejo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'via-varejo',
    'version': '0.1.1',
    'description': 'library com as funcoes utilitarias',
    'long_description': '',
    'author': 'Jaderson Macedo',
    'author_email': 'jaderson.macedo@viavarejo.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
