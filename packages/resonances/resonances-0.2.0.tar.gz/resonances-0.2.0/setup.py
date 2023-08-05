# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resonances',
 'resonances.data',
 'resonances.experiment',
 'resonances.matrix',
 'resonances.resonance']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.2.1,<5.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'rebound>=3.17.3,<4.0.0',
 'scipy>=1.7.0,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['ain = '
                     'resonances.experiment.console:asteroids_in_resonance',
                     'asteroids-in-resonance = '
                     'resonances.experiment.console:asteroids_in_resonance',
                     'ia = resonances.experiment.console:asteroids',
                     'identify-asteroids = '
                     'resonances.experiment.console:asteroids',
                     'identify-quick = resonances.experiment.console:quick',
                     'identify-resonances = '
                     'resonances.experiment.console:identifier',
                     'iq = resonances.experiment.console:quick',
                     'ir = resonances.experiment.console:identifier',
                     'simulation-shape = '
                     'resonances.experiment.console:calc_shape',
                     'ss = resonances.experiment.console:calc_shape']}

setup_kwargs = {
    'name': 'resonances',
    'version': '0.2.0',
    'description': 'Identification of mean-motion resonances',
    'long_description': None,
    'author': 'Evgeny Smirnov',
    'author_email': 'smirik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
