# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['insta_checker']
install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'insta-checker',
    'version': '0.3.6',
    'description': 'Python Instagram API checker / scrapper / wrapper 2021. Fast and asynchronously scrapes instagram profiles and posts, powered by aiohttp.',
    'long_description': None,
    'author': 'Anton Nechaev',
    'author_email': 'antonnechaev990@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
