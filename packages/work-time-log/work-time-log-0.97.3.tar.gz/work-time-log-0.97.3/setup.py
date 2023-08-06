# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['work_components']

package_data = \
{'': ['*']}

modules = \
['work']
entry_points = \
{'console_scripts': ['work = work:main']}

setup_kwargs = {
    'name': 'work-time-log',
    'version': '0.97.3',
    'description': 'Manual time tracking via a CLI that works similarly to git.',
    'long_description': None,
    'author': 'Valentin',
    'author_email': 'noemail@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
