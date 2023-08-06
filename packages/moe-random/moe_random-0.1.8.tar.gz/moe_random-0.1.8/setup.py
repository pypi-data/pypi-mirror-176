# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moe_random']

package_data = \
{'': ['*']}

install_requires = \
['Moe>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['moe = moe.cli:main'],
 'moe.plugins': ['random = moe_random.random']}

setup_kwargs = {
    'name': 'moe-random',
    'version': '0.1.8',
    'description': 'Plugin for moe to output a random item from your music library.',
    'long_description': '# moe_random\nAdds a `random` command to Moe to output a random item from your library.\n\nThis is a simple plugin to serve as an example for how to create a third-party plugin for Moe.\n',
    'author': 'Jacob Pavlock',
    'author_email': 'jtpavlock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MoeMusic/moe_random',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
