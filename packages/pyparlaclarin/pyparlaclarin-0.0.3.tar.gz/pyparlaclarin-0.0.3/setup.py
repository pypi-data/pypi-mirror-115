# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pyparlaclarin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyparlaclarin',
    'version': '0.0.3',
    'description': 'Read, create, and modify Parla-Clarin XML files',
    'long_description': '# Pyparlaclarin\n\nThis module includes functionality for reading, creating, and modifying Parla-Clarin XML files.\n\nInstall by running\n\n```bash\npip install pyparlaclarin\n```\n',
    'author': 'ninpnin',
    'author_email': 'vainoyrjanainen@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://welfare-state-analytics.github.io/pyparlaclarin/pyparlaclarin/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
