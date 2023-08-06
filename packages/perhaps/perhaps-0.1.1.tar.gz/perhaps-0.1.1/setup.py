# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perhaps']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'perhaps',
    'version': '0.1.1',
    'description': 'Perhaps there is no data or perhaps there is',
    'long_description': '# perhaps\nSave your time when dealing with data that *perhaps* may exist.\n',
    'author': 'HKGx',
    'author_email': 'mail@hkgdoes.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
