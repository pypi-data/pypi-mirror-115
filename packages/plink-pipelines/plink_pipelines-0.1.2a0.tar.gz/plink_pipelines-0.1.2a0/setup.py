# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plink_pipelines']

package_data = \
{'': ['*']}

install_requires = \
['aislib==0.1.4a0',
 'luigi>=3.0.3,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'py>=1.10.0,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0']

entry_points = \
{'console_scripts': ['plink_pipelines = plink_pipelines.make_dataset:main']}

setup_kwargs = {
    'name': 'plink-pipelines',
    'version': '0.1.2a0',
    'description': '',
    'long_description': None,
    'author': 'Arnor Sigurdsson',
    'author_email': 'arnor-sigurdsson@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
