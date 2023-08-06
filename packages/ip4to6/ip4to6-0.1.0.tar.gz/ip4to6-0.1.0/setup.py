# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ip4to6']
entry_points = \
{'console_scripts': ['ip4to6 = ip4to6:main']}

setup_kwargs = {
    'name': 'ip4to6',
    'version': '0.1.0',
    'description': '',
    'long_description': "# ip4to6\n\nconvert ipv4 to equivalent ipv6\n\n## Usage\n\n### Command Line\n\n``` shell\nip4to6 <ipv4>\n```\n\n### Programmatic API\n\n``` py\nfrom ip4to6 import ip4to6\n\nprint(ip4to6('127.0.0.1'))\n```\n",
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
