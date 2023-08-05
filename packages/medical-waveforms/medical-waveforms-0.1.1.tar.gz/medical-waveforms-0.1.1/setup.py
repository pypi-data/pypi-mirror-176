# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['medical_waveforms', 'medical_waveforms.features']

package_data = \
{'': ['*'], 'medical_waveforms': ['data/*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.3.4,<2.0.0',
 'pyampd>=0.0.1,<0.0.2',
 'pydantic>=1.9.2,<2.0.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'medical-waveforms',
    'version': '0.1.1',
    'description': 'Preprocessing and analysis of physiological waveforms',
    'long_description': None,
    'author': 'Finneas Catling',
    'author_email': 'f.catling@imperial.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UCL-Chimera/medical-waveforms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
