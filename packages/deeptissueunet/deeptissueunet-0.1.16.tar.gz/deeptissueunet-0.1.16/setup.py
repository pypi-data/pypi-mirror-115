# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeptissueunet',
 'deeptissueunet.package',
 'deeptissueunet.package.Unet_2plus',
 'deeptissueunet.siam_package',
 'deeptissueunet.siam_package.helpers']

package_data = \
{'': ['*']}

install_requires = \
['albumentations',
 'barbar',
 'matplotlib',
 'numpy',
 'opencv-python',
 'scikit-image>=0.18.2,<0.19.0',
 'scikit_image',
 'tifffile',
 'torch>=1.9.0,<2.0.0',
 'tqdm',
 'wandb']

setup_kwargs = {
    'name': 'deeptissueunet',
    'version': '0.1.16',
    'description': '',
    'long_description': None,
    'author': 'Yuxi Long',
    'author_email': 'longyuxi@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
