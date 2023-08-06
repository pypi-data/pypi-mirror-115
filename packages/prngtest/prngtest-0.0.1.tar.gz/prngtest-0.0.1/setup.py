# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['prngtest']
install_requires = \
['bitarray>=2.2.4,<3.0.0', 'scipy==1.5.4']

setup_kwargs = {
    'name': 'prngtest',
    'version': '0.0.1',
    'description': 'RNG testing CLI and library',
    'long_description': None,
    'author': 'Matthew Barber',
    'author_email': 'quitesimplymatt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honno/prngtest',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
