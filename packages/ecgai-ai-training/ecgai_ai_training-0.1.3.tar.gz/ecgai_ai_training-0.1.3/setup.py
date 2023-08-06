# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ecgai_ai_training']

package_data = \
{'': ['*']}

install_requires = \
['PyWavelets==1.3.0',
 'adabound>=0.0.5,<0.0.6',
 'numpy==1.21.6',
 'pandas==1.3.5',
 'pydantic>=1.10.2,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'scikit-image==0.18.3',
 'scikit-learn==1.0.2',
 'torch==1.12.1']

setup_kwargs = {
    'name': 'ecgai-ai-training',
    'version': '0.1.3',
    'description': '',
    'long_description': 'None',
    'author': 'RobC',
    'author_email': 'rob.clapham@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
