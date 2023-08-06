# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_composex_specs']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'ecs-composex-specs',
    'version': '0.1.0',
    'description': 'JSON Schema Specifications for ECS Compose-X',
    'long_description': '===================\nECS Compose-X Specs\n===================\n\n\n.. image:: https://img.shields.io/pypi/v/ecs_composex_specs.svg\n        :target: https://pypi.python.org/pypi/ecs_composex_specs\n\n.. image:: https://readthedocs.org/projects/compose-x-specs/badge/?version=latest\n        :target: https://compose-x-specs.readthedocs.io/en/latest/?version=latest\n        :alt: Documentation Status\n\n\nSpecifications for ECS Compose-X.\n\n\n* Free software: MPL2.0\n* Documentation: https://ecs-composex-specs.readthedocs.io.\n\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'John Preston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
