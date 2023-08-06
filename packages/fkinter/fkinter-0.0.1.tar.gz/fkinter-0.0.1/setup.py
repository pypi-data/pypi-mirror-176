# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fkinter']
install_requires = \
['colorama>=0.4.6,<0.5.0', 'tkdesigner>=1.0.6,<2.0.0']

setup_kwargs = {
    'name': 'fkinter',
    'version': '0.0.1',
    'description': 'Figma to Tkinter generator! 1.0.0!',
    'long_description': '```python\nfrom fkinter import figma_to_tkinter\nfigma_to_tkinter("FILE_URL", "ACCESS_TOKEN")\n```',
    'author': 'ozodbeksobirjonovich',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
