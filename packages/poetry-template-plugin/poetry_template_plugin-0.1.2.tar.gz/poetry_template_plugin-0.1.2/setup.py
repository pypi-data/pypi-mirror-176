# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_template_plugin']

package_data = \
{'': ['*']}

entry_points = \
{'poetry.application.plugin': ['template = '
                               'poetry_template_plugin.plugin:TemplatePlugin']}

setup_kwargs = {
    'name': 'poetry-template-plugin',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'aachurin',
    'author_email': 'aachurin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
