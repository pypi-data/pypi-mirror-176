# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numena', 'numena.dataset', 'numena.features', 'numena.image', 'numena.io']

package_data = \
{'': ['*']}

install_requires = \
['czifile',
 'matplotlib',
 'numpy',
 'opencv-python',
 'pandas',
 'roifile',
 'scikit-image',
 'simplejson',
 'tifffile']

setup_kwargs = {
    'name': 'numena',
    'version': '0.1.3',
    'description': 'Image Processing and Analysis toolbox package',
    'long_description': '# Numena\n',
    'author': 'Kevin Cortacero',
    'author_email': 'cortacero@inserm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
