# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biu', 'biu.progress', 'biu.siam_unet', 'biu.siam_unet.helpers', 'biu.unet']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=0.5.2,<0.6.0',
 'barbar>=0.2.1,<0.3.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.19.5,<2.0.0',
 'opencv-python>=4.5.2,<5.0.0',
 'scikit-image>=0.18.2,<0.19.0',
 'scikit_image>=0.18.2,<0.19.0',
 'tifffile',
 'torch>=1.7.0,<2.0.0',
 'tqdm>=4.61.2,<5.0.0',
 'wandb>=0.10.33,<0.11.0']

setup_kwargs = {
    'name': 'bio-image-unet',
    'version': '0.1.1',
    'description': 'Implementations of U-Net and Siam U-Net for biological image segmentation',
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
