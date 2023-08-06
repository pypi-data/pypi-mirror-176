# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toml_bench', 'toml_bench.cases']

package_data = \
{'': ['*']}

install_requires = \
['benchwork>=0.0.2,<0.0.3',
 'importlib-metadata>=5.0.0,<6.0.0',
 'pyparam>=0.5,<0.6',
 'python-dateutil>=2.8.2,<3.0.0',
 'qtoml>=0.3.1,<0.4.0',
 'regex>=2022.10.31,<2023.0.0',
 'rtoml>=0.9.0,<0.10.0',
 'toml>=0.10.2,<0.11.0',
 'tomli-w>=1.0.0,<2.0.0',
 'tomli>=2.0.1,<3.0.0',
 'tomlkit>=0.11.6,<0.12.0']

extras_require = \
{':python_version < "3.11"': ['pytomlpp>=1.0.11,<2.0.0']}

entry_points = \
{'console_scripts': ['toml-bench = toml_bench.__main__:main']}

setup_kwargs = {
    'name': 'toml-bench',
    'version': '0.2.1',
    'description': 'Benchmarking for python toml libraries',
    'long_description': 'None',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
