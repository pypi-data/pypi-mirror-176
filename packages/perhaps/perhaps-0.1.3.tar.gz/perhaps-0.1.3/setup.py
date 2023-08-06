# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perhaps']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'perhaps',
    'version': '0.1.3',
    'description': 'Perhaps there is no data or perhaps there is',
    'long_description': '# perhaps\nSave your time when dealing with data that *perhaps* may exist.\n',
    'author': 'HKGx',
    'author_email': 'mail@hkgdoes.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HKGx/perhaps',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
