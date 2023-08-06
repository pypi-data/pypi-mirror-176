# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['osiotk', 'osiotk.path', 'osiotk.scan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'osiotk',
    'version': '1.2.2',
    'description': 'os io toolkit',
    'long_description': '\n## Osiotk\n\n## Description:\n\n    os io toolkit\n\n## Commands:\n\n# Install Poetry:\n#    python3 -m pip install poetry\n\n# Build Package:\n#    python3 -m poetry build\n\n# Publish Package:\n#    python3 -m poetry publish -u <username> -p <password>\n\n# Install Package Locally:\n#    python3 -m pip install osiotk==1.2.2\n\n# Build And Publish Package:\n#    python3 -m poetry build;python3 -m poetry publish -u <username> -p <password>\n\n# Build Package; Publish Package; Install Package:\n#    python3 -m poetry build;python3 -m poetry publish -u <username> -p <password>;python3 -m pip install osiotk==1.2.2\n\n# Test Osiotk:\n#    python3 -m pytest -rpP tests/\n\n',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
