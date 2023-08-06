# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chunkdup']

package_data = \
{'': ['*']}

install_requires = \
['chunksum>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['chunkdup = chunkdup.chunkdup:main']}

setup_kwargs = {
    'name': 'chunkdup',
    'version': '0.2.0',
    'description': 'Find (partial content) duplicate files.',
    'long_description': '# chunkdup\n\nFind (partial content) duplicate files.\n',
    'author': 'Xie Yanbo',
    'author_email': 'xieyanbo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xyb/chunkdup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
