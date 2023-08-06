# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schuylkill', 'schuylkill.tests']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy==0.18.0',
 'pandas>=1.3,<2.0',
 'python-levenshtein==0.12.2',
 'scikit-learn>=1.0,<2.0',
 'sparse-dot-topn>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'schuylkill',
    'version': '0.1.2',
    'description': 'Fixing human errors by matching those hard-to-spell words',
    'long_description': 'None',
    'author': 'Nick Hand',
    'author_email': 'nick.hand@phila.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
